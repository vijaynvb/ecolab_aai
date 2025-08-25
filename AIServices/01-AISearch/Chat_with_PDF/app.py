import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import AzureSearch
from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from htmlTemplates import css, bot_template, user_template
from langchain.prompts import PromptTemplate
from datetime import datetime
import os

openai_api_key = "1m4mqdn7iqQOhsfap31qVSTyBPSq3A039iCoO37UVpeKKZi12oilJQQJ99BHACL93NaXJ3w3AAAAACOGNwoX"
azure_endpoint = "https://ecolab-azureaifoundry.cognitiveservices.azure.com/"
openai_api_version = "2024-12-01-preview"

# Azure AI Search configuration
# Prefer environment variables if set; otherwise use provided defaults
AZURE_SEARCH_ENDPOINT = "https://ecolab.search.windows.net"
AZURE_SEARCH_ADMIN_KEY = "lrKZ7CvF6mBnDKAP8FQ3ZnsZ1eNIymnWLTp0PoOQZHAzSeAyRms9"
# Customize if you want a different index name
AZURE_SEARCH_INDEX = "ecolab-pdf-index"

# This method takes a list of PDF files as input, reads them using PdfReader from PyPDF2, 
# and concatenates the text content from all pages into a single string
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# This method splits the provided text into smaller chunks. It uses the CharacterTextSplitter from langchain library
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# This method converts text chunks into embeddings and creates a FAISS vector store.
def get_vectorstore(text_chunks):
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment="text-embedding-ada-002",
        openai_api_key=openai_api_key,
        azure_endpoint=azure_endpoint,
        openai_api_version=openai_api_version,
    )

    # Create or connect to Azure AI Search index and upload chunks
    vectorstore = AzureSearch.from_texts(
        texts=text_chunks,
        embedding=embeddings,
        azure_search_endpoint=AZURE_SEARCH_ENDPOINT,
        azure_search_key=AZURE_SEARCH_ADMIN_KEY,
        index_name=AZURE_SEARCH_INDEX,
    )

    st.success("PDF loaded and indexed in Azure AI Search")
    return vectorstore

# delete some documents from the azure ai search vector db

def delete_documents_from_vectorstore(vectorstore, doc_ids):
    for doc_id in doc_ids:
        AzureSearch.delete_document(vectorstore, doc_id)
    st.success("Selected documents deleted from Azure AI Search")
    return vectorstore

# list all the documents in the azure ai search vector db

def list_documents_in_vectorstore(vectorstore):
    documents = []
    skip = 0
    top = 1000 # Max value for 'top'
    
    while True:
        results = vectorstore.search(query="", search_type="similarity")
        current_batch = list(results) # Convert results to a list
        print(current_batch)
        if not current_batch:
            break # No more documents
    
        documents.extend(current_batch)
        skip += len(current_batch)
    print(documents)
    return documents

# This method initializes a conversational retrieval chain using a language model and a vector store
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def get_conversation_chain(vectorstore):
    # System prompt
    qa_prompt_template = """
    You are a professional data assistant designed to help users with questions related to their uploaded documents.

    - If the user greets you, respond courteously and inform them that you're here to assist with queries based on their provided data.
    - If a question is relevant to the uploaded documents, use the provided context to generate a helpful and accurate response.
    - If the question is outside the scope of the provided data, respond politely and clarify that you can only assist with questions related to the uploaded content.
    - If you are unsure of the answer based on the available context, respond with: "I'm sorry, I don't have enough information to answer that based on the provided documents."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    qa_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=qa_prompt_template,
    )

    # Default question rephrasing prompt (can be customized)
    condense_question_prompt = PromptTemplate.from_template(
        "Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question.\n\n"
        "Chat History:\n{chat_history}\nFollow-up question: {question}\nStandalone question:"
    )

    llm = AzureChatOpenAI(
        deployment_name="gpt-4o",
        openai_api_key=openai_api_key,
        azure_endpoint=azure_endpoint,
        openai_api_version=openai_api_version
    )

    # Main QA chain using custom prompt
    qa_chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=qa_prompt)

    # Question generator chain (needed for ConversationalRetrievalChain)
    question_generator = LLMChain(llm=llm, prompt=condense_question_prompt)

    # Chat memory
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)

    # Final chain with required fields
    conversation_chain = ConversationalRetrievalChain(
        retriever=vectorstore.as_retriever(),
        combine_docs_chain=qa_chain,
        question_generator=question_generator,
        memory=memory
    )

    return conversation_chain


# This method handles user input by passing the question to the conversation chain and displaying the response
def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    # Reverse chat history to show latest messages at the top
    for i, message in enumerate(reversed(st.session_state.chat_history)):
        time_str = datetime.now().strftime('%H:%M')
        if (len(st.session_state.chat_history) - 1 - i) % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content).replace("{{TIME}}", time_str), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content).replace("{{TIME}}", time_str), unsafe_allow_html=True)


#  This is the main function which orchestrates the entire process. It sets up 
# the Streamlit app, handles user input, and processes PDF documents.
def main():
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)
                
                list_documents_in_vectorstore(vectorstore)
                


if __name__ == '__main__':
    main()

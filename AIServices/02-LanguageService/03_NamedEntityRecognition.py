# endpoint = "https://ecolab16789.cognitiveservices.azure.com/"
# key = "4oBDyNySUirl7mrU96NDfnoK9h5Mbd7Eym45yMBopjQDjjwPvof6JQQJ99BHACYeBjFXJ3w3AAAaACOGglMV"
endpoint = "https://ecolab-language.cognitiveservices.azure.com/"
key = "D36sIAF9Nnkmb2pou5pqR0TbYw5Xr89D3B52XFa01VnH7waGBzd9JQQJ99BHACL93NaXJ3w3AAAaACOGv3Fu"


from azure.ai.textanalytics import TextAnalyticsClient #pip install azure-ai-textanalytics
from azure.core.credentials import AzureKeyCredential

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Example function for recognizing entities from text
def entity_recognition_example(client):

    try:
        documents = ["I had a wonderful trip to Seattle last week."]
        result = client.recognize_entities(documents = documents)[0]

        print("Named Entities:\n")
        for entity in result.entities:
            print("\tText: \t", entity.text, "\tCategory: \t", entity.category, "\tSubCategory: \t", entity.subcategory,
                    "\n\tConfidence Score: \t", round(entity.confidence_score, 2), "\tLength: \t", entity.length, "\tOffset: \t", entity.offset, "\n")

    except Exception as err:
        print("Encountered exception. {}".format(err))
entity_recognition_example(client)
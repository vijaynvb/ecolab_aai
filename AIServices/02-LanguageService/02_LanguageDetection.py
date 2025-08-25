endpoint = "https://ecolab-language.cognitiveservices.azure.com/"
key = "D36sIAF9Nnkmb2pou5pqR0TbYw5Xr89D3B52XFa01VnH7waGBzd9JQQJ99BHACL93NaXJ3w3AAAaACOGv3Fu"

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Example method for detecting the language of text
def language_detection_example(client):
    try:
        documents = ["सभी को नमस्कार"]
        response = client.detect_language(documents = documents, country_hint = 'us')[0]
        print("Language: ", response.primary_language.name)

    except Exception as err:
        print("Encountered exception. {}".format(err))
language_detection_example(client)
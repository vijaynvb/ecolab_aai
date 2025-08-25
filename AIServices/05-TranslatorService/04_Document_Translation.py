import requests, uuid, json

# Configuration
key = "5tY84qhc3hquNY8A7wzf01s07Oi2ROFoQw06C4bI6f2z1gk7YrLkJQQJ99BHACL93NaXJ3w3AAAbACOGqrcC"
endpoint = "https://api.cognitive.microsofttranslator.com/"
region = "australiaeast"
path = '/translate?api-version=3.0'
params = '&from=en&to=hi'  # Translating from English to Hindi
constructed_url = endpoint + path + params

headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': region,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

def translate_text(text):
    body = [{'text': text}]
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    return response[0]["translations"][0]["text"]

# Assuming you have a simple text file 'document.txt' in English
input_filename = "Document\\test.txt"
output_filename = "Document\\document_translated.txt"

try:
    with open(input_filename, 'r', encoding='utf-8') as file:
        original_text = file.read()

    translated_text = translate_text(original_text)
    print("Translated Text:", translated_text)

    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(translated_text)

    print("Document translated successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

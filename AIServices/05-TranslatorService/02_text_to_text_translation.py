import requests, uuid, json

# Your subscription key and endpoint from your Azure Translator resource
key = "5tY84qhc3hquNY8A7wzf01s07Oi2ROFoQw06C4bI6f2z1gk7YrLkJQQJ99BHACL93NaXJ3w3AAAbACOGqrcC"
endpoint = "https://api.cognitive.microsofttranslator.com/"
region = "australiaeast"

path = '/translate?api-version=3.0'
params = '&from=en&to=hi'
constructed_url = endpoint + path + params

headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': region,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

# The text you want to translate
body = [{
    'text': 'I am getting confused with all these services, I cannot differentiate between them.'
}]

# Make the request
response = requests.post(constructed_url, headers=headers, json=body)
response = response.json()

# Print the translation
print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4))

# Extracting and printing just the translated text
for translation in response[0]["translations"]:
    print(translation["text"])

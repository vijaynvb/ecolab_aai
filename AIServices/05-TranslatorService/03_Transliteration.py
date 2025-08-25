import os, requests, uuid, json

# Add your subscription key and endpoint
key = "5tY84qhc3hquNY8A7wzf01s07Oi2ROFoQw06C4bI6f2z1gk7YrLkJQQJ99BHACL93NaXJ3w3AAAbACOGqrcC"
endpoint = "https://api.cognitive.microsofttranslator.com/"
region = "australiaeast"

# The path for transliteration
path = '/transliterate?api-version=3.0'

# Specify the language and scripts. Example below: Hindi (Devanagari) -> Latin
constructed_url = endpoint + path + '&language=hi&fromScript=Deva&toScript=Latn'

# &language=ru&fromScript=cyrl&toScript=latn
# Set the headers
headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': region,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

# Replace the body with the text you want to transliterate

body = [{
    'Text': 'मुझे कृत्रिम बुद्धिमत्ता सीखना पसंद है।',  # sample Hindi text
}]
# Владимир  (russian)  vladimir

# Make the request
response = requests.post(constructed_url, headers=headers, json=body)
response = response.json()

print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

from azure.ai.translation.text import TextTranslationClient #pip install azure-ai-translation-text
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError
from azure.core.credentials import AzureKeyCredential

# set `<your-key>`, `<your-endpoint>`, and  `<region>` variables with the values from the Azure portal
key = "5tY84qhc3hquNY8A7wzf01s07Oi2ROFoQw06C4bI6f2z1gk7YrLkJQQJ99BHACL93NaXJ3w3AAAbACOGqrcC"
endpoint = "https://api.cognitive.microsofttranslator.com/"
region = "australiaeast"

credential = AzureKeyCredential (key)
text_translator = TextTranslationClient(endpoint=endpoint, credential=credential, region=region)


try:
    response = text_translator.get_supported_languages()

    print(
        f"Number of supported languages for translate operation: {len(response.translation) if response.translation is not None else 0}"
    )
    print(
        f"Number of supported languages for transliterate operation: {len(response.transliteration) if response.transliteration is not None else 0}"
    )
    print(
        f"Number of supported languages for dictionary operations: {len(response.dictionary) if response.dictionary is not None else 0}"
    )

    if response.translation is not None:
        print("Translation Languages:")
        for key, value in response.translation.items():
            print(f"{key} -- name: {value.name} ({value.native_name})")

    if response.transliteration is not None:
        print("Transliteration Languages:")
        for key, value in response.transliteration.items():
            print(f"{key} -- name: {value.name}, supported script count: {len(value.scripts)}")

    if response.dictionary is not None:
        print("Dictionary Languages:")
        for key, value in response.dictionary.items():
            print(f"{key} -- name: {value.name}, supported target languages count: {len(value.translations)}")

except HttpResponseError as exception:
    if exception.error is not None:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")
    raise


try:
    to_language = ["hi",'ar']
    input_text_elements = ["This is a test"]

    response = text_translator.translate(body=input_text_elements, to_language=to_language)
    translation = response[0] if response else None

    if translation:
        detected_language = translation.detected_language
        if detected_language:
            print(
                f"Detected languages of the input text: {detected_language.language} with score: {detected_language.score}."
            )
        for translated_text in translation.translations:
            print(f"Text was translated to: '{translated_text.to}' and the result is: '{translated_text.text}'.")

except HttpResponseError as exception:
    if exception.error is not None:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")


try:
    source_language = "en"
    target_languages = ["es", "it"]
    input_text_elements = [ InputTextItem(text = "Am I impressed with language services? yes indeed iam.") ]

    response = text_translator.translate(body = input_text_elements, to_language = target_languages)
    translation = response[0] if response else None

    if translation:
        for translated_text in translation.translations:
            print(f"Text was translated to: '{translated_text.to}' and the result is: '{translated_text.text}'.")

except HttpResponseError as exception:
    print(f"Error Code: {exception.error.code}")
    print(f"Message: {exception.error.message}")
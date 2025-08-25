# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
# https://github.com/Azure-Samples/document-intelligence-code-samples/blob/main/Python(v4.0)/Prebuilt_model/sample_analyze_invoices.py

"""
FILE: sample_analyze_invoices.py

DESCRIPTION:
    This sample demonstrates how to analyze invoices.

    See fields found on a invoice here:
    https://aka.ms/invoice-field-schema

PREREQUISITES:
    The following prerequisites are necessary to run the code. For more details, please visit the "How-to guides" link: https://aka.ms/how-to-guide

    -------Python and IDE------
    1) Install Python 3.7 or later (https://www.python.org/), which should include pip (https://pip.pypa.io/en/stable/).
    2) Install the latest version of Visual Studio Code (https://code.visualstudio.com/) or your preferred IDE. 
    
    ------Azure AI services or Document Intelligence resource------ 
    Create a single-service (https://aka.ms/single-service) or multi-service (https://aka.ms/multi-service) resource.
    You can use the free pricing tier (F0) to try the service and upgrade to a paid tier for production later.
    
    ------Get the key and endpoint------
    1) After your resource is deployed, select "Go to resource". 
    2) In the left navigation menu, select "Keys and Endpoint". 
    3) Copy one of the keys and the Endpoint for use in this sample. 
    
    ------Set your environment variables------
    At a command prompt, run the following commands, replacing <yourKey> and <yourEndpoint> with the values from your resource in the Azure portal.
    1) For Windows:
       setx DOCUMENTINTELLIGENCE_API_KEY <yourKey>
       setx DOCUMENTINTELLIGENCE_ENDPOINT <yourEndpoint>
       • You need to restart any running programs that read the environment variable.
    2) For macOS:
       export key=<yourKey>
       export endpoint=<yourEndpoint>
       • This is a temporary environment variable setting method that only lasts until you close the terminal session. 
       • To set an environment variable permanently, visit: https://aka.ms/set-environment-variables-for-macOS
    3) For Linux:
       export DOCUMENTINTELLIGENCE_API_KEY=<yourKey>
       export DOCUMENTINTELLIGENCE_ENDPOINT=<yourEndpoint>
       • This is a temporary environment variable setting method that only lasts until you close the terminal session. 
       • To set an environment variable permanently, visit: https://aka.ms/set-environment-variables-for-Linux
       
    ------Set up your programming environment------
    At a command prompt,run the following code to install the Azure AI Document Intelligence client library for Python with pip:
    pip install azure-ai-documentintelligence --pre
    
    ------Create your Python application------
    1) Create a new Python file called "sample_analyze_invoices.py" in an editor or IDE.
    2) Open the "sample_analyze_invoices.py" file and insert the provided code sample into your application.
    3) At a command prompt, use the following code to run the Python code: 
       python sample_analyze_invoices.py
"""

import os


def analyze_invoice():
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient #pip install azure-ai-documentintelligence
    from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest

    # For how to obtain the endpoint and key, please see PREREQUISITES above.
    endpoint = "https://ecolab-document-intelligence.cognitiveservices.azure.com/"
    key = "EJ4HjHZg5iZIgfnL6T4Ovf6Z0Fu6ucAMVVoVJc65hpDClxH9iHHrJQQJ99BHACL93NaXJ3w3AAALACOGrxa3"

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # Analyze a document at a URL:
    invoiceUrl = "https://raw.githubusercontent.com/vijaynvb/ecolab_aai/46cf89c700dc75bf08bbb8a783e3cb9acd0ff76e/Docs/invoice.pdf"
    # Replace with your actual invoiceUrl:
    # If you use the URL of a public website, to find more URLs, please visit: https://aka.ms/more-URLs 
    # If you analyze a document in Blob Storage, you need to generate Public SAS URL, please visit: https://aka.ms/create-sas-tokens
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-invoice",
        AnalyzeDocumentRequest(url_source=invoiceUrl)
    )       
    
    # # If analyzing a local document, remove the comment markers (#) at the beginning of these 8 lines.
    # # Delete or comment out the part of "Analyze a document at a URL" above.
    # # Replace <path to your sample file>  with your actual file path.
    # path_to_sample_document = "<path to your sample file>"
    # with open(path_to_sample_document, "rb") as f:
    #     poller = document_intelligence_client.begin_analyze_document(
    #         "prebuilt-invoice", analyze_request=f, locale="en-US", content_type="application/octet-stream"
    #     )
    invoices: AnalyzeResult = poller.result()   

    # [START analyze_invoices]
    if invoices.documents:
        for idx, invoice in enumerate(invoices.documents):
            print(f"--------Analyzing invoice #{idx + 1}--------")
            if invoice.fields:
                vendor_name = invoice.fields.get("VendorName")
                if vendor_name:
                    print(f"Vendor Name: {vendor_name.get('content')} has confidence: {vendor_name.get('confidence')}")
                vendor_address = invoice.fields.get("VendorAddress")
                if vendor_address:
                    print(
                        f"Vendor Address: {vendor_address.get('content')} has confidence: {vendor_address.get('confidence')}"
                    )
                vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
                if vendor_address_recipient:
                    print(
                        f"Vendor Address Recipient: {vendor_address_recipient.get('content')} has confidence: {vendor_address_recipient.get('confidence')}"
                    )
                customer_name = invoice.fields.get("CustomerName")
                if customer_name:
                    print(
                        f"Customer Name: {customer_name.get('content')} has confidence: {customer_name.get('confidence')}"
                    )
                customer_id = invoice.fields.get("CustomerId")
                if customer_id:
                    print(f"Customer Id: {customer_id.get('content')} has confidence: {customer_id.get('confidence')}")
                customer_address = invoice.fields.get("CustomerAddress")
                if customer_address:
                    print(
                        f"Customer Address: {customer_address.get('content')} has confidence: {customer_address.get('confidence')}"
                    )
                customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
                if customer_address_recipient:
                    print(
                        f"Customer Address Recipient: {customer_address_recipient.get('content')} has confidence: {customer_address_recipient.get('confidence')}"
                    )
                invoice_id = invoice.fields.get("InvoiceId")
                if invoice_id:
                    print(f"Invoice Id: {invoice_id.get('content')} has confidence: {invoice_id.get('confidence')}")
                invoice_date = invoice.fields.get("InvoiceDate")
                if invoice_date:
                    print(
                        f"Invoice Date: {invoice_date.get('content')} has confidence: {invoice_date.get('confidence')}"
                    )
                invoice_total = invoice.fields.get("InvoiceTotal")
                if invoice_total:
                    print(
                        f"Invoice Total: {invoice_total.get('content')} has confidence: {invoice_total.get('confidence')}"
                    )
                due_date = invoice.fields.get("DueDate")
                if due_date:
                    print(f"Due Date: {due_date.get('content')} has confidence: {due_date.get('confidence')}")
                purchase_order = invoice.fields.get("PurchaseOrder")
                if purchase_order:
                    print(
                        f"Purchase Order: {purchase_order.get('content')} has confidence: {purchase_order.get('confidence')}"
                    )
                billing_address = invoice.fields.get("BillingAddress")
                if billing_address:
                    print(
                        f"Billing Address: {billing_address.get('content')} has confidence: {billing_address.get('confidence')}"
                    )
                billing_address_recipient = invoice.fields.get("BillingAddressRecipient")
                if billing_address_recipient:
                    print(
                        f"Billing Address Recipient: {billing_address_recipient.get('content')} has confidence: {billing_address_recipient.get('confidence')}"
                    )
                shipping_address = invoice.fields.get("ShippingAddress")
                if shipping_address:
                    print(
                        f"Shipping Address: {shipping_address.get('content')} has confidence: {shipping_address.get('confidence')}"
                    )
                shipping_address_recipient = invoice.fields.get("ShippingAddressRecipient")
                if shipping_address_recipient:
                    print(
                        f"Shipping Address Recipient: {shipping_address_recipient.get('content')} has confidence: {shipping_address_recipient.get('confidence')}"
                    )
                print("Invoice items:")
                items = invoice.fields.get("Items")
                if items:
                    for idx, item in enumerate(items.get("valueArray")):
                        print(f"...Item #{idx + 1}")
                        item_description = item.get("valueObject").get("Description")
                        if item_description:
                            print(
                                f"......Description: {item_description.get('content')} has confidence: {item_description.get('confidence')}"
                            )
                        item_quantity = item.get("valueObject").get("Quantity")
                        if item_quantity:
                            print(
                                f"......Quantity: {item_quantity.get('content')} has confidence: {item_quantity.get('confidence')}"
                            )
                        unit = item.get("valueObject").get("Unit")
                        if unit:
                            print(f"......Unit: {unit.get('content')} has confidence: {unit.get('confidence')}")
                        unit_price = item.get("valueObject").get("UnitPrice")
                        if unit_price:
                            unit_price_code = (
                                unit_price.get("valueCurrency").get("currencyCode")
                                if unit_price.get("valueCurrency").get("currencyCode")
                                else ""
                            )
                            print(
                                f"......Unit Price: {unit_price.get('content')}{unit_price_code} has confidence: {unit_price.get('confidence')}"
                            )
                        product_code = item.get("valueObject").get("ProductCode")
                        if product_code:
                            print(
                                f"......Product Code: {product_code.get('content')} has confidence: {product_code.get('confidence')}"
                            )
                        item_date = item.get("valueObject").get("Date")
                        if item_date:
                            print(
                                f"......Date: {item_date.get('content')} has confidence: {item_date.get('confidence')}"
                            )
                        tax = item.get("valueObject").get("Tax")
                        if tax:
                            print(f"......Tax: {tax.get('content')} has confidence: {tax.get('confidence')}")
                        amount = item.get("valueObject").get("Amount")
                        if amount:
                            print(f"......Amount: {amount.get('content')} has confidence: {amount.get('confidence')}")
                subtotal = invoice.fields.get("SubTotal")
                if subtotal:
                    print(f"Subtotal: {subtotal.get('content')} has confidence: {subtotal.get('confidence')}")
                total_tax = invoice.fields.get("TotalTax")
                if total_tax:
                    print(f"Total Tax: {total_tax.get('content')} has confidence: {total_tax.get('confidence')}")
                previous_unpaid_balance = invoice.fields.get("PreviousUnpaidBalance")
                if previous_unpaid_balance:
                    print(
                        f"Previous Unpaid Balance: {previous_unpaid_balance.get('content')} has confidence: {previous_unpaid_balance.get('confidence')}"
                    )
                amount_due = invoice.fields.get("AmountDue")
                if amount_due:
                    print(f"Amount Due: {amount_due.get('content')} has confidence: {amount_due.get('confidence')}")
                service_start_date = invoice.fields.get("ServiceStartDate")
                if service_start_date:
                    print(
                        f"Service Start Date: {service_start_date.get('content')} has confidence: {service_start_date.get('confidence')}"
                    )
                service_end_date = invoice.fields.get("ServiceEndDate")
                if service_end_date:
                    print(
                        f"Service End Date: {service_end_date.get('content')} has confidence: {service_end_date.get('confidence')}"
                    )
                service_address = invoice.fields.get("ServiceAddress")
                if service_address:
                    print(
                        f"Service Address: {service_address.get('content')} has confidence: {service_address.get('confidence')}"
                    )
                service_address_recipient = invoice.fields.get("ServiceAddressRecipient")
                if service_address_recipient:
                    print(
                        f"Service Address Recipient: {service_address_recipient.get('content')} has confidence: {service_address_recipient.get('confidence')}"
                    )
                remittance_address = invoice.fields.get("RemittanceAddress")
                if remittance_address:
                    print(
                        f"Remittance Address: {remittance_address.get('content')} has confidence: {remittance_address.get('confidence')}"
                    )
                remittance_address_recipient = invoice.fields.get("RemittanceAddressRecipient")
                if remittance_address_recipient:
                    print(
                        f"Remittance Address Recipient: {remittance_address_recipient.get('content')} has confidence: {remittance_address_recipient.get('confidence')}"
                    )
    # [END analyze_invoices]


if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError
    # from dotenv import find_dotenv, load_dotenv

    try:
        # load_dotenv(find_dotenv())
        analyze_invoice()
    except HttpResponseError as error:
        # Examples of how to check an HttpResponseError
        # Check by error code:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            # Raise the error again after printing it
            raise
        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        # Raise the error again
        raise

# Next steps:
# Learn more about Invoice model: https://aka.ms/concept-invoice
# Find more sample code: https://aka.ms/doc-intelligence-samples
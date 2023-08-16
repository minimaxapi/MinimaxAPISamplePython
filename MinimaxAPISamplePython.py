import requests
import json
import datetime
import uuid
from requests.exceptions import HTTPError
import base64

#VARIABLES
username = "xxx"
password = "xxx"
client_id = "xxx"
client_secret = "xxx"

lokalizacija='SI' # RS, HR
APIBaseUrl = "https://moj.minimax." + lokalizacija + "/" + lokalizacija


### FUNCTION definitions

# Obtain token
def get_access_token(username, password, client_id, client_secret):
    token_endpoint = APIBaseUrl + "/aut/oauth20/token"
    response = requests.post(
        token_endpoint,
        data = {'grant_type': 'password',
                'username': username,
                'password': password,
                'scope': 'minimax.si',
               },
        auth=(client_id, client_secret),
    )
    return response.json()["access_token"]

# GET OrganizationId
def GetMyOrganizationId():

    api_url=APIBaseUrl + "/API/api/currentuser/orgs"

    head = {"Authorization": "Bearer " + token}

    response = requests.get(api_url, headers=head)
    
    if response.status_code != 200:
        print(response.status_code)
    else: 
        # serialize response
        data=response.json()
        # Get Organization ID    
        if data and 'Rows' in data:
            organization_id=(data.get('Rows')[0]['Organisation']['ID'])
            response.close()

    return organization_id

# GET GetVatRateByCode
def GetVatRateByCode(organization_id, vat_rate_code, date): # Returns also vat rate id

    api_url = APIBaseUrl + "/API/api/orgs/" + str(organization_id) + "/vatrates/code(" + vat_rate_code + ")""?""date=" + date

    head = {"Authorization": "Bearer " + token}

    response = requests.get(api_url, headers=head)

    if response.status_code != 200:
        print(response.status_code)
        
        return (response.status_code)
    else:
        # serialize response
        data=response.json()

        vatRateId=(data.get('VatRateId'))
        vatPercent=(data.get('Percent'))
        response.close()

        return vatRateId, vatPercent

# GET GetCurrencyByCode
def GetCurrencyByCode(organization_id, currencyCode):

    api_url = APIBaseUrl + "/API/api/orgs/" + str(organization_id) + "/currencies/code(" +currencyCode + ")"

    head = {"Authorization": "Bearer " + token}

    response = requests.get(api_url, headers=head)

    if response.status_code != 200:
        print(response.status_code)
        
        return (response.status_code)
    else:
        # serialize response
        data=response.json()

        currencyId=(data.get('CurrencyId'))
        response.close()

        return currencyId

# GET GetCountryByCode
def GetCountryByCode(organization_id, countryCode):
    
    api_url = APIBaseUrl + "/API/api/orgs/" + str(organization_id) + "/countries/code(" + countryCode + ")"
    
    head = {"Authorization": "Bearer " + token}

    response = requests.get(api_url, headers=head)

    if response.status_code != 200:
        print(response.status_code)
        
        return (response.status_code)
    else:
         # serialize response
        data=response.json()

        CountryId=(data.get('CountryId'))
        response.close()

        return CountryId

# GET GetReportTemplateIdByDisplayType
def GetReportTemplateIdByDisplayType(organization_id, DisplayType):

    api_url = APIBaseUrl + "/API/api/orgs/" + str(organization_id) + "/report-templates/?SearchString=" + DisplayType

    head = {"Authorization": "Bearer " + token}

    response = requests.get(api_url, headers=head)

    if response.status_code != 200:
        print(response.status_code)
        
        return (response.status_code)
    else:
        data=response.json()

        if data and 'Rows' in data:
            ReportTemplateId=(data.get('Rows')[0]['ReportTemplateId'])

        response.close()

    return ReportTemplateId

# GET GetEmployeeId by search string (name is used in this example)
def GetEmployeeId(organization_id, employee_search_string):

    api_url = APIBaseUrl + "/API/api/orgs/" + str(organization_id) + "/employees" + employee_search_string

    head = {"Authorization": "Bearer " + token}

    response = requests.get(api_url, headers=head)

    if response.status_code != 200:
        print(response.status_code)
        
        return (response.status_code)
    else:
        data=response.json()

        if data and 'Rows' in data:
            employeeId=(data.get('Rows')[0]['EmployeeId'])

        response.close()

        return employeeId

# POST AddItem
def AddItem(organization_id, data):

    api_url = APIBaseUrl + "/API/api/orgs/" + str(organization_id) + "/items"

    head = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json; charset=utf-8",
        }

    try:
        response = requests.post(api_url, data, headers=head)
        response.close()
    
        if response.status_code == 201:
            response = requests.get(response.headers['Location'], headers=head)
            response.close()
            data=response.json()
            ItemId=(data.get('ItemId'))
            return ItemId
        else:
            return response.status_code, response.text
    except HTTPError as e:
        return(e.response.text())

# POST AddCustomer    
def AddCustomer(organization_id, data):
    
    api_url = APIBaseUrl + "/API/api/orgs/" + str(organization_id) + "/customers"

    head = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json; charset=utf-8",
        }
    
    try:
        response = requests.post(api_url, data, headers=head)
        response.close()

        if response.status_code == 201:
            response = requests.get(response.headers['Location'], headers=head)
            response.close()
            data=response.json()
            CustomerId=(data.get('CustomerId'))
            return CustomerId
        else:
            return response.status_code, response.text
    except HTTPError as e:
        return(e.response.text())

# POST AddIssuedInvoice
def AddIssuedInvoice(organization_id, data):

    api_url = APIBaseUrl + "/API/api/orgs/" + str(organization_id) + "/issuedinvoices"

    head = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json; charset=utf-8",
        }
    
    try:
        response = requests.post(api_url, data, headers=head)
        
        if(response.status_code == 201):
            for key, value in (response.headers).items():
                if(key == "Location"):
                    IssuedInvoiceId = value.split('=')[-1]
            
        response.close()

        return IssuedInvoiceId
    
    except HTTPError as e:
        return(e.response.text())

# PUT UpdateIssuedInvoice
def UpdateIssuedInvoice(organization_id, issuedInvoiceId, rowVersion, actionName, data):

    api_url = APIBaseUrl + "/API/api/orgs/" + str(organization_id) + "/issuedinvoices/" + str(issuedInvoiceId) + "/actions/" + actionName + "?rowVersion=" + str(rowVersion)

    head = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json; charset=utf-8",
        }
    
    try:
        response = requests.put(api_url, data, headers=head)
        data = response.json()

        for key, value in data.items():
            if(key == "Data"):
                pdf_data = value['AttachmentData']

        response.close()

        return pdf_data
    
    except HTTPError as e:
        return(e.response.text())

### FUNCTION USAGE

#Get token
token=(get_access_token(username = username, password = password, client_id=client_id, client_secret=client_secret))

### GET OrgId
organization_id=GetMyOrganizationId()

### GET Codes
str_date = (str)(datetime.date.today().strftime("%Y-%m-%d"))
str_vat_code = "S"
currencyCode = "EUR"
countryCode = "HU"
IRreportTemplateCode = "IR"
DOreportTemplateCode = "DO"
itemName = str(uuid.uuid4())
itemCode = str(uuid.uuid4())
customerCode = str(uuid.uuid4())

vatRateId = GetVatRateByCode(organization_id, str_vat_code, str_date)
currencyId = GetCurrencyByCode(organization_id, currencyCode)
countryId = str(GetCountryByCode(organization_id, countryCode))
currencyId = str(GetCurrencyByCode(organization_id, currencyCode))
IRreportTemplateId = str(GetReportTemplateIdByDisplayType(organization_id, IRreportTemplateCode))
DOreportTemplateId = str(GetReportTemplateIdByDisplayType(organization_id, DOreportTemplateCode))

if(lokalizacija == "HR"):
    employeeId = str(GetEmployeeId(organization_id, ""))
else:
    employeeId = ""

### POST requests
# real data is used for some values!
# POST AddItem
json_data={
    "Name": "ArticleName",
    "Code": itemCode[0: 29],
    "ItemType": "B",
    "VatRate": {"ID": int(vatRateId[0])},
    "Price": "100.0",
    "Currency": {"ID": int(currencyId)},
}

ItemId = AddItem(organization_id, json.dumps(json_data))

# POST AddCustomer (change Code string value to reuse it )
json_data = {
	"Name": "Test",
	"Address": "test",
	"PostalCode": "1234",
	"City": "Nowhere",
	"Code": customerCode[0: 29],
	"Country": {"ID": int(countryId)},
	"CountryName": "-",
	"SubjectToVAT": "N",
	"Currency": {"ID": int(currencyId)},
	"EInvoiceIssuing": "SeNePripravlja"
}

CustomerId = AddCustomer(organization_id, json.dumps(json_data))

# POST AddIssuedInvoice
json_data = {
    "Customer": {"ID": CustomerId},
    "Employee": {"ID": employeeId},
    "DateIssued": str_date,
    "DateTransaction": str_date,
    "DateTransactionFrom": str_date,
    "DateDue": str_date,
    "AddresseeName": "Test",
    "AddresseeAddress": "Nowhere",
    "AddresseePostalCode": "1234",
    "AddresseeCity": "test",
	"AddresseeCountryName" :"-", 
    "AddresseeCountry": {"ID": countryId},
    "Currency": {"ID": currencyId},
    "IssuedInvoiceReportTemplate": {"ID": IRreportTemplateId},
    "DeliveryNoteReportTemplate": {"ID": DOreportTemplateId},
    "Status": "0",
    "PricesOnInvoice": "N",
    "RecurringInvoice": "N",
    "InvoiceType": "R",
    "IssuedInvoiceRows": [{
        "Item": {"ID": ItemId},
        "ItemName": "Test",
        "RowNumber": "1",
        "ItemCode": "code",
        "Description": "description",
        "Quantity": "1",
        "UnitOfMeasurement": "kom",
        "Price": 10.6475,
        "PriceWithVAT": 12.99,
        "VATPercent": 0,
        "Discount": 0,
        "DiscountPercent": 0,
        "Value": 10.6475,
        "VatRate": {"ID": vatRateId[0]},
    }],   
}

# POST AddIssuedInvoice (returns invoice id)
InvoiceId = (AddIssuedInvoice(organization_id, json.dumps(json_data)))

# PUT UpdateIssuedInvoice
actionName = "IssueAndGeneratePdf"
pdf_data = base64.b64decode(UpdateIssuedInvoice(organization_id, InvoiceId, "", actionName, json.dumps(json_data)))

filename = (str)(datetime.date.today().strftime("%Y%m%d%H%M%S_")) + "test.pdf"

with open(filename, "wb") as f:
    f.write(pdf_data)

print(filename)

import requests
import csv
from dotenv import dotenv_values
import urllib.parse

# Load Mautic configuration from .env file
config = dotenv_values('.env')
mautic_url = config['MAUTIC_URL']
client_id = config['CLIENT_ID']
client_secret = config['CLIENT_SECRET']
redirect_uri = config['REDIRECT_URI']

# CSV file path
csv_file = './contacts/contacts.csv'

# Generate the authorization URL
def generate_authorization_url():
    authorize_endpoint = f'{mautic_url}/oauth/v2/authorize'
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': '',
        'state': 'main_import'  # optional
    }
    query_params = urllib.parse.urlencode(params)
    authorization_url = f'{authorize_endpoint}?{query_params}'
    return authorization_url

# Get the authorization code from user input
def get_authorization_code():
    authorization_url = generate_authorization_url()
    print("Please authorize the application by visiting the following URL:")
    print(authorization_url)
    authorization_code = input("Enter the authorization code from the redirect URL: ")
    return authorization_code

# Exchange the authorization code for an access token
def exchange_authorization_code(authorization_code):
    token_endpoint = f'{mautic_url}/oauth/v2/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorization_code,
        'redirect_uri': redirect_uri
    }
    response = requests.post(token_endpoint, data=data)
    response.raise_for_status()
    return response.json().get('access_token')

# Import contacts from CSV

def import_contacts():
    authorization_code = get_authorization_code()
    access_token = exchange_authorization_code(authorization_code)
    contacts_endpoint = f'{mautic_url}/api/contacts/new'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            contact_data = {
                'firstname': row['first_name'],
                'lastname': row['last_name'],
                'email': row['email'],
                'kid': row['kid'],
                'country': row['country'],
                'plan': row['plan'],
                'billing_status': row['billing_status'],
                'creation_date': row['creation_date'],
                'buy_date': row['buy_date'],
                'end_date': row['end_date'],
                'preferred_locale': row['locale'],
                'phone': row['phone_number'],
                'event_lead': row['event_lead']

                # Add other fields as needed
            }
            response = requests.post(contacts_endpoint, json=contact_data, headers=headers)
            response.raise_for_status()
            
            # Retrieve the contact ID from the response
            contact_id = response.json().get('contact')['id']
            
            # Add UTM tags using the specific endpoint
            utm_add_endpoint = f'{mautic_url}/api/contacts/{contact_id}/utm/add'
            utm_data = {
                'utm_source': row['utm_source'],
                'utm_medium': row['utm_medium'],
                'utm_campaign': row['utm_campaign']
            }
            response = requests.post(utm_add_endpoint, json=utm_data, headers=headers)
            response.raise_for_status()

    print('Contacts imported successfully!')

# Run the import
import_contacts()
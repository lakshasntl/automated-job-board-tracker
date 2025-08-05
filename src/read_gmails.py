from google.oauth2.credentials import Credentials
#for loading the OAuth2 tokens
from googleapiclient.discovery import build
#Initializes the Gmail API Client
from email.utils import parsedate_to_datetime
from parser import parse_email 

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
#Defines the minimum permissions used - READONLY ACCESS

def load_credentials(account_label):
    #loads OAuth credentils for specific account, goes through personal, then professional, then umd emails
    token_path = f"credentials/token_{account_label}.json"
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    return creds

def search_job_emails(service, query='subject:("thank you for applying" OR "application received" OR "we received your application" OR "thanks for applying" OR "application confirmation" OR "submission confirmation")'):
    #Core search logic using Gmail API, add to the query line if need to broaden search
    results = service.users().messages().list(userId='me', q=query, maxResults=100).execute()
    messages = results.get('messages', [])
    #Gmail API is returning a list of message metadata (ID ONLY) so that we can identify whats already in the csv and whats not
    email_data = []

    for msg in messages:
        full_message = service.users().messages().get(
            userId='me', id=msg['id'], format='full'
        ).execute()
        #getches the full email meta data (only header and structure)
        parsed = parse_email(full_message)
        #here we use parse_email() in parser.py to process the headers
        #print(parsed)
        email_data.append(parsed)

    return email_data

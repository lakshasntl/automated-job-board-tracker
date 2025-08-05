# src/test_gmail_auth.py

from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow 
#gmail api
import sys

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
#permission scope, app can only read gmail NOT send or delete
BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_PATH = BASE_DIR / 'credentials' / 'credentials.json'
#points to API client credentials information

def authenticate(label: str):
    token_path = BASE_DIR / 'credentials' / f'token_{label}.json'
# The label is either personal, professional, or umd
    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
    creds = flow.run_local_server(port=0)
    
    #loads the OAuth flow with client secrets
    #opens a local browser to pick email and approve permissions

    with open(token_path, 'w') as token:
        token.write(creds.to_json())
        #writes credential information into .json file (token)

    print(f"Token saved for: {label}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/test_gmail_auth.py [personal|professional|umd]")
    else:
        label = sys.argv[1]
        authenticate(label)

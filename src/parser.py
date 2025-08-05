import base64 #GMail API encodes email body parts in this
import re
from email.utils import parsedate_to_datetime

def parse_email(message): 
    """
    this function receives a full gmail message from read_gmails.py
    and returns a cleaned dictionary of structured fields
    """
    # Unique ID from Gmail API to avoide duplicates
    email_id = message['id']

    # Get the subject
    headers = message['payload'].get('headers', [])
    subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), '')

    # Get the sender
    sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), '')

    # Get date
    raw_date = next((h['value'] for h in headers if h['name'].lower() == 'date'), '')
    #All of these extract the Subject, Sender, and Date for the dictionary
    
    try:
        date = parsedate_to_datetime(raw_date).isoformat()
    except Exception:
        date = raw_date
        #converts the date into YYYY-MM-DD format

    # Get a snippet (short preview of the email)
    snippet = message.get('snippet', '')

    # tries to extract and decode the plain text email body - but doesn't work fully
    body = ''
    try:
        parts = message['payload'].get('parts', [])
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                body = base64.urlsafe_b64decode(data).decode('utf-8')
                break
    except Exception:
        pass

    # Try to extract company or position info from subject/snippet/body
    company = extract_company(subject, snippet, body)
       
    return {
       
        
        'email_id': email_id,
        'subject': subject,
        'sender': sender,
        'date': date,
        'snippet': snippet,
        'company': company
    }

def extract_company(subject, snippet, body):
    """
    Infers the company or job title from the email text using regex
    """
    patterns = [
        r'Thank you for applying to ([\w\s&-]+)',
        r'Application Received at ([\w\s&-]+)',
        r'We received your application to ([\w\s&-]+)',
        r'Your application to ([\w\s&-]+)',
        r'from ([\w\s&-]+) about your application'
    ]
    
    combined_text = ' '.join([subject, snippet, body])
    for pattern in patterns:
        match = re.search(pattern, combined_text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ''

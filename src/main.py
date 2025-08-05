# src/main.py

from read_gmails import load_credentials, search_job_emails
from googleapiclient.discovery import build
import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/job_applications.csv")

# Load existing email IDs to avoid duplicates
try:
    existing_df = pd.read_csv(DATA_PATH)
    existing_ids = set(existing_df['email_id'].astype(str))
except FileNotFoundError:
    existing_df = pd.DataFrame()
    existing_ids = set()

def get_emails_for_account(label):
    creds = load_credentials(label)
    service = build('gmail', 'v1', credentials=creds)
    emails = search_job_emails(service)
    for email in emails:
        email['account'] = label
    return emails

if __name__ == "__main__":
    all_emails = []
    for label in ['personal', 'professional', 'umd']:
        print(f" Fetching emails for: {label}")
        emails = get_emails_for_account(label)

        # Only keep new emails
        new_emails = [e for e in emails if e['email_id'] not in existing_ids]
        print(f" Found {len(new_emails)} new emails for: {label}")
        all_emails.extend(new_emails)

    # Append new emails to the existing CSV
    if all_emails:
        new_df = pd.DataFrame(all_emails)
        final_df = pd.concat([existing_df, new_df], ignore_index=True)
        final_df.to_csv(DATA_PATH, index=False)
        print(f" Appended {len(new_df)} new job application emails to {DATA_PATH}")
    else:
        print("⚠️ No new job application emails found.")

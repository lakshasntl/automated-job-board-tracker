# Automated Job Board Tracker
A Python-based tool that reads application confirmation emails across multiple GMail accounts and logs job applications into a centralized CSV file. It uses GMail API, OAuth2, and Python to streamline tracking job applications across your personal, professional, and school email accounts.

---

## Features

- Connects to multiple Gmail accounts via OAuth2
- Searches for job application confirmation emails using Gmail search queries
- Extracts structured fields: subject, sender, date, snippet, and inferred company name
- Deduplicates emails based on Gmail message ID
- Logs new entries to `data/job_applications.csv`

---

## Project Structure
'''bash
automated-job-board-tracker/
│
├── credentials/ # OAuth token files (not tracked)
│ ├── token_personal.json
│ ├── token_professional.json
│ └── token_umd.json
│
├── data/
│ └── job_applications.csv # Centralized log of applications
│
├── src/
│ ├── main.py # Entry point: loads creds, fetches, dedupes, logs
│ ├── parser.py # Extracts structured info from emails
│ ├── read_gmails.py # Gmail API connection and email fetching
│ └── test_gmail_auth.py #Test API connection and email fetching
│
├── .gitignore
└── README.md
'''

##How it works
1. (Explain the step by step process of getting Gmail credentials etc.)
2. 'main.py' runs through each account label ('personal | professional | umd )
    - keep in mind that the user can change the label to something that suits their use, as a umd graduate, thats one of my emails
3. Connects to email through 'read_gmails.py'
4. parses emails using 'parser.py'
    - Searches for subjects including the following:
        1. "thank you for applying"
        2. "application received"
        3. "we received your application"
        4. "thanks for applying"
        5. "submission confirmation"
    - The company name is then extracted using regex to go through the subject, snippet or body of the email
    '''python
    r'Thank you for applying to ([\w\s&-]+)',
        r'Application Received at ([\w\s&-]+)',
        r'We received your application to ([\w\s&-]+)',
        r'Your application to ([\w\s&-]+)',
        r'from ([\w\s&-]+) about your application'
    '''
5. skips duplicates using the email_id component
6. adds any new application emails to job_applications.csv


## Set up instructions
You have to set up a Gmail API access and generate OAuth2 tokens for each email used
1. Set the API access through the Google Cloud Console
2. Create credentails for each account
3. place the tokens in the credentials/ folder
4. run the script
'''bash
python src/main.py
'''
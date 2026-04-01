
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import getpass
import time
import random
import os

# Load the contacts from the CSV file
contacts_file = 'Final_Merged_HR_Contacts.csv'
sent_emails_file = 'sent_emails.csv'

# Parametrize email credentials
sender_email = input("Enter your email address: ")
password = getpass.getpass("Enter your email password: ")
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Parametrize the CV file path
cv_file_path = input("Enter the path to your CV file: ")

# Email content (customize this message as needed)
subject = "Looking for positions in Data Science or Data Engineering"
body_template = f"""
Hi [name],

I hope this email finds you well. I am reaching out to introduce myself and explore potential opportunities in data related fields (Data Science, Data Architecture, Data Engineering or Data Analysis) as a candidate.

Looking forward to hearing from you. (^_^)

(Just in case: attached you'll find my CV/Resume)

Best regards,
Bsc. Ezequiel H. Martinez,
MBA, Msc. in Data Science
"""

# Function to send email
def send_email(to_email, bcc_email, subject, body, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Bcc'] = bcc_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Attach the file
    attachment = MIMEBase('application', 'octet-stream')
    with open(attachment_path, 'rb') as attachment_file:
        attachment.set_payload(attachment_file.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
    msg.attach(attachment)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, [to_email, bcc_email], msg.as_string())
        print(f"Email sent to {to_email} with BCC to {bcc_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False

def main():
    # Load the contacts
    contacts_df = pd.read_csv(contacts_file)

    # Load the list of already sent emails if it exists
    if os.path.exists(sent_emails_file):
        sent_emails_df = pd.read_csv(sent_emails_file)
        sent_emails = set(sent_emails_df['Email'].tolist())
    else:
        sent_emails = set()

    # Filter out already sent emails
    contacts_df['Emails'] = contacts_df['Emails'].apply(lambda x: ', '.join([email for email in x.split(', ') if email not in sent_emails]))

    for index, row in contacts_df.iterrows():
        emails = row['Emails']
        if pd.notna(emails):  # Check if the email address is not NaN
            name = row['First Name'] if pd.notna(row['First Name']) else row['Last Name']
            body = body_template.replace('[name]', name)
            for to_email in emails.split(', '):
                if to_email in sent_emails:
                    continue

                # Preview the email
                print(f"\nPreview:\nTo: {to_email}\nFrom: {sender_email}\nBCC: {sender_email}\nSubject: {subject}\nBody:\n{body}\n")
                action = input("Send email? [y]es/[n]o/[c]ontinue/[a]bort: ").strip().lower()

                if action == 'y':
                    if send_email(to_email, sender_email, subject, body, cv_file_path):
                        sent_emails.add(to_email)
                elif action == 'n':
                    continue
                elif action == 'c':
                    for remaining_index, remaining_row in contacts_df.iterrows():
                        remaining_emails = remaining_row['Emails']
                        remaining_name = remaining_row['First Name'] if pd.notna(remaining_row['First Name']) else remaining_row['Last Name']
                        remaining_body = body_template.replace('[name]', remaining_name)
                        for remaining_to_email in remaining_emails.split(', '):
                            if remaining_to_email not in sent_emails:
                                send_email(remaining_to_email, sender_email, subject, remaining_body, cv_file_path)
                                sent_emails.add(remaining_to_email)
                    break
                elif action == 'a':
                    break
                else:
                    print("Invalid option. Skipping this email.")
                
                if action == 'a':
                    break
            if action == 'a':
                break

            delay = random.uniform(1, 120)
            print(f"Waiting for {delay:.2f} seconds before sending the next email...")
            time.sleep(delay)

    # Save the sent emails to a file
    pd.DataFrame(list(sent_emails), columns=['Email']).to_csv(sent_emails_file, index=False)

if __name__ == "__main__":
    main()

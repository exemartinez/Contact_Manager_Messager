import pandas as pd

# Load the provided CSV file
file_path = 'Final_Merged_HR_Contacts.csv'
contacts_df = pd.read_csv(file_path)

# Rename columns to match Mailchimp's format
contacts_df.rename(columns={
    'First Name': 'FNAME',
    'Last Name': 'LNAME',
    'Emails': 'EMAIL'
}, inplace=True)

# Ensure only necessary columns are included
mailchimp_df = contacts_df[['FNAME', 'LNAME', 'EMAIL']]

# Split emails into separate rows
mailchimp_df = mailchimp_df.set_index(['FNAME', 'LNAME'])['EMAIL'].str.split(', ', expand=True).stack().reset_index(name='EMAIL').drop('level_2', axis=1)

# Save the Mailchimp friendly CSV
mailchimp_file_path = 'Mailchimp_Friendly_Contacts.csv'
mailchimp_df.to_csv(mailchimp_file_path, index=False)

print("Mailchimp friendly CSV file created successfully!")

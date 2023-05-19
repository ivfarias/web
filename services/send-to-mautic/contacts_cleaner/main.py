import os
import csv
import re

# Input and output directories
input_directory = 'inputs'
output_directory = 'outputs'

# Maximum rows per output file
max_rows_per_file = 1000

# Load country dictionary from file
country_dict = {}
with open('country_dict.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        country_dict[row['country_name']] = row['iso_code']

# Clean up and standardize contacts
def clean_contacts(input_file, output_file):
    cleaned_contacts = []
    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            buy_date = row['buy_date']
            end_date = row['end_date']
            creation_date = row['creation_date']
            locale = row['locale']

            
            # Skip the row if it has a buy_date or end_date or creation_date prior to 2023
            if buy_date or end_date or (creation_date and creation_date < '2023') or not locale:
                continue
            
            # Clean up fields: first_name, last_name, phone_number
            first_name = re.sub(r'[^a-zA-Z0-9\s]', '', row['first_name'])
            last_name = re.sub(r'[^a-zA-Z0-9\s]', '', row['last_name'])
            phone_number = re.sub(r'[^0-9]', '', row['phone_number'])
            
            # Update the row with cleaned values
            row['first_name'] = first_name.strip()
            row['last_name'] = last_name.strip()
            row['phone_number'] = phone_number.strip()

            # Standardize the country column using ISO codes
            country_name = row['country']
            country_code = country_dict.get(country_name)
            if country_code:
                row['country'] = country_code
            
            cleaned_contacts.append(row)

    return cleaned_contacts

# Create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Process each input file in the input directory
input_files = os.listdir(input_directory)
for input_file in input_files:
    input_path = os.path.join(input_directory, input_file)
    output_file_base = os.path.splitext(input_file)[0] + '_cleaned'
    output_file_counter = 1
    batch_counter = 1

    # Read and clean contacts from the input file
    contacts = clean_contacts(input_path, None)

    # Split contacts into batches with a maximum number of rows
    contact_batches = [contacts[i:i+max_rows_per_file] for i in range(0, len(contacts), max_rows_per_file)]

    # Write each batch to a separate output file
    for batch in contact_batches:
        output_file = os.path.join(output_directory, f'{output_file_base}_{output_file_counter}.csv')
        with open(output_file, 'w', newline='') as file:
            fieldnames = batch[0].keys() if batch else []
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(batch)

        print(f'Batch {batch_counter} written to {output_file}')

        output_file_counter += 1
        batch_counter += 1

import streamlit as st
import requests

# Set up Streamlit interface
st.title("Automated Google Form Submission")
st.write("Fill in the required details to automatically submit the Google Form multiple times.")

# Input fields for Google Form details
form_url = st.text_input("Enter Google Form URL (response URL)", "https://docs.google.com/forms/d/e/YOUR_FORM_ID/formResponse")
num_responses = st.number_input("Number of responses to submit", min_value=1, max_value=1000, value=10)
entry_ids = st.text_area("Enter each entry ID (one per line)", "entry.123456\nentry.654321")
responses = st.text_area("Enter response for each entry ID (one per line)", "Sample Answer 1\nSample Answer 2")

# Parse entry IDs and responses into a dictionary
entry_ids_list = entry_ids.splitlines()
responses_list = responses.splitlines()

if len(entry_ids_list) != len(responses_list):
    st.error("The number of entry IDs and responses do not match.")
else:
    # Prepare submission data
    submission_data = dict(zip(entry_ids_list, responses_list))

    # Button to trigger the form submission
    if st.button("Submit Form"):
        def submit_form(url, data, count):
            success_count = 0
            for i in range(count):
                # Construct URL with parameters
                params = "&".join([f"{key}={value}" for key, value in data.items()])
                full_url = f"{url}?{params}"
                
                # Send GET request
                response = requests.get(full_url)
                
                if response.status_code == 200:
                    success_count += 1
                    st.write(f"Form submitted successfully: {i + 1}/{count}")
                else:
                    st.error(f"Form submission failed with status: {response.status_code}")
                    break
            return success_count

        # Execute the submission function
        success_count = submit_form(form_url, submission_data, num_responses)
        if success_count > 0:
            st.success(f"Form submitted {success_count} times successfully!")
        else:
            st.error("Form submission failed.")

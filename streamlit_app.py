import streamlit as st
import requests
import os 

# Define the API endpoint
api_url = "https://api.lens.org/patent/search"

# Create a Streamlit app
st.title("Lens.org Patent Search API Visualizer")

# Secret value
secret = os.getenv("API_TOKEN_LENS_ORG")

# Form to capture user input for the API request
with st.form(key='search_form'):
    use_secret_token = st.checkbox("Use secret API token")
    if use_secret_token:
        api_token = secret
        st.write(f"Secret: {secret}")
    else:
        api_token = st.text_input("API Token", type="password")
    
    query = st.text_input("Query", value="title:((solar OR photovoltaic) AND silicon NOT (amorphous OR a-Si)) OR abstract:((solar OR photovoltaic) AND silicon NOT (amorphous OR a-Si)) OR claim:((solar OR photovoltaic) AND silicon NOT (amorphous OR a-Si)) OR description:((solar OR photovoltaic) AND silicon NOT (amorphous OR a-Si)) AND (class_cpc.symbol:(Y02E10\/5*) OR class_cpc.symbol:(H01L31\/*)) AND jurisdiction:US AND publication_type:GRANTED_PATENT AND year_published:[2021 TO 2022]")
    
    submit_button = st.form_submit_button(label='Search')

# When the form is submitted
if submit_button:
    # Make the API request
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'query': query
    }
    response = requests.get(api_url, headers=headers, params=params)

    # Display the response status
    st.write(f"Response Status: {response.status_code}")

    # Check if the response was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Display the raw response
        st.write("Raw Response:", data)

        # Visualize the relevant fields
        st.write("Total Results:", data.get('total', 'N/A'))

        for result in data.get('data', []):
            st.write("Title:", result.get('title', 'N/A'))
            st.write("Abstract:", result.get('abstract', 'N/A'))
            st.write("Publication Date:", result.get('publication_date', 'N/A'))
            st.write("Jurisdiction:", result.get('jurisdiction', 'N/A'))
            st.write("---")
    else:
        st.write("Error:", response.json())

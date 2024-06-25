import streamlit as st
import requests
import json

# Define the API endpoint
api_url = "https://api.lens.org/patent/search"

# Create a Streamlit app
st.title("Lens.org Patent Search API Visualizer")

# Form to capture user input for the API request
with st.form(key='search_form'):
    api_token = st.text_input("API Token", type="password")
    
    # Query parameters
    title = st.text_input("Title")
    abstract = st.text_input("Abstract")
    claim = st.text_input("Claim")
    description = st.text_input("Description")
    
    # Other parameters
    size = st.number_input("Number of Results", min_value=1, max_value=100, value=10)
    sort_options = ["created", "year_published"]
    sort_by = st.selectbox("Sort By", sort_options)
    sort_order = st.selectbox("Sort Order", ["asc", "desc"])
    include_fields = st.multiselect("Include Fields", [
        "biblio.invention_title",
        "legal_status",
        "biblio.priority_claims"
    ])
    
    submit_button = st.form_submit_button(label='Search')

# When the form is submitted
if submit_button:
    # Construct the query payload
    query = {
        "query": {
            "bool": {
                "must": []
            }
        },
        "size": size,
        "from": 0,
        "include": include_fields,
        "sort": [
            {sort_by: sort_order}
        ],
        "exclude": None,
        "scroll": None,
        "scroll_id": None
    }

    # Add query parts if they are provided
    if title:
        query["query"]["bool"]["must"].append({"match": {"title": title}})
    if abstract:
        query["query"]["bool"]["must"].append({"match": {"abstract": abstract}})
    if claim:
        query["query"]["bool"]["must"].append({"match": {"claim": claim}})
    if description:
        query["query"]["bool"]["must"].append({"match": {"description": description}})

    # Make the API request
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(api_url, headers=headers, json=query)

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

        # Button to download results
        json_data = json.dumps(data, indent=4)
        st.download_button(label='Download Results as JSON', data=json_data, file_name='results.json', mime='application/json')
    else:
        st.write("Error:", response.json())

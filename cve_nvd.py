import streamlit as st 
import requests
import json
 

 
def get_cve_data(cve_id):
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId="
    url = f"{base_url}{cve_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        cve_data = response.json()
        return cve_data
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")

# cve_id = "CVE-2021-44228"

# cve_data = json.loads(get_cve_data(cve_id))

# st.json(cve_data)
# print(cve_data)
# print(cve_data['vulnerabilities'])
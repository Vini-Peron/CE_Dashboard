import gspread
import pandas as pd
import streamlit as st


GCP_SERVICE_ACCOUNT = st.secrets["gcp_service_account"]
PRIVATE_SHEET = st.secrets['private_sheet']

@st.cache()
def get_devices_sheet_data():
    gc = gspread.service_account_from_dict(GCP_SERVICE_ACCOUNT)
    sh = gc.open(PRIVATE_SHEET)
    data = sh.sheet1.get_all_values()
    #print(data)
    return data


if __name__ == "__main__":
    st.title("CE Devices Dashboard.")
    raw_sheet_data = get_devices_sheet_data()

    data = pd.DataFrame(raw_sheet_data)
    data.drop(0, axis=0, inplace=True)
    data.columns = ['Order #', "dev_1", "dev_2", "dev_3", "Activate By", "email_address"]

    email_search = st.text_input('Search An Email Address')
    if email_search:
        email_search_res = data[data['email_address'] == email_search]
        if len(email_search_res['Order #']) > 0:
            st.dataframe(email_search_res.drop('Activate By', axis=1))
        else:
            st.write(f'No results for: {str(email_search)}')

    sn_search = st.text_input('Search A Serial Number')
    if sn_search:
        sn_search_res = data[(data["dev_1"] == sn_search) | (data["dev_2"] == sn_search) | (data["dev_3"] == sn_search)]
        if len(sn_search_res['Order #']) > 0:
            st.dataframe(sn_search_res.drop('Activate By', axis=1))
        else:
            st.write(f'No results for: {str(sn_search)}')

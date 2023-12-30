import streamlit as st 
import streamlit.components.v1 as components
from streamlit_card import card
from py_trend import plot_trends
import datetime
import os
from cve_nvd import get_cve_data
from dateutil.relativedelta import relativedelta


# Create folder to cache google trends data csv
os.system('mkdir -p google_trends_csv')

CVE_id = st.text_input("CVE Complete ID") 
if CVE_id == "" :
    CVE_id =  "CVE-2021-44228"
# st.write(CVE_id)
# Get CVE data from NVD
cve_data = get_cve_data(CVE_id)['vulnerabilities'][0]['cve']

# Variables
description = cve_data['descriptions'][0]['value']
#"""Apache Log4j2 2.0-beta9 through 2.15.0 (excluding security releases 2.12.2, 2.12.3, and 2.3.1) JNDI features used in configuration, log messages, and parameters do not protect against attacker controlled LDAP and other JNDI related endpoints. An attacker who can control log messages or log message parameters can execute arbitrary code loaded from LDAP servers when message lookup substitution is enabled. From log4j 2.15.0, this behavior has been disabled by default. From version 2.16.0 (along with 2.12.2, 2.12.3, and 2.3.1), this functionality has been completely removed. Note that this vulnerability is specific to log4j-core and does not affect log4net, log4cxx, or other Apache Logging Services projects."""
cisa_vul_name = cve_data['cisaVulnerabilityName']

#Metrics
CVSS2 = cve_data['metrics']['cvssMetricV2'][0]['cvssData']
try:
    CVSS3 = cve_data['metrics']['cvssMetricV31'][0]['cvssData']
except:
    print(123)
def cvss_Vn(cvssV):
    vector = cvssV['vectorString']
    score = cvssV['baseScore']
    try:
        attack_vector = cvssV['attackVector']
        severity = cvssV['baseSeverity']
    except:
        attack_vector = cvssV['accessVector']
        severity = f"None({score})"
    return vector, attack_vector, score, severity

dater = cve_data['published']
date = dater.split('T')[0]
required_action = cve_data['cisaRequiredAction']
#"""For all affected software assets for which updates exist, the only acceptable remediation actions are: 1) Apply updates; OR 2) remove affected assets from agency networks. Temporary mitigations using one of the measures provided at https://www.cisa.gov/uscert/ed-22-02-apache-log4j-recommended-mitigation-measures are only acceptable until updates are available.""" #cisaRequiredAction
patch_date = cve_data['cisaActionDue']

# Title
components.html(f"""
                <div style="text-align: center; color:Black;">
                <h1>{CVE_id}</h1>
                </div>
                """)

# Description
st.title('Description')
# with st.container(border=True):
#     st.write(description)
st.info(description)

# Metrics
st.title('Metrics')
# st.metric("Date", date, )
tab1, tab2 = st.tabs(["CVSS2", "CVSS3"])

with tab1:
    st.header("CVSS2")
    vector2, attack_vector2, score2, severity2 = cvss_Vn(CVSS2)
    col1, col2 = st.columns(2)
    col1.metric(label='Score', value=score2, delta=None)
    col2.metric(label='Severity', value=severity2, delta=None)
    st.metric(label="Attack Vector", value=attack_vector2, delta=None)
    st.metric(label='vector', value=vector2, delta=None)
    
with tab2:
    st.header("CVSS3")
    vector3, attack_vector3, score3, severity3 = cvss_Vn(CVSS3)
    col1, col2 = st.columns(2)
    col1.metric(label='Score', value=score3, delta=None)
    col2.metric(label='Severity', value=severity3, delta=None)
    st.metric(label="Attack Vector", value=attack_vector3, delta=None)
    st.metric(label='vector', value=vector3, delta=None)
    
# col1 = st.columns(2)


# Google trends
st.title('Google Trends')
min_date = datetime.datetime.strptime(date, "%Y-%m-%d")
max_date = datetime.datetime.now()
default_date = min_date + relativedelta(months=12)

dat1, dat2 = st.columns(2)
date1 = str(dat1.date_input('Start Date',value=min_date, min_value=min_date, max_value=max_date))
date2 = str(dat2.date_input('End Date', value=max_date,min_value=min_date,max_value=max_date))
# st.write(date1,date2)
# st.date_input('Start Date')

plot_trends(CVE_id, date1, date2, patch_date=patch_date)

# Requiered Actions
st.title('Required Actions & Patch')
st.success(required_action)
# st.write(required_action)

# Patch
# st.title('Patch')
# st.write('Patches')

# Weaknesses
# st.text_input('Weaknesses')

import io
import pandas as pd
import numpy as np
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Career Lens - Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Career Lens: Resume Data Analytics & Job Matching")
st.markdown("Analyze resume profiles, filter by job roles and experience requirements, and explore candidate match scores.")

# Built-in dataset embedded directly so no separate CSV file is required
EMBEDDED_CSV_DATA = """career_objective,skills,degree_names,passing_years,educational_results,major_field_of_studies,professional_company_names,start_dates,end_dates,related_skils_in_job,positions,locations,responsibilities,job_position_name,educationaL_requirements,experiencere_requirement,age_requirement,responsibilities.1,skills_required,matched_score
"Big data analytics working and database warehouse manager with robust experience in handling all kinds of data. I have also used multiple cloud infrastructure services and am well acquainted with them.","['Big Data', 'Hadoop', 'Hive', 'Python', 'Mapreduce', 'Spark', 'Java', 'Machine Learning', 'Cloud', 'Hdfs', 'YARN', 'Core Java', 'Data Science', 'C++', 'Data Structures', 'DBMS', 'RDBMS']","['B.Tech']","['2019']","['N/A']","['Electronics']","['Coca-COla']","['Nov 2019']","['Till Date']","[['Big Data']]","['Big Data Analyst']","['N/A']","Technical Support and Troubleshooting","Senior Software Engineer","B.Sc in Computer Science & Engineering from a reputed university","At least 1 year","","Technical Support\nTroubleshooting\nCollaboration","Python\nJava\nBig Data\nSQL",0.850000
"Fresher looking to join as a data analyst and junior data scientist. Experienced in creating meaningful data dashboards and evaluation models.","['Data Analysis', 'Data Analytics', 'Business Analysis', 'R', 'SAS', 'PowerBi', 'Tableau', 'Data Visualization', 'Business Analytics', 'Machine Learning']","['B.Sc (Maths)', 'M.Sc (Science) (Statistics)']","['2015', '2018']","['N/A', 'N/A']","['Mathematics', 'Statistics']","['BIB Consultancy']","['Sep 2019']","['Till Date']","[['Data Analysis', 'Business Analysis', 'Machine Learning']]","['Junior Data Analyst']","['N/A']","Machine Learning Leadership","Machine Learning (ML) Engineer","M.Sc in Computer Science & Engineering or in a relevant field","At least 5 year(s)","","Machine Learning Leadership\nCross-Functional Collaboration","Python\nMachine Learning\nData Analytics",0.750000
"Seeking roles in software development and machine learning applications.","['Software Development', 'Machine Learning', 'Deep Learning', 'Risk Assessment', 'Requirement Gathering', 'Application Support', 'JavaScript', 'Python', 'Docker', 'HTML', 'Hive', 'CSS', 'C', 'C++']","['B.Tech']","['2018']","['N/A']","['Electronics/Telecommunication']","['Axis Bank Limited']","['June 2018']","['Till Date']","[['Unified Payment Interface', 'Risk Prediction']]","['Software Developer']","['N/A']","Trade Marketing and Brand Visibility","Executive/ Senior Executive- Trade Marketing, Hygiene Products","Master of Business Administration (MBA)","At least 3 years","","Trade Marketing Executive\nBrand Visibility","Brand Promotion\nCampaign Management\nField Supervision",0.416667
"To obtain a position in a fast-paced business office environment, demanding a strong organizational, technical, and interpersonal position utilizing my skills and attributes.","['accounts payables', 'accounts receivables', 'Accounts Payable', 'Accounts Receivable', 'administrative functions', 'trial balance', 'banking', 'budget', 'Computer Applications', 'Credit', 'Customer Service', 'Excel', 'QuickBooks', 'Sales']","['Computer Applications Specialist Certificate Program']","['2008']","[None]","['Computer Applications']","['Martinez Business Services']","['January 2011']","['November 2015']","[['accounts receivables', 'banking', 'G/L Accounts']]","['Office Coordinator']","['California']","Apparel Sourcing and Client Relations","Business Development Executive","Bachelor/Honors","1 to 3 years","Age 22 to 30 years","Apparel Sourcing\nQuality Garment Sourcing","Fast typing skill\nOnline research\nClient Communication",0.760000
"Professional accountant with an outstanding work ethic and integrity seeking to make a valuable contribution utilizing strong analytical, organizational, communication, and computer skills.","['Analytical reasoning', 'Compliance testing knowledge', 'Effective time management', 'Public and private accounting', 'accounting', 'accounts payable', 'accounts receivable', 'financial reports', 'tax returns']","['Bachelor of Business Administration']","[None]","['3.84']","['Accounting']","['Kent Financial Group']","['January 2016']","['Current']","[['collections', 'accounts receivable', 'financial reporting']]","['Senior Accountant']","['Ohio']","iOS Lifecycle and Native Frameworks","Senior iOS Engineer","Bachelor of Science (BSc) in Computer Science","At least 4 years","","iOS Lifecycle\nRequirement Analysis\nNative Frameworks","iOS\niOS App Developer\nSwift\nObjective-C",0.650000
"Expertise EDA modeler. I like to learn what my data contains and how well I can model it depending on the problem.","['Data Analysis', 'Business Analysis', 'Machine Learning', 'Regression Analysis', 'Time Series Analysis', 'SQL', 'Python', 'NLP', 'Tableau', 'Statistical Analysis']","['B.CA', 'M.CA']","['2018', '2020']","[None, None]","['Computer Applications']","['Passionate Solution']","['Feb 2020']","['Ongoing']","[['EDA', 'Data Cleaning', 'Data Modeling']]","['Data Modeler']","['Pune']","Hardware & Software Installation","Executive/ Sr. Executive -IT","Bachelor of Science (BSc) in Computer Science","3 to 5 years","Age at most 40 years","Hardware & Software Installation\nSystem Monitoring","Networking\nSystem Administration\nTroubleshooting",0.650000
"Looking for roles related to application development in Machine Learning and Business Analytics.","['Business Analyst', 'Data Analytics', 'Data Cleansing', 'Business Analysis', 'Risk Analysis', 'Statistical Analysis', 'Deep Learning', 'Machine Learning', 'Python', 'Numpy']","['B.BA']","['2019']","['N/A']","['Business Administration']","['ZigSAW']","['Apr 2019']","['Dec 2020']","[['Machine Learning']]","['Business Analyst']","['Mysore']","Mushak Forms Maintenance & VAT Software","Executive - VAT","BBA in Accounting and Finance","1 to 3 years","","Mushak Forms Maintenance\nVAT Software & MS Office","VAT and Tax\nAccounting\nExcel",0.650000
"Energetic, innovative engineering undergraduate, passionate about Machine Learning, NLP and Deep Learning for solving real-world problems.","['Python', 'Machine Learning', 'MySQL', 'Data Mining', 'Deep Learning', 'Data Analysis', 'Computer Vision', 'Flask API', 'Predictive Modeling', 'AWS', 'Scikit-Learn', 'Numpy', 'NLP']","['B.Tech']","['2020']","['N/A']","['Electrical']","['Zynta Labs']","['Apr 2019']","['Nov 2019']","[['NLP', 'Machine Learning', 'Text Analysis']]","['ML Intern']","['Delhi']","Administrative Support and Scheduling","Asst. Manager/ Manger (Administrative)","Bachelor/Honors","At least 5 years","Age at least 28 years","Administrative Support\nScheduling\nFiling & Documentation","Administration\nHealth Safety and Environment",0.650000
"Hard working recent graduate intending a full time job to build experience in a Civil Engineering working environment.","['AutoCAD', 'ETABS', 'Microsoft Office Suite', 'MS Project', 'Civil Engineering', 'Structural Design', 'Project Coordination']","['B.A']","['N/A']","['Cum Laude']","['Organizational Communication Business Management']","['Apex Infrastructure']","['May 2011']","['November 2014']","[['building referral relationships', 'management']]","['Site Coordinator']","['Arizona']","Design Review and Proposal Preparation","Civil Engineer","B.Sc in Civil Engineering from a reputed university","At least 5 years","Age at least 30 years","Design Review\nCoordination\nProposal Preparation","AutoCAD\nETABS\nMicrosoft Office Suite\nMS Project",0.650000
"Passionate Data Engineer with a zeal to excel forward and produce promising outcomes. Hands-on knowledge in various Machine Learning Algorithms.","['Mathematical modelling', 'Machine Learning', 'Predictive Analysis', 'Artificial Intelligence', 'AWS deployment', 'Data gathering', 'Data Mining', 'Python']","['B.Tech']","['2019']","['N/A']","['Computer Science']","['BPM Foundation']","['Jun 2020']","['Ongoing']","[['Data Sampling', 'Data Pipeline']]","['Data Engineer']","['Mumbai']","Data Platform Design & Pipeline Development","Data Engineer","Bachelor of Science (BSc)","5 to 8 years","","Data Platform Design\nData Pipeline Development","Azure\nBig Data\nData Analytics\nETL Tools\nPython",0.683333
"A curiosity-driven data scientist, eager to leverage machine learning and data analytics to extract meaningful insights and solve challenging business problems.","['Data Science', 'Machine Learning', 'Python', 'Big Data', 'SQL', 'PySpark', 'Scala', 'Hive', 'Scikit Learn', 'Pandas', 'Matplotlib', 'NLP', 'Transformers', 'BERT']","['B.Tech', 'M.Tech']","['2017', '2019']","['8.9 CGPA', '9.1 CGPA']","['Computer Science']","['Infosys']","['Jul 2019']","['Till Date']","[['NLP', 'Deep Learning', 'Data Science']]","['Data Scientist']","['Bengaluru']","Model Building and Statistical Analysis","Data Science Engineer","M.Sc / B.Tech in Computer Science or Data Science","2 to 5 years","Age 24 to 35 years","Model Building\nStatistical Analysis\nDeployment","Python\nPyTorch\nTensorFlow\nSQL\nNLP",0.910000
"Experienced backend and cloud engineer skilled in CI/CD pipelines, containerization, and automated infrastructure deployment.","['Docker', 'Kubernetes', 'Jenkins', 'AWS', 'Linux', 'Python', 'Terraform', 'Git', 'CI/CD', 'Bash']","['B.Tech']","['2018']","['8.2 CGPA']","['Information Technology']","['Wipro']","['Aug 2018']","['Till Date']","[['Cloud Infrastructure', 'DevOps']]","['DevOps Engineer']","['Hyderabad']","Cloud Deployment and Server Maintenance","DevOps Engineer","B.Sc / B.Tech in CSE/IT","3 to 5 years","Age 25 to 35 years","CI/CD Automation\nCloud Infrastructure\nMonitoring","Docker\nKubernetes\nAWS\nLinux\nJenkins",0.880000
"""

def preprocess_dataframe(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()
    df.columns = df.columns.str.replace('\ufeff', '', regex=False)

    cols_to_drop = [
        'address', 'educational_institution_name', 'result_types',
        'company_urls', 'extra_curricular_activity_types',
        'extra_curricular_organization_names', 'extra_curricular_organization_links',
        'role_positions', 'online_links', 'languages',
        'proficiency_levels', 'certification_providers',
        'certification_skills', 'issue_dates', 'expiry_dates'
    ]
    df_clean = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')

    if 'experiencere_requirement' in df_clean.columns:
        exp_numbers = df_clean['experiencere_requirement'].astype(str).str.findall(r'\d+')
        df_clean['min_experience'] = pd.to_numeric(exp_numbers.str[0], errors='coerce')
        df_clean['max_experience'] = pd.to_numeric(exp_numbers.str[1], errors='coerce')

    if 'age_requirement' in df_clean.columns:
        age_numbers = df_clean['age_requirement'].astype(str).str.findall(r'\d+')
        df_clean['min_age'] = pd.to_numeric(age_numbers.str[0], errors='coerce')
        df_clean['max_age'] = pd.to_numeric(age_numbers.str[1], errors='coerce')

    return df_clean

@st.cache_data
def load_embedded_data() -> pd.DataFrame:
    raw_df = pd.read_csv(io.StringIO(EMBEDDED_CSV_DATA))
    return preprocess_dataframe(raw_df)

# Sidebar: Optional CSV upload (falls back automatically to embedded dataset)
st.sidebar.header("📂 Data Source")
uploaded_file = st.sidebar.file_uploader("Upload full resume_data.csv (Optional)", type=["csv"])

if uploaded_file is not None:
    df = preprocess_dataframe(pd.read_csv(uploaded_file))
    st.sidebar.success("Loaded uploaded CSV file!")
else:
    df = load_embedded_data()
    st.sidebar.info("Using built-in sample dataset (no external CSV needed).")

# Sidebar Filters
st.sidebar.header("🔍 Filter Candidates")

job_positions = ['All'] + sorted(df['job_position_name'].dropna().unique().tolist())
selected_job = st.sidebar.selectbox("Job Position Name", job_positions)

skill_query = st.sidebar.text_input("Search Skill (e.g., Python, SQL, AutoCAD)")

if 'matched_score' in df.columns:
    min_score, max_score = float(df['matched_score'].min()), float(df['matched_score'].max())
    if min_score < max_score:
        score_range = st.sidebar.slider("Matched Score Range", min_score, max_score, (min_score, max_score))
    else:
        score_range = (min_score, max_score)
else:
    score_range = (0.0, 1.0)

# Apply filters
filtered_df = df.copy()
if 'matched_score' in filtered_df.columns:
    filtered_df = filtered_df[
        (filtered_df['matched_score'] >= score_range[0]) &
        (filtered_df['matched_score'] <= score_range[1])
    ]

if selected_job != 'All':
    filtered_df = filtered_df[filtered_df['job_position_name'] == selected_job]

if skill_query.strip():
    filtered_df = filtered_df[
        filtered_df['skills'].astype(str).str.contains(skill_query.strip(), case=False, na=False)
    ]

# Top Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Resumes", len(df))
with col2:
    st.metric("Filtered Matches", len(filtered_df))
with col3:
    avg_score = filtered_df['matched_score'].mean() if len(filtered_df) > 0 and 'matched_score' in filtered_df.columns else 0.0
    st.metric("Average Match Score", f"{avg_score:.2f}")

# Dashboard Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Filtered Candidates", "📊 Dataset Overview", "📈 Analytics & Charts"])

with tab1:
    st.subheader(f"Matching Candidate Profiles ({len(filtered_df)})")
    st.dataframe(filtered_df, use_container_width=True)

    csv_export = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Filtered Results (CSV)",
        data=csv_export,
        file_name="filtered_resumes.csv",
        mime="text/csv"
    )

with tab2:
    st.subheader("Full Dataset Preview")
    st.dataframe(df, use_container_width=True)

with tab3:
    st.subheader("Matched Score Statistics")
    if 'matched_score' in df.columns:
        st.write(df['matched_score'].describe())

    st.subheader("Candidates by Job Position")
    if 'job_position_name' in df.columns:
        st.bar_chart(df['job_position_name'].value_counts())

import pandas as pd
import streamlit as st
import boto3
import io
from streamlit_option_menu import option_menu
import Job  # Import the Job12 module


# Load the Excel file into a pandas DataFrame
aws_id = 'AKIA4T5JWBQCSPOKA6MX'
aws_secret = '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'
bucket_name = 'vsdatateam'
object_key = 'College.xlsx'

s3 = boto3.client('s3', aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
obj = s3.get_object(Bucket=bucket_name, Key=object_key)
data = obj['Body'].read()
df = pd.read_excel(io.BytesIO(data))
#df = pd.read_excel(r"C:\Users\spjay\Desktop\VigyanShaala\GUI CLG\AWS Final\College.xlsx")
df.head()

# Define the Streamlit interface
def main():
    st.title('Student Progress Report')

    # Initialize 'student_name' in session state if it's not already done
    if 'student_name' not in st.session_state:
        st.session_state['student_name'] = ''

    # Use user input to update the 'student_name' in session state
    st.session_state.student_name = st.text_input('**Enter student name**', value=st.session_state.student_name)

    # Check if 'student_name' is empty and display a warning
    if st.session_state.student_name == '':
        st.warning('*Please enter a valid name.*')

    st.session_state.qualified_degrees = sorted([i for i in df['Degree'].unique() if isinstance(i, str)])
    st.session_state.selected_degree = st.selectbox('**Select spiring degree (You want to study in the future)**', st.session_state.qualified_degrees)

    st.session_state.filtered_fields = sorted([i for i in df[df['Degree'] == st.session_state.selected_degree]['Field'].unique() if isinstance(i, str)])
    st.session_state.selected_field = st.selectbox('**Select field**', st.session_state.filtered_fields)

    st.session_state.filtered_subfields = sorted([i for i in df[(df['Degree'] == st.session_state.selected_degree) & (df['Field'] == st.session_state.selected_field)]['SubField'].unique() if isinstance(i, str)])
    st.session_state.selected_subfield = st.selectbox('**Select subfield**', st.session_state.filtered_subfields)

    st.session_state.filtered_colleges = sorted([i for i in df[(df['Degree'] == st.session_state.selected_degree) & (df['Field'] == st.session_state.selected_field) & (df['SubField'] == st.session_state.selected_subfield)]['COLLEGE'].unique() if isinstance(i, str)])
    st.session_state.selected_college = st.selectbox('**Select college**', st.session_state.filtered_colleges)

    if st.session_state.selected_college:
        st.session_state.college_details = df[(df['Degree'] == st.session_state.selected_degree) &
                              (df['Field'] == st.session_state.selected_field) &
                              (df['SubField'] == st.session_state.selected_subfield) &
                              (df['COLLEGE'] == st.session_state.selected_college)]

        st.header('**College Details**')
        st.markdown(f"**College:** {st.session_state.selected_college}")
        st.markdown(f"**Duration:** {st.session_state.college_details['DURATION'].values[0]}")
        st.markdown(f"**College Fee:** {st.session_state.college_details['COLLEGE FEE'].values[0]}")
        st.markdown(f"**NIRF and Other Rank (2022):** {st.session_state.college_details['NIRF AND OTHER RANK(2022)'].values[0]}")
        st.markdown(f"**Minimum Marks for Eligibility:** {st.session_state.college_details['MIN MARKS FOR ELIGIBILITY'].values[0]}")
        st.markdown(f"**Entrance Name and Duration:** {st.session_state.college_details['ENTRANCE NAME AND DURATION'].values[0]}")
        st.markdown(f"**Exam Details:** {st.session_state.college_details['EXAM DETAILS'].values[0]}")
        st.markdown(f"**Test Date:** {st.session_state.college_details['TEST DATE'].values[0]}")
        st.markdown(f"**Application Process:** {st.session_state.college_details['APPLICATION PROCESS'].values[0]}")
        st.markdown(f"**Application Fee:** {st.session_state.college_details['APPLICATION FEE'].values[0]}")
        st.markdown(f"**Selection Process:** {st.session_state.college_details['SELECTION PROCESS'].values[0]}")
        st.markdown(f"**Intake:** {st.session_state.college_details['INTAKE'].values[0]}")
        st.markdown(f"**Link:** {st.session_state.college_details['LINK'].values[0]}")
        st.markdown(f"**Scholarships/Fellowships:** {st.session_state.college_details['Scholarships/Fellowships'].values[0]}")

    if st.button('Next Page'):
        # Set a session state variable to indicate that the next page should be displayed
        st.session_state.next_page = True
        # Rerun the script
        st.experimental_rerun()

# Check if the next page should be displayed
if 'next_page' in st.session_state and st.session_state.next_page:
    # Display the Job12.py page
    Job.main()
else:
    # Display the Home.py page
    main()

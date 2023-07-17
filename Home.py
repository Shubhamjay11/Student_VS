import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import Job12  # Import the Job12 module

# Move the call to st.set_page_config to the beginning of the script
st.set_page_config(layout="wide")

# Load the Excel file into a pandas DataFrame
df = pd.read_excel(r"C:\Users\spjay\Desktop\VigyanShaala\GUI CLG\Final Data\Rode Map.xlsx")
df.head()

# Define the Streamlit interface
def main():
    st.title('Student Progress Report')

    st.session_state.student_name = st.text_input('Enter student name')
    if st.session_state.student_name == '':
        st.warning('Please enter a valid name.')

    st.session_state.qualified_degrees = sorted([i for i in df['Degree'].unique() if isinstance(i, str)])
    st.session_state.selected_degree = st.selectbox('Select qualified degree', st.session_state.qualified_degrees)

    st.session_state.filtered_fields = sorted([i for i in df[df['Degree'] == st.session_state.selected_degree]['Field'].unique() if isinstance(i, str)])
    st.session_state.selected_field = st.selectbox('Select field', st.session_state.filtered_fields)

    st.session_state.filtered_subfields = sorted([i for i in df[(df['Degree'] == st.session_state.selected_degree) & (df['Field'] == st.session_state.selected_field)]['SubField'].unique() if isinstance(i, str)])
    st.session_state.selected_subfield = st.selectbox('Select subfield', st.session_state.filtered_subfields)

    st.session_state.filtered_colleges = sorted([i for i in df[(df['Degree'] == st.session_state.selected_degree) & (df['Field'] == st.session_state.selected_field) & (df['SubField'] == st.session_state.selected_subfield)]['COLLEGE'].unique() if isinstance(i, str)])
    st.session_state.selected_college = st.selectbox('Select college', st.session_state.filtered_colleges)

    if st.session_state.selected_college:
        st.session_state.college_details = df[(df['Degree'] == st.session_state.selected_degree) &
                              (df['Field'] == st.session_state.selected_field) &
                              (df['SubField'] == st.session_state.selected_subfield) &
                              (df['COLLEGE'] == st.session_state.selected_college)]

        st.header('College Details')
        st.write(f"College: {st.session_state.selected_college}")
        st.write(f"Duration: {st.session_state.college_details['DURATION'].values[0]}")
        st.write(f"College Fee: {st.session_state.college_details['COLLEGE FEE'].values[0]}")
        st.write(f"NIRF and Other Rank (2022): {st.session_state.college_details['NIRF AND OTHER RANK(2022)'].values[0]}")
        st.write(f"Minimum Marks for Eligibility: {st.session_state.college_details['MIN MARKS FOR ELIGIBILITY'].values[0]}")
        st.write(f"Entrance Name and Duration: {st.session_state.college_details['ENTRANCE NAME AND DURATION'].values[0]}")
        st.write(f"Exam Details: {st.session_state.college_details['EXAM DETAILS'].values[0]}")
        st.write(f"Test Date: {st.session_state.college_details['TEST DATE'].values[0]}")
        st.write(f"Application Process: {st.session_state.college_details['APPLICATION PROCESS'].values[0]}")
        st.write(f"Application Fee: {st.session_state.college_details['APPLICATION FEE'].values[0]}")
        st.write(f"Selection Process: {st.session_state.college_details['SELECTION PROCESS'].values[0]}")
        st.write(f"Intake: {st.session_state.college_details['INTAKE'].values[0]}")
        st.write(f"Link: {st.session_state.college_details['LINK'].values[0]}")

    if st.button('Next Page'):
        # Set a session state variable to indicate that the next page should be displayed
        st.session_state.next_page = True
        # Rerun the script
        st.experimental_rerun()

# Check if the next page should be displayed
if 'next_page' in st.session_state and st.session_state.next_page:
    # Display the Job12.py page
    Job12.main()
else:
    # Display the Home.py page
    main()
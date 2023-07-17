import pandas as pd
import streamlit as st
from fpdf import FPDF
from fpdf import FPDF, HTMLMixin
import base64
import tempfile
from PIL import Image


class PDF(FPDF,HTMLMixin):
    def __init__(self, width, height):
        super().__init__('P', 'mm', (width, height))
        self.width = width
        self.height = height

    def header(self):
        # Load the original image
        bg_image = Image.open("assets/Watermark.png")

        # Set the background image as the page background
        temp_bg_file = tempfile.mktemp(suffix=".png")
        bg_image.save(temp_bg_file, format="PNG")
        self.image(temp_bg_file, x=50, y=50, w=self.width/2, h=self.height/2)

        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'VigyanShaala International Report', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')

    def chapter_body(self, content):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, content)
        self.ln()

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

# Load the Excel file into a pandas DataFrame
dp = pd.read_excel(r"C:\Users\spjay\Desktop\VigyanShaala\GUI CLG\Final Data\Final NCS.xlsx")
dp.head()

@st.cache_resource
def load_job_details(selected_field):
    filtered_job_titles = dp[dp['Field'] == selected_field]['Job Titles'].unique()
    return filtered_job_titles

def main():
    st.title('Job Details Report')

    selected_field = st.session_state.selected_field
    filtered_job_titles = load_job_details(selected_field)

    if len(filtered_job_titles) == 0:
        st.error(f"No job titles found for the selected field: {selected_field}")
        st.write("Please choose a different field and job title below:")

        fields = sorted(list(dp['Field'].unique()))  # Sort the fields
        fields.insert(0, 'Select a field')  # Add a default option

        selected_field = st.selectbox('Select Field', fields)
        if selected_field == 'Select a field':
            st.warning("Please select a field.")
            return

        st.session_state.selected_field = selected_field

        filtered_job_titles = load_job_details(selected_field)
        
        # Use len() to check if the array is empty
        if len(filtered_job_titles) == 0:
            filtered_job_titles = ['Select a job title']  # Add a default option
        else:
            filtered_job_titles = sorted(filtered_job_titles)  # Sort the job titles

        selected_job_title = st.selectbox('Select Job Title', filtered_job_titles)
    else:
        selected_job_title = st.selectbox('Select Job Title', sorted(filtered_job_titles))  # Sort the job titles

    if selected_job_title:
        job_details = dp[(dp['Field'] == selected_field) & (dp['Job Titles'] == selected_job_title)]

        st.header('Job Details')
        st.write(f"Field: {selected_field}")
        st.write(f"Job Title: {selected_job_title}")
        st.write(f"SubField: {job_details['SubField'].values[0]}")
        st.write(f"Job Description: {job_details['Job Description'].values[0]}")
        st.write(f"Work Environment: {job_details['Work Environment'].values[0]}")
        st.write(f"Key Competancy: {job_details['Key Competancy'].values[0]}")
        st.write(f"Available Skill Training Schemes: {job_details['Available skill training schemes'].values[0]}")
        st.write(f"Sample Training & Courses: {job_details['Sample training & courses'].values[0]}")
        st.write(f"Career Path Progression: {job_details['Career path progression'].values[0]}")
        st.write(f"Probable Employers: {job_details['Probable Employers'].values[0]}")

        # Create a PDF object
        pdf = PDF(210, 297)
        # Add a page
        pdf.add_page()

        # Set font
        pdf.set_font("Arial", size=12)


        # Add title
        pdf.cell(200, 15, txt="College Details Report", ln=True, align="C")

        # Add content
        college_content = [
            f"Student Name: {st.session_state.student_name}",
            f"Qualified Degree: {st.session_state.selected_degree}",
            f"Field: {st.session_state.selected_field}",
            f"Subfield: {st.session_state.selected_subfield}",
            f"College: {st.session_state.selected_college}",
            f"Duration: {st.session_state.college_details['DURATION'].values[0]}",
            f"College Fee: {st.session_state.college_details['COLLEGE FEE'].values[0]}",
            f"NIRF and Other Rank (2022): {st.session_state.college_details['NIRF AND OTHER RANK(2022)'].values[0]}",
            f"Minimum Marks for Eligibility: {st.session_state.college_details['MIN MARKS FOR ELIGIBILITY'].values[0]}",
            f"Entrance Name and Duration: {st.session_state.college_details['ENTRANCE NAME AND DURATION'].values[0]}",
            f"Exam Details: {st.session_state.college_details['EXAM DETAILS'].values[0]}",
            f"Test Date: {st.session_state.college_details['TEST DATE'].values[0]}",
            f"Application Process: {st.session_state.college_details['APPLICATION PROCESS'].values[0]}",
            f"Application Fee: {st.session_state.college_details['APPLICATION FEE'].values[0]}",
            f"Selection Process: {st.session_state.college_details['SELECTION PROCESS'].values[0]}",
            f"Intake: {st.session_state.college_details['INTAKE'].values[0]}",
            f"Link: {st.session_state.college_details['LINK'].values[0]}"
        ]

        # Add college content to the PDF
        for line in college_content:
            # Replace non-latin-1 characters
            line_cleaned = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, txt=line_cleaned)


        # Add title
        pdf.cell(200, 15, txt="Job Details Report", ln=True, align="C")

        # Add content
        job_content = [
            f"Job Title: {selected_job_title}",
            f"Job Description: {job_details['Job Description'].values[0]}",
            f"Work Environment: {job_details['Work Environment'].values[0]}",
            f"Key Competancy: {job_details['Key Competancy'].values[0]}",
            f"Available Skill Training Schemes: {job_details['Available skill training schemes'].values[0]}",
            f"Sample Training & Courses: {job_details['Sample training & courses'].values[0]}",
            f"Career Path Progression: {job_details['Career path progression'].values[0]}",
            f"Probable Employers: {job_details['Probable Employers'].values[0]}",
        ]


        # Add job content to the PDF
        for line in job_content:
            # Replace non-latin-1 characters
            line_cleaned = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, txt=line_cleaned)

        # Save the pdf with name .pdf
        pdf_output = pdf.output(dest="S").encode("latin1")

    st.download_button(
        label="Download PDF",
        data=pdf_output,
        file_name=f"{st.session_state.student_name}_progress_report.pdf",
        mime="application/pdf",
    )

    if st.button('Back'):
        st.session_state.next_page = False
        st.experimental_rerun()

if __name__ == '__main__':
    main()



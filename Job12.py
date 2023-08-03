import pandas as pd
import boto3
import streamlit as st
from fpdf import FPDF
from fpdf import FPDF, HTMLMixin
import base64
import tempfile
from PIL import Image

s3 = boto3.client('s3')
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='AKIA4T5JWBQCSPOKA6MX',
    aws_secret_access_key='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'
)

import io




class PDF(FPDF,HTMLMixin):
    def __init__(self, width, height):
        super().__init__('P', 'mm', (width, height))
        self.width = width
        self.height = height

    def header(self):
        # Load the original image
        bg_image = Image.open("assets/Watermark.jpeg")

        # Set the background image as the page background
        temp_bg_file = tempfile.mktemp(suffix=".jpeg")
        bg_image.save(temp_bg_file, format="JPEG")
        self.image(temp_bg_file, x=50, y=50, w=self.width/2, h=self.height/2)

        # Load the logo
        logo = Image.open("assets/logo.jpeg")

        # Save the logo to a temporary file
        temp_logo_file = tempfile.mktemp(suffix=".jpeg")
        logo.save(temp_logo_file, format="JPEG")
        
        # Define logo size
        logo_width = 26  # You can adjust the size as you need
        logo_height = 20  # You can adjust the size as you need

        # Add the logo on the top right corner
        self.image(temp_logo_file, x = self.width - logo_width - 10, y = 10, w = logo_width, h = logo_height)

        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Career Exploration Report', 0, 1, 'C')
        self.cell(0, 10, '', 0, 1, 'C')
      

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')

    def chapter_body(self, content):
        self.set_font('Arial', '', 12)
        line_height = 5  # Set the desired interline spacing
        lines = content.split('\n')
        for line in lines:
            if ":" in line:
                # If the line contains a colon (":"), consider it as a content header and display it in bold
                parts = line.split(":")
                self.set_font('Arial', 'B', 12)
                self.cell(0, line_height, txt=parts[0] + ":", ln=False)
                self.set_font('Arial', '', 12)
                self.cell(0, line_height, txt=parts[1], ln=True)
            else:
                self.cell(0, line_height, txt=line, ln=True)
        self.ln()

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

    def add_bold_text(self, text):
        self.set_font('Arial', 'B', 12)
        line_height = 5  # Set the desired interline spacing
        lines = text.split('\n')
        for line in lines:
            self.cell(0, line_height, txt=line, ln=True)
        self.ln()  # Add a line after each detail
        self.set_font('Arial', '', 12)  # Set the font back to normal for the next line
        
    def add_scholarship_table(self, data):
        # Set column names for the table
        column_names = ['Scholarship Name']

        # Set column widths
        col_widths = [100]

        # Set font for table header
        self.set_font('Arial', 'B', 12)

        # Add table header
        for name, width in zip(column_names, col_widths):
            self.cell(width, 10, str(name), 1, 0, 'C')
        self.ln()

        # Set font for table content
        self.set_font('Arial', '', 10)  # Reduce font size to fit the content

        # Add table content
        for row in data:
            for item, width in zip(row, col_widths):
                self.cell(width, 8, str(item).encode('latin-1', 'replace').decode('latin-1'), 1, 0, 'C')
            self.ln()

    def add_scholarship_offered_by_table(self, data):
        column_names = ['Offered by', 'Govt./Private', 'For study in']
        col_widths = [60, 40, 60]

        self.set_font('Arial', 'B', 12)

        for name, width in zip(column_names, col_widths):
            self.cell(width, 10, str(name), 1, 0, 'C')
        self.ln()

        self.set_font('Arial', '', 10)

        for row in data:
            for item, width in zip(row, col_widths):
                self.cell(width, 8, str(item).encode('latin-1', 'replace').decode('latin-1'), 1, 0, 'C')
            self.ln()

    def add_scholarship_duration_table(self, data):
        column_names = ['Duration', 'Award amount', 'Application deadline']
        col_widths = [50, 50, 50]

        self.set_font('Arial', 'B', 12)

        for name, width in zip(column_names, col_widths):
            self.cell(width, 10, str(name), 1, 0, 'C')
        self.ln()

        self.set_font('Arial', '', 10)

        for row in data:
            for item, width in zip(row, col_widths):
                self.cell(width, 8, str(item).encode('latin-1', 'replace').decode('latin-1'), 1, 0, 'C')
            self.ln()
            
    def add_scholarship_details(self, scholarship_name, details):
        # Set font for scholarship details content
        self.set_font('Arial', '', 12)

        # Loop through scholarship details and add them to the PDF
        for key, value in details.items():
            # Convert the key and value to strings using 'utf-8' encoding
            key_str = str(key).encode('latin-1', 'replace').decode('latin-1')
            value_str = str(value).encode('latin-1', 'replace').decode('latin-1')

            # Concatenate the key and value
            content = f"{key_str}: {value_str}"

            # Find the index of ':' to make it bold
            separator_index = content.index(':')

            # Set font to bold for the ':' (content separator)
            self.set_font('Arial', 'B', 12)
            self.cell(self.get_string_width(content[:separator_index]), 8, content[:separator_index], ln=False)

            # Reset font back to normal for the value
            self.set_font('Arial', '', 12)
            #self.cell(0, 8, content[separator_index:], ln=True)

            # Calculate available width for the value
            value_width = self.w - self.get_string_width(content[:separator_index]) - self.r_margin - self.l_margin

             # Check if the value is a contact website (assuming it contains "http")
            if "http" in value:
            # Set the text color to blue
                self.set_text_color(0, 0, 255)
            
            # Check if the value fits within the available width
                if self.get_string_width(content[separator_index:]) <= value_width:
                    self.cell(0, 8, content[separator_index:], ln=True)
                else:
                # If the value does not fit, use multi_cell to wrap it
                    self.multi_cell(0, 8, content[separator_index:], align='L')

            # Reset text color back to black
                self.set_text_color(0, 0, 0)
            else:
            # If it's not a contact website, display normally
                if self.get_string_width(content[separator_index:]) <= value_width:
                    self.cell(0, 8, content[separator_index:], ln=True)
                else:
                # If the value does not fit, use multi_cell to wrap it
                    self.multi_cell(0, 8, content[separator_index:], align='L')

        self.ln()

        # Reset font back to normal
        self.set_font('Arial', '', 12)
        

def add_detail(self, detail, separator="\n"):
    # Split into column name and value
    column_name, value = detail.split(": ", 1)

    # Print column name
    self.set_font('Arial', 'B', 12)
    self.cell(70, 10, txt=column_name + ":", ln=0)

    # Calculate value position
    value_x = self.get_x() + 1

    # Print value
    self.set_font('Arial', '', 12)
    value_width = self.w - value_x - self.r_margin
    self.set_x(value_x)

    # Check for URL and set color
    if "http" in value:
        self.set_text_color(0, 0, 255)

    self.multi_cell(value_width, 7, txt=value, align='L')  # Adjust line_height to reduce interline spacing

    # Reset text color
    self.set_text_color(0, 0, 0)

    # Add the custom separator after each detail
    self.set_font('Arial', '', 5)  # Adjust font size for the separator
    self.cell(0, 2, separator, ln=True)

    
# Load the Excel file into a pandas DataFrame
#dp = pd.read_excel(r"C:\Users\spjay\Desktop\VigyanShaala\GUI CLG\Final Data\Job Final.xlsx")
#dp.head()

obj = s3.Bucket('vsdatateamtest1').Object('Job.xlsx').get()
dp = pd.read_excel(io.BytesIO(obj['Body'].read()), index_col=0)

@st.cache_resource
def load_job_details(selected_field):
    filtered_job_titles = dp[dp['Field'] == selected_field]['Job Titles'].unique()
    return filtered_job_titles


def clean_text(text):
    try:
        return text.encode('latin-1', 'replace').decode('latin-1')
    except UnicodeEncodeError:
        return "[Non-Latin-1 Character]"

def main():
    st.title('Job Details Report')

    selected_field = st.session_state.selected_field
    filtered_job_titles = load_job_details(selected_field)

    if len(filtered_job_titles) == 0:
        st.error(f"No job titles found for the selected field: {selected_field}")
        st.error("Please choose a different field and job title below:")

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
        st.markdown(f"**Field:** {selected_field}")
        st.markdown(f"**Job Title:** {selected_job_title}")
        st.markdown(f"**SubField:** {job_details['SubField'].values[0]}")
        st.markdown(f"**Job Description:** {job_details['Job Description'].values[0]}")
        st.markdown(f"**Work Environment:** {job_details['Work Environment'].values[0]}")
        st.markdown(f"**Key Competancy:** {job_details['Key Competancy'].values[0]}")
        st.markdown(f"**Available Skill Training Schemes:** {job_details['Available skill training schemes'].values[0]}")
        st.markdown(f"**Sample Training & Courses:** {job_details['Sample training & courses'].values[0]}")
        st.markdown(f"**Career Path Progression:** {job_details['Career path progression'].values[0]}")
        st.markdown(f"**Probable Employers:** {job_details['Probable Employers'].values[0]}")

        # Load the data from Excel into a DataFrame
        #df = pd.read_excel(r"C:\Users\spjay\Desktop\VigyanShaala\GUI CLG\Final Data\Scholarship Final.xlsx")
        obj = s3.Bucket('vsdatateamtest1').Object('Scholarship.xlsx').get()
        df = pd.read_excel(io.BytesIO(obj['Body'].read()), index_col=0)

        # Filter the DataFrame to only include rows where Field is 'Science'
        df_science = df[df['Field'] == 'Science']

        # Filter the DataFrame for the selected field
        df_selected = df[df['Field'] == selected_field]

        # Create a PDF object
        pdf = PDF(210, 297)
        # Add a page
        pdf.add_page()
        pdf.set_left_margin(20)  # Adjust the left margin (default is 10 mm)
        pdf.set_right_margin(20)  

        # Set font 
        pdf.set_font("Arial", "B", 14)

        # Add title
        pdf.cell(200, 10, txt="College Details Report", ln=True, align="C")

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
            add_detail(pdf, line_cleaned)

         # Set font 
        pdf.set_font("Arial", "B", 14)

        # Add title
        pdf.cell(200, 10, txt="Job Details Report", ln=True, align="C")

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
            add_detail(pdf, line_cleaned)
            
        # Set font for the "Scholarship Details" section to bold
        pdf.set_font("Arial", "B", 14)

        # Add a cell
        pdf.cell(200, 10, txt = "Scholarship Details Report", ln = True, align = 'C')
   
        # Set font for the scholarship details content
        pdf.set_font("Arial", "", 12)
        
        # Group scholarship details by 'Scholarship Name' and loop through each group
        grouped_scholarships = df_science.groupby('Scholarship Name')
        bullet_counter = 1  # Initialize the bullet counter
        
        for scholarship_name, scholarship_group in grouped_scholarships:
            # Add scholarship name with bullet point to the PDF
            pdf.cell(5, 8, txt=f"{bullet_counter}.", ln=False)
            pdf.add_bold_text(f"Scholarship Name: {scholarship_name}")
        
            # Add scholarship tables to the PDF
            pdf.add_scholarship_offered_by_table(scholarship_group[['Offered by', 'Govt./Private', 'For study in']].values)
            pdf.add_scholarship_duration_table(scholarship_group[['Duration', 'Award amount', 'Application deadline']].values)
            
            # Create a dictionary with scholarship details for printing
            scholarship_details = scholarship_group.iloc[0].to_dict()            
            scholarship_details.pop('Degree', None)
            scholarship_details.pop('Field', None)
            scholarship_details.pop('Subfield', None)
            scholarship_details.pop('Scholarship Name', None)
            scholarship_details.pop('Offered by', None)
            scholarship_details.pop('Govt./Private', None)
            scholarship_details.pop('For study in', None)
            scholarship_details.pop('Duration', None)
            scholarship_details.pop('Award amount', None)
            scholarship_details.pop('Application deadline', None)

    # Add scholarship details to the PDF
            pdf.add_scholarship_details(scholarship_name, scholarship_details)

        # Additional space after scholarship details
            pdf.ln()
        
        # Increment the bullet counter for the next scholarship
            bullet_counter += 1
       
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

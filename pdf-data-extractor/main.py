import os
import glob
import re
import pandas as pd
import xlsxwriter
import openpyxl
import pdfplumber

class PDFParser:
    def __init__(self, folder_path):
        self.folder_path = folder_path


    def parse_folder(self, output_format, output_folder):
        # Get a list of PDF files in the folder
        pdf_files = glob.glob(os.path.join(self.folder_path, '*.pdf'))

        # Initialize an empty dictionary to store the data
        data = {}

        # Process each PDF file in the folder
        for pdf_file in pdf_files:
            file_path = os.path.join(self.folder_path, pdf_file)
            file_data = self.extract_data(file_path)
            if file_data:
                data.update(file_data)

        output = self.generate_output(data, output_format, output_folder)

        return output

    # ...

    def extract_data(self, file_path):
        # Open the PDF file
        data = {}
        with pdfplumber.open(file_path) as pdf:
            # Extract text from all pages
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            text = text.replace('\n', '')

            # Extract employee code and amount
            regex = r"Tax amounting to R(\d+\.\d{2})"
            matches = re.findall(regex, text, re.DOTALL | re.MULTILINE)
            
            if matches:
                data[matches[-1]] = matches[-1]
        print(data)     
        return data
            
    def generate_output(self, data, output_format, output_folder):
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Generate output based on the specified format
        if output_format == 'html':
            return self._generate_html_output(data)
        elif output_format == 'csv':
            return self._generate_csv_output(data)
        elif output_format == 'json':
            return self._generate_json_output(data)
        elif output_format == 'excel':
            return self._generate_excel_output(data, output_folder)
        else:
            return 'Invalid output format specified.'

    def _generate_html_output(self, data):
        # Generate HTML output using pandas DataFrame
        df = pd.DataFrame.from_dict(data, orient='index', columns=['Amount'])
        df.index.name = 'Employee Code'
        return df.to_html()

    def _generate_csv_output(self, data):
        # Generate CSV output using pandas DataFrame
        df = pd.DataFrame.from_dict(data, orient='index', columns=['Amount'])
        df.index.name = 'Employee Code'
        return df.to_csv()

    def _generate_json_output(self, data):
        # Generate JSON output using pandas DataFrame
        df = pd.DataFrame.from_dict(data, orient='index', columns=['Amount'])
        df.index.name = 'Employee Code'
        return df.to_json(orient='index')

    def _generate_excel_output(self, data, output_folder):
        import datetime
        # Generate Excel output using pandas DataFrame
        current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"output_{current_datetime}.xlsx"
        file_path = os.path.join(output_folder, file_name)

        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            df = pd.DataFrame.from_dict(data, orient='index', columns=['Amount'])
            df.index.name = 'Employee Code'
            df.to_excel(writer, sheet_name='Sheet1')

        return file_path

def test_client(folder='../test-files', format='excel', output_folder='../output-folder'):
    parser = PDFParser(folder)
    results = parser.parse_folder(format, output_folder)
   
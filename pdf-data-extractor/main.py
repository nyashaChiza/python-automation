import os
import glob
import re
import pandas as pd
import xlsxwriter
import openpyxl
import pdfplumber

class PDFParser:
    """
    A class for parsing PDF files in a folder and generating output in different formats.
    """

    def __init__(self, folder_path):
        """
        Initialize the PDFParser object with the folder path containing the PDF files.

        Args:
            folder_path (str): The path to the folder containing the PDF files.
        """
        self.folder_path = folder_path

    def parse_folder(self, output_format, output_folder):
        """
        Parse the PDF files in the folder and generate output in the specified format.

        Args:
            output_format (str): The desired output format ('html', 'csv', 'json', 'excel').
            output_folder (str): The path to the output folder where the generated files will be saved.

        Returns:
            str: The path to the generated output file.
        """
        # Get a list of PDF files in the folder
        pdf_files = glob.glob(os.path.join(self.folder_path, '*.pdf'))

        # Initialize an empty dictionary to store the data
        data = {}

        # Process each PDF file in the folder
        for pdf_file in pdf_files:
            file_path = os.path.join(self.folder_path, pdf_file)
            if file_data := self.extract_data(file_path):
                data |= file_data

        return self.generate_output(data, output_format, output_folder)

    def extract_data(self, file_path):
        """
        Extract data from a PDF file.

        Args:
            file_path (str): The path to the PDF file.

        Returns:
            dict: A dictionary containing the extracted data.
        """
        # Open the PDF file
        data = {}
        with pdfplumber.open(file_path) as pdf:
            text = "".join(page.extract_text() for page in pdf.pages)
            text = text.replace('\n', '')

            # Extract employee code and amount
            regex = r"Tax amounting to R(\d+\.\d{2})"
            if matches := re.findall(regex, text, re.DOTALL | re.MULTILINE):
                # Get the filename from the file_path
                filename = os.path.basename(file_path)
                filename = filename.split('.')[0]
                data[filename] = matches[-1]
        return data

    def generate_output(self, data, output_format, output_folder):
        """
        Generate output in the specified format.

        Args:
            data (dict): A dictionary containing the data to be included in the output.
            output_format (str): The desired output format ('html', 'csv', 'json', 'excel').
            output_folder (str): The path to the output folder where the generated files will be saved.

        Returns:
            str: The path to the generated output file.
        """
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Generate output based on the specified format
        if output_format == 'html':
            return self._generate_html_output(data, output_folder)
        elif output_format == 'csv':
            return self._generate_csv_output(data, output_folder)
        elif output_format == 'json':
            return self._generate_json_output(data, output_folder)
        elif output_format == 'excel':
            return self._generate_excel_output(data, output_folder)
        else:
            return 'Invalid output format specified.'

    def _generate_html_output(self, data, output_folder):
        """
        Generate HTML output using pandas DataFrame.

        Args:
            data (dict): A dictionary containing the data to be included in the output.
            output_folder (str): The path to the output folder where the generated file will be saved.

        Returns:
            str:
            str: The path to the generated HTML output file.
        """
        # Generate HTML output using pandas DataFrame
        df = pd.DataFrame.from_dict(data, orient='index', columns=['Amount'])
        df.index.name = 'Employee Code'
        file_path = os.path.join(output_folder, 'output.html')
        df.to_html(file_path)
        return file_path

    def _generate_csv_output(self, data, output_folder):
        """
        Generate CSV output using pandas DataFrame.

        Args:
            data (dict): A dictionary containing the data to be included in the output.
            output_folder (str): The path to the output folder where the generated file will be saved.

        Returns:
            str: The path to the generated CSV output file.
        """
        # Generate CSV output using pandas DataFrame
        df = pd.DataFrame.from_dict(data, orient='index', columns=['Amount'])
        df.index.name = 'Employee Code'
        file_path = os.path.join(output_folder, 'output.csv')
        df.to_csv(file_path)
        return file_path

    def _generate_json_output(self, data, output_folder):
        """
        Generate JSON output using pandas DataFrame.

        Args:
            data (dict): A dictionary containing the data to be included in the output.
            output_folder (str): The path to the output folder where the generated file will be saved.

        Returns:
            str: The path to the generated JSON output file.
        """
        # Generate JSON output using pandas DataFrame
        df = pd.DataFrame.from_dict(data, orient='index', columns=['Amount'])
        df.index.name = 'Employee Code'
        file_path = os.path.join(output_folder, 'output.json')
        df.to_json(file_path, orient='index')
        return file_path

    def _generate_excel_output(self, data, output_folder):
        """
        Generate Excel output using pandas DataFrame.

        Args:
            data (dict): A dictionary containing the data to be included in the output.
            output_folder (str): The path to the output folder where the generated file will be saved.

        Returns:
            str: The path to the generated Excel output file.
        """
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
    """
    A test client for the PDFParser class.

    Args:
        folder (str): The path to the folder containing the PDF files.
        format (str): The desired output format ('html', 'csv', 'json', 'excel').
        output_folder (str): The path to the output folder where the generated files will be saved.
    """
    parser = PDFParser(folder)
    results = parser.parse_folder(format, output_folder)
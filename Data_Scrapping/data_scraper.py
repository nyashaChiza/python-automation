import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_table(url, table_class):
    """
    Scrape data from a table on a webpage and store it as a Pandas dataframe.
    
    Parameters:
    url (str): The URL of the webpage to scrape.
    table_class (str): The class attribute of the table element to scrape.
    
    Returns:
    pandas.DataFrame: A dataframe containing the scraped data.
    """
    
    # Define headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Send a GET request to the URL with headers
    response = requests.get(url, headers=headers)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table element using its class attribute
    table = soup.find("table", {"class": table_class})

    if table is not None:
        # Extract the data from the table
        rows = table.find_all("tr")
        data = []
        for row in rows:
            cols = row.find_all("td")
            cols = [col.text.strip() for col in cols]
            data.append(cols)

        return pd.DataFrame(data[1:], columns=data[0])
    else:
        print("No table found on the webpage.")
        return None


if __name__ == "__name__":

    url = "https://www.databasestar.com/sample-database-movies/"

    data = scrape_table(url,"sqlTable")

    print(data.head())
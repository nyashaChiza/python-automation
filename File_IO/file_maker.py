import pandas as pd

def read_file(file_path, file_type=None, **kwargs):
    """
    Read a file with Pandas.
    
    Parameters:
    file_path (str): The path to the file to read.
    file_type (str): The type of the file to read (e.g. 'csv', 'xlsx', 'txt', 'json').
    **kwargs: Additional keyword arguments to pass to the Pandas reader function.
    
    Returns:
    pandas.DataFrame: A dataframe containing the data from the file.
    """
    
    # Determine the file type based on the file extension if not provided
    if file_type is None:
        file_type = file_path.split(".")[-1]
    
    # Read the file with Pandas
    if file_type == "csv":
        df = pd.read_csv(file_path, **kwargs)
    elif file_type == "xlsx":
        df = pd.read_excel(file_path, **kwargs)
    elif file_type == "txt":
        df = pd.read_table(file_path, **kwargs)
    elif file_type == "json":
        df = pd.read_json(file_path, **kwargs)
    else:
        print(f"Unsupported file type: {file_type}")
        return None
    
    # Return the dataframe
    return df


if __name__ == "__name__":
    
    file_path = "https://json.org/example.html"

    data = read_file(file_path, file_type='json')

    print(data.head())
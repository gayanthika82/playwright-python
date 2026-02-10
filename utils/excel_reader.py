import openpyxl

def read_excel_to_dict(file_path: str, sheet_name: str = None) -> list[dict]:
    """
    Reads an Excel file and converts it into a list of dictionaries.
    Each row in the Excel sheet becomes a dictionary, with the headers as keys.
    All values are converted to strings.

    Args:
        file_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet to read. Defaults to the first sheet.

    Returns:
        list[dict]: A list of dictionaries representing the rows in the Excel sheet.
    """
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name] if sheet_name else workbook.active

    # Extract headers from the first row
    headers = [str(cell.value) for cell in sheet[1]]

    # Convert rows into dictionaries
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_dict = {headers[i]: str(row[i]) if row[i] is not None else "" for i in range(len(headers))}
        data.append(row_dict)

    return data
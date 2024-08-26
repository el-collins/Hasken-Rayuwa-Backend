import pandas as pd
from datetime import datetime


print("Starting the script...")
# Load the Excel file
file_path = "C:/Users/Collins/Downloads/fileupload.xlsx"
df = pd.read_excel(file_path)

# Define a function to convert the date format
def convert_date(date):
    try:
        # Assuming the wrong format is "6-8/02/24"
        date_part = "-".join(date.split("-")[1:])

        return datetime.strptime(date_part, "%m/%d/%y")


        # date_obj = datetime.strptime(date, "%m/%d/%Y")
        # return date_obj.strftime("%d/%m/%Y")
    except Exception as e:
        print(f"Error converting date: {e}")
        return date
    # if isinstance(date, pd.Timestamp):
    #     date_str = date.strftime("%Y-%m-%d %H:%M:%S")
    # else:
    #     date_str = date

    # try:
    #     # Try to parse the date in the format YYYY-MM-DD HH:MM:SS
    #     date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    # except ValueError:
    #     try:
    #         # If the first format fails, try MM/DD/YYYY
    #         date_obj = datetime.strptime(date_str, "%m/%d/%Y")
    #     except ValueError as e:
    #         print(f"Error converting date: {e}")
    #         return date_str
    # return date_obj.strftime("%d/%m/%Y")

# Apply the conversion function to the 'Date' column
df['Date'] = df['Date'].apply(convert_date)

# Save the modified DataFrame back to an Excel file
output_file_path = 'C:/Users/Collins/Downloads/upload_out.xlsx'
df.to_excel(output_file_path, index=False)

print("Date column has been successfully updated.")

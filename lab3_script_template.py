import os 
import sys
from datetime import date
import pandas as pd


def main():
    sales_csv = get_sales_csv()
    orders_dir = create_orders_dir(sales_csv)
    process_sales_data(sales_csv, orders_dir)

# Get path of sales data CSV file from the command line
def get_sales_csv():
    # Check whether command line parameter provided
    if len(sys.argv) < 2:
        print("ERROR: Missing CSV file path.")
        sys.exit(1)

    # Check whether provide parameter is valid path of file
    csv_path = sys.argv[1]
    if not os.path.isfile(csv_path):
        print("ERROR: Invalid CSV file path.")
        sys.exit(1)

    return csv_path

# Create the directory to hold the individual order Excel sheets
def create_orders_dir(sales_csv):
    # Get directory in which sales data CSV file resides
    sales_csv_path = os.path.abspath(sales_csv)
    sales_csv_dir = os.path.dirname(sales_csv_path)

    # Determine the name and path of the directory to hold the order data files
    current_date = date.today().isoformat()
    orders_folder = f"Orders_{current_date}"
    orders_dir = os.path.join(sales_csv_dir, orders_folder)

    # Create the order directory if it does not already exist
    if not os.path.isdir(orders_dir):
        os.makedirs(orders_dir)

    return orders_dir 

# Split the sales data into individual orders and save to Excel sheets
def process_sales_data(sales_csv, orders_dir):
    # Import the sales data from the CSV file into a DataFrame
    sales_df = pd.read_csv(sales_csv)

    # Insert a new "TOTAL PRICE" column into the DataFrame
    sales_df.insert(7, "TOTAL PRICE", sales_df["ITEM QUALITY"] * sales_df["ITEM PRICE"]
                    )

    # Remove columns from the DataFrame that are not needed
    sales_df = sales_df.drop(["ADDRESS", "CITY", "STATE", "POSTAL CODE", "COUNTRY"], inplace=True)
    # Group the rows in the DataFrame by order ID
    data = {}
    sales_data = pd.DataFrame(date)

    # For each order ID:
    grouped_df = sales_data.groupby('ORDER ID')

    for order_id, group in grouped_df:

        # Remove the "ORDER ID" column
        group = group.drop(columns=['ORDER ID'])
         
        # Sort the items by item number
        group = group.sort_values(by='ITEM NUMBER')

        # Append a "GRAND TOTAL" row
        grand_total = group.assign(QUANTITY=lambda x: x['QUANTITY'].sum(),
                                   ITEM_PRICE=lambda x: x['QUANTITY'] * x['ITEM PRICE']).sum()
        grand_total['ITEM NUMBER'] = 'GRAND TOTAL'
        group = group.append(grand_total, ignore_index=True)

        # Determine the file name and full path of the Excel sheet
        file_name = f"{order_id}.xlsx"
        full_path = f"Orders_{order_id}/{file_name}"

        # Export the data to an Excel sheet
        group.to_excel(full_path, index=False)
        # TODO: Format the Excel sheet
    pass

if __name__ == '__main__':
    main()
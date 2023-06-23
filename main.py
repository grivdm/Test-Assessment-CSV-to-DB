import time
from data_loader import load_restaurants_data_from_csv_to_db
from data_processing import calculate_rank_and_upload
import argparse

parser = argparse.ArgumentParser(description='Load data from CSV to DB and calculate rank')
parser.add_argument( '--interactive', action='store_true', help='Interactive mode')

def main():



    args = parser.parse_args()


    # Load the data from the CSV file
    defalut_file = 'fastfood.csv'

    # Ask the user to enter filename if in interactive mode
    input_file = input(f"Enter the name of the file to load (default: {defalut_file}): ") if args.interactive else defalut_file
    
    start_time = time.time()
    load_restaurants_data_from_csv_to_db(input_file or defalut_file)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    print(f"DataLoad: {elapsed_time} seconds")

    # Calculate the rank and upload the data about categories and subcategories to CSV
    calculate_rank_and_upload()


if __name__ == "__main__":
    main()


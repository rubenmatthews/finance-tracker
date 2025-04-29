import pandas as pd # Load pandas for data manipulation
import os # Load environment variables

file_path = os.getenv('TRANSACTIONS_FILE_PATH', 'data/sample_transactions.csv')

if not file_path or not os.path.exists(file_path): # If I dont even have a path or the file does not exist
    print(f"Error: File not found at {file_path}")
    transactions = None
else:
    print("File found! Ready to load.")
    transactions = pd.read_csv(file_path)
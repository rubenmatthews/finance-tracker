import pandas as pd
import os

# Load file path from environment or use default sample
file_path = os.getenv('TRANSACTIONS_FILE_PATH', 'data/sample_transactions.csv')

# Load the data if file exists
if not file_path or not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    transactions = None
else:
    print("File found! Loading data...")
    transactions = pd.read_csv(file_path)
    
    # Clean column names by stripping whitespace
    transactions.columns = transactions.columns.str.strip()
    
    # Check required columns exist
    required_columns = ['Date', 'Amount', 'Category', 'Description', 'Recurring']
    missing_columns = [col for col in required_columns if col not in transactions.columns]
    if missing_columns:
        print(f"Error: Missing required columns: {missing_columns}")
        transactions = None
    else:
        print("All required columns present.")

def clean_transactions(df):
    """
    Cleans a transaction DataFrame: handles missing values, standardizes fields,
    ensures valid formats for analysis.
    """
    if df is None:
        print("Error: No transactions data to clean")
        return None

    # Make a copy to avoid mutating the original DataFrame
    clean_df = df.copy()

    # Strip whitespace from column names
    clean_df.columns = clean_df.columns.str.strip()

    # Clean 'Description' entries
    if 'Description' in clean_df.columns:
        clean_df['Description'] = clean_df['Description'].astype(str).str.strip().str.strip('"')
    
    # Drop rows with missing dates  
    clean_df = clean_df.dropna(subset=['Date'])
    print(f"Dropped {len(df) - len(clean_df)} rows with missing dates")

    # Convert 'Date' to datetime format
    clean_df['Date'] = pd.to_datetime(clean_df['Date'], format='%d/%m/%Y', errors='coerce')
    print("Converted Date column to datetime format")

    # Fill missing values with standard values
    clean_df['Amount'] = clean_df['Amount'].fillna(0)
    clean_df['Category'] = clean_df['Category'].fillna('Uncategorized')
    clean_df['Description'] = clean_df['Description'].fillna('No description')
    clean_df['Recurring'] = clean_df['Recurring'].fillna('No')
    print("Filled missing values with standard values")

    # Standardize category names
    clean_df['Category'] = clean_df['Category'].str.strip().str.title()
    valid_categories = ['Food', 'Transportation', 'Housing', 'Leisure']
    is_valid = clean_df['Category'].isin(valid_categories)
    invalid = (~is_valid).sum()
    if invalid:
        print(f"Warning: Found {invalid} invalid categories. Replacing with 'Uncategorized'.")
        clean_df.loc[~is_valid, 'Category'] = 'Uncategorized'

    # Convert recurring column to boolean
    clean_df['Recurring'] = clean_df['Recurring'].str.strip().str.title() == 'Yes'
    print("Converted Recurring column to boolean")

    # Remove rows that only have a date
    mask = (
        clean_df['Date'].notna() &
        clean_df['Amount'].isna() &
        clean_df['Description'].isna() &
        clean_df['Category'].isna() &
        clean_df['Recurring'].isna()
    )
    rows_to_drop = mask.sum()
    if rows_to_drop:
        clean_df = clean_df[~mask]
        print(f"Dropped {rows_to_drop} rows that only had a date")

    # Drop duplicates
    before = len(clean_df)
    clean_df = clean_df.drop_duplicates()
    after = len(clean_df)
    print(f"Dropped {before - after} duplicate rows")

    return clean_df

# Run clean if data exists
if transactions is not None:
    cleaned = clean_transactions(transactions)
    if cleaned is not None:
        print("\nCleaned Transactions:")
        print(cleaned.head(10))
        print("\nDataFrame Info:")
        print(cleaned.info())
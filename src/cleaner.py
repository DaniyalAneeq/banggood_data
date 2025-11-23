import pandas as pd
import os
import glob

# --- CONFIGURATION ---
# Robust directory detection (Works in Jupyter AND Scripts)
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    BASE_DIR = os.getcwd() # Fallback for Jupyter Notebooks

# Construct paths relative to the project root (assuming you run from project root or src)
# If running from 'src/', move up one level. If running from root, stay there.
if os.path.basename(BASE_DIR) == "src":
    DATA_DIR = os.path.join(BASE_DIR, "../data")
else:
    DATA_DIR = os.path.join(BASE_DIR, "data")

INPUT_PATTERN = os.path.join(DATA_DIR, "*.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "cleaned_all_products.csv")

def clean_currency(val):
    """Converts 'US$1,234.99' -> 1234.99"""
    if not isinstance(val, str):
        return val
    # Clean currency strings
    clean_str = val.replace("US", "").replace("$", "").replace(",", "").strip()
    try:
        return float(clean_str)
    except ValueError:
        return 0.0

def clean_reviews(val):
    """Converts '15 Reviews' or '(15)' -> 15"""
    if pd.isna(val): return 0
    clean_str = str(val).replace("Reviews", "").replace("(", "").replace(")", "").strip()
    try:
        return int(clean_str)
    except ValueError:
        return 0

def main():
    print("--- Starting Data Cleaning ---")
    print(f"Looking for data in: {os.path.abspath(DATA_DIR)}")
    
    # 1. Load and Merge all CSVs
    all_files = glob.glob(INPUT_PATTERN)
    # Exclude output/raw files to prevent loops
    all_files = [f for f in all_files if "cleaned_all_products.csv" not in f and "raw_products" not in f]
    
    if not all_files:
        print("No CSV files found! Check your directory.")
        return

    print(f"Found {len(all_files)} files. Merging...")
    
    df_list = []
    for filename in all_files:
        try:
            df_temp = pd.read_csv(filename)
            df_list.append(df_temp)
        except Exception as e:
            print(f"Skipping bad file {filename}: {e}")

    if not df_list:
        print("No valid data to merge.")
        return

    df = pd.concat(df_list, ignore_index=True)
    print(f"Raw merged shape: {df.shape}")

    # 2. Data Cleaning
    print("Cleaning columns...")
    df['Price'] = df['Price'].apply(clean_currency)
    df['Reviews'] = df['Reviews'].apply(clean_reviews)
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').fillna(0.0)
    
    # Filter invalid rows
    df = df[df['Price'] > 0]

    # 3. Feature Engineering
    print("Generating features...")
    df['Revenue_Potential'] = df['Price'] * df['Reviews']
    
    def get_tier(price):
        if price < 20: return "Budget"
        elif price < 100: return "Mid-Range"
        else: return "Premium"
        
    df['Price_Tier'] = df['Price'].apply(get_tier)

    # 4. Save
    # Create directory if not exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"SUCCESS: Cleaned data saved to {OUTPUT_FILE}")
    print(df.head())

if __name__ == "__main__":
    main()
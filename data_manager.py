from pathlib import Path
from datetime import datetime
import pandas as pd

DATA_FILE = Path(__file__).resolve().parent / "transactions.csv"
COLUMNS = ["id", "date", "type", "category", "amount",
           "description", "payment_method", "month"]

def load_data():
    """Load the project CSV and standardize its column names."""
    if not DATA_FILE.exists():
        empty = pd.DataFrame(columns=COLUMNS)
        empty.to_csv(DATA_FILE, index=False)
        return empty

    df = pd.read_csv(DATA_FILE)
    df.columns = [str(col).strip().lower() for col in df.columns]

    for col in COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df = df[COLUMNS].copy()
    df["id"] = df["id"].fillna("").astype(str)
    df["date"] = df["date"].fillna("").astype(str)
    df["type"] = df["type"].fillna("").astype(str).str.strip().str.title()
    df["category"] = df["category"].fillna("Other").astype(str)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df["description"] = df["description"].fillna("No description").astype(str)
    df["payment_method"] = df["payment_method"].fillna("Not specified").astype(str)
    df["month"] = df["month"].fillna("").astype(str)

    # Save standardized headers so all modules use the same schema.
    df.to_csv(DATA_FILE, index=False)
    return df

def save_data(data):
    data = data.copy()
    data.columns = [str(col).strip().lower() for col in data.columns]
    for col in COLUMNS:
        if col not in data.columns:
            data[col] = ""
    data = data[COLUMNS]
    data.to_csv(DATA_FILE, index=False)

def generate_id(data):
    numbers = []
    for value in data["id"].astype(str):
        digits = "".join(ch for ch in value if ch.isdigit())
        if digits:
            numbers.append(int(digits))
    return f"TXN{max(numbers, default=0) + 1:03d}"

def add_record(data):
    print("\\n--- Add Transaction ---")
    choice = input("Type (1 = Income, 2 = Expense): ").strip()
    if choice not in ("1", "2"):
        print("Invalid type. Record not added.")
        return data

    txn_type = "Income" if choice == "1" else "Expense"
    txn_date = input("Date (YYYY-MM-DD): ").strip()
    try:
        parsed_date = datetime.strptime(txn_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return data

    category = input("Category: ").strip() or "Other"
    description = input("Description: ").strip() or "No description"
    payment_method = input("Payment method (Cash/UPI/Card): ").strip() or "Not specified"
    try:
        amount = float(input("Amount (Rs.): ").strip())
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Amount must be a number greater than zero.")
        return data

    new_row = {
        "id": generate_id(data),
        "date": parsed_date.strftime("%Y-%m-%d"),
        "type": txn_type,
        "category": category,
        "amount": amount,
        "description": description,
        "payment_method": payment_method,
        "month": parsed_date.strftime("%B")
    }
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
    save_data(data)
    print(f"Transaction added. Your ID is {new_row['id']}")
    return data

def display_records(data):
    print("\\n--- All Transactions ---")
    if data.empty:
        print("No transactions found.")
    else:
        print(data.to_string(index=False))
        print(f"\\nTotal records: {len(data)}")

def search_record(data):
    txn_id = input("Enter transaction ID: ").strip().upper()
    result = data[data["id"].astype(str).str.upper() == txn_id]
    if result.empty:
        print("Transaction not found.")
    else:
        print(result.to_string(index=False))

def update_record(data):
    txn_id = input("Enter transaction ID to update: ").strip().upper()
    matches = data.index[data["id"].astype(str).str.upper() == txn_id].tolist()
    if not matches:
        print("Transaction not found.")
        return data

    idx = matches[0]
    print("Press Enter to keep the existing value.")
    for col in ["category", "description", "payment_method"]:
        new_value = input(f"{col} [{data.at[idx, col]}]: ").strip()
        if new_value:
            data.at[idx, col] = new_value

    new_amount = input(f"amount [{data.at[idx, 'amount']}]: ").strip()
    if new_amount:
        try:
            value = float(new_amount)
            if value <= 0:
                raise ValueError
            data.at[idx, "amount"] = value
        except ValueError:
            print("Invalid amount; old amount kept.")

    save_data(data)
    print("Transaction updated successfully.")
    return data

def delete_record(data):
    txn_id = input("Enter transaction ID to delete: ").strip().upper()
    updated = data[data["id"].astype(str).str.upper() != txn_id].copy()
    if len(updated) == len(data):
        print("Transaction not found.")
    else:
        data = updated.reset_index(drop=True)
        save_data(data)
        print("Transaction deleted successfully.")
    return data

def show_data_structures(data):
    # List, Tuple, Set, Dictionary and List methods
    category_list = data["category"].tolist()
    category_list.append("Sample")
    category_list.sort()
    category_tuple = tuple(category_list[:5])
    category_set = set(category_list)
    details = {
        "total_transactions": len(data),
        "unique_categories": len(category_set),
        "categories": sorted(category_set)
    }
    print("\\n--- Python Data Structures ---")
    print("List:", category_list[:10])
    print("Tuple:", category_tuple)
    print("Set:", category_set)
    print("Dictionary:", details)
    print("List methods used: append(), sort()")

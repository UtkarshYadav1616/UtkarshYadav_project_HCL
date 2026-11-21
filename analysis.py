import numpy as np
import pandas as pd

def analyze_data(data):
    df = pd.DataFrame(data).copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    if df.empty:
        print("No data available for analysis.")
        return

    required = ["id", "date", "type", "category", "amount",
                "description", "payment_method", "month"]
    for col in required:
        if col not in df.columns:
            df[col] = ""

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df["type"] = df["type"].fillna("Unknown").astype(str).str.strip().str.title()
    df["category"] = df["category"].fillna("Other").astype(str)

    print("\\n========== PANDAS ANALYSIS ==========")
    print("\\nMissing values:")
    print(df.isnull().sum())
    print("\\nFirst five rows:")
    print(df.head().to_string(index=False))
    print("\\nSelected columns:")
    print(df[["id", "date", "category", "amount"]].head().to_string(index=False))

    expenses = df[df["type"].str.lower() == "expense"]
    print("\\nExpense records:")
    print(expenses.head().to_string(index=False) if not expenses.empty else "No expenses found.")

    print("\\nSorted by amount (highest first):")
    print(df.sort_values("amount", ascending=False).head().to_string(index=False))

    print("\\nGroupBy: total amount by category")
    print(df.groupby("category")["amount"].sum().sort_values(ascending=False))

    amounts = np.array(df["amount"], dtype=float)       # 1D array
    amounts_2d = df[["amount"]].to_numpy(dtype=float)  # 2D array

    print("\\n========== NUMPY ANALYSIS ==========")
    print("1D array:", amounts)
    print("2D array (first five rows):\\n", amounts_2d[:5])
    print("Indexing - first amount:", amounts[0])
    print("Slicing - first five amounts:", amounts[:5])
    print("Sum:", np.sum(amounts))
    print("Mean:", np.mean(amounts))
    print("Maximum:", np.max(amounts))
    print("Minimum:", np.min(amounts))
    print("Standard deviation:", np.std(amounts))

    print("\\nPandas statistical summary:")
    print(df["amount"].describe())

    income = df.loc[df["type"].str.lower() == "income", "amount"].sum()
    expense = df.loc[df["type"].str.lower() == "expense", "amount"].sum()
    print("\\n========== BUDGET INSIGHTS ==========")
    print(f"Total income: Rs. {income:.2f}")
    print(f"Total expenses: Rs. {expense:.2f}")
    print(f"Net savings: Rs. {income - expense:.2f}")

import pandas as pd

def summary_report(data):
    df = pd.DataFrame(data).copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    if df.empty:
        print("No transactions available for report.")
        return

    # Standardize expected fields and avoid KeyError from capitalized CSV headers.
    for col in ["type", "category", "amount"]:
        if col not in df.columns:
            df[col] = "" if col != "amount" else 0

    df["type"] = df["type"].fillna("Unknown").astype(str).str.strip().str.title()
    df["category"] = df["category"].fillna("Other").astype(str)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)

    income = df.loc[df["type"] == "Income", "amount"].sum()
    expense = df.loc[df["type"] == "Expense", "amount"].sum()

    print("\\n========== STUDENT BUDGET SUMMARY ==========")
    print("Total transactions:", len(df))
    print(f"Total income: Rs. {income:.2f}")
    print(f"Total expenses: Rs. {expense:.2f}")
    print(f"Net savings: Rs. {income - expense:.2f}")

    expense_df = df[df["type"] == "Expense"]
    print("\\nCategory-wise expenses:")
    if expense_df.empty:
        print("No expense records.")
    else:
        totals = expense_df.groupby("category")["amount"].sum().sort_values(ascending=False)
        print(totals.to_string())
        print(f"Highest spending category: {totals.idxmax()} (Rs. {totals.max():.2f})")
    print("============================================")

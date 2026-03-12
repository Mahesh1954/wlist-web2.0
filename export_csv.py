import csv
from datetime import datetime

def export_all_transactions_to_csv(transactions):
    try:
        if not transactions:
            return None
        
        current_date = datetime.now().strftime("%d-%m-%Y")
        default_filename = f"wlist_transactions_{current_date}.csv"
        
        rows = []
        rows.append(['Date', 'Time', 'Item Name', 'Amount', 'Currency', 'Note'])
        
        for trans in transactions:
            rows.append([
                trans.get('transaction_date', ''),
                trans.get('transaction_time', ''),
                trans.get('item_name', ''),
                trans.get('amount', 0),
                trans.get('currency', 'Rs'),
                trans.get('note', '')
            ])
        
        csv_data = '\n'.join([','.join(map(str, row)) for row in rows])
        return csv_data
    except Exception as e:
        return None

def export_item_transactions_to_csv(item_name, transactions):
    try:
        if not transactions:
            return None
        
        current_date = datetime.now().strftime("%d-%m-%Y")
        safe_name = "".join(c for c in item_name if c.isalnum() or c in ' ')
        default_filename = f"wlist_{safe_name}_{current_date}.csv"
        
        rows = []
        rows.append(['Date', 'Time', 'Amount', 'Currency', 'Note'])
        
        for trans in transactions:
            rows.append([
                trans.get('transaction_date', ''),
                trans.get('transaction_time', ''),
                trans.get('amount', 0),
                trans.get('currency', 'Rs'),
                trans.get('note', '')
            ])
        
        csv_data = '\n'.join([','.join(map(str, row)) for row in rows])
        return csv_data
    except Exception as e:
        return None

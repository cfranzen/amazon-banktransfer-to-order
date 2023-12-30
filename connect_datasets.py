import pandas as pd
import re
from decimal import Decimal

AMAZON_ORDERS_CSVFILE = 'data/Retail.OrderHistory.2.csv'
BANK_TRANSACTIONS_CSVFILE = 'data/transactions.csv'
RESULT_CSVFILE = 'data/result.csv'

orders = pd.read_csv(AMAZON_ORDERS_CSVFILE, delimiter=',', index_col='Order ID')
transactions = pd.read_csv(BANK_TRANSACTIONS_CSVFILE, delimiter=';')

result_rows = []
for index, row in transactions.iterrows():
    date = row['Date']
    payer_name = row['PayeePayerName']
    purpose = row['Purpose']
    transactionValue = Decimal(row['Value'].replace('.', '').replace(',', '.'))

    match = re.search(r"\d+-\d+-\d+", purpose)
    if match:
        order_id = match.group()
    else:
        continue

    order = orders.loc[order_id]
    if isinstance(order, pd.DataFrame):
        for order_index, order_row in order.iterrows():
            orderValue = Decimal(order_row['Total Owed'].replace(',', ''))
            productName = order_row['Product Name']
            result_rows.append([date, order_id, transactionValue, orderValue, productName, payer_name])
    else:
        orderValue = Decimal(order['Total Owed'].replace(',', ''))
        productName = order['Product Name']
        result_rows.append([date, order_id, transactionValue, orderValue, productName, payer_name])

result = pd.DataFrame(result_rows, columns=[
    'Date', 'OrderID', 'BankTransactionValue', 'OrderValue', 'ProductName', 'Payer'
])
result.to_csv(RESULT_CSVFILE, index=False)

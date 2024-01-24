import MetaTrader5 as mt5
import pandas as pd
import json

# Function to read login detail
def read_login_details(file_path='login_details.json'):
    with open(file_path, 'r') as file:
        login_details = json.load(file)
    return login_details

# Function to read lot size from 'lot.txt'
def read_lot_size():
    with open('lot.txt', 'r') as file:
        lot_size = float(file.read().strip())
    return lot_size

# Function to delete all pending orders
def delete_all_pending_orders():
     # get all pending orders
    orders = mt5.orders_get()

    # loop through the orders and delete them
    for order in orders:
        # use the order_send function with the action parameter set to mt5.TRADE_ACTION_REMOVE
        result = mt5.order_send({"action": mt5.TRADE_ACTION_REMOVE, "order": order.ticket})
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"Order {order.ticket} deleted successfully")
        else:
            print(f"Order {order.ticket} deletion failed, retcode: {result.retcode}")

# Function to send pending orders based on data in 'orderlist.xlsx'
def send_pending_orders():
    # Read lot size
    lot = read_lot_size()
    # Read order data from 'orderlist.xlsx'
    order_data = pd.read_excel('orderlist.xlsx')
    # Iterate through each row in the order data
    for index, row in order_data.iterrows():
        symbol = row['Pair']
        order_type = row['Order']
        price = row['Entry']
        sl = row['SL']
        tp = row['TP']
        comment = row['Comment']

        # Determine order type
        mt5_order_type = mt5.ORDER_TYPE_BUY_LIMIT if order_type == 'Buy_Limit' else mt5.ORDER_TYPE_SELL_LIMIT

        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": lot,
            "type": mt5_order_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "magic": 182412,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        # Place limit order
        result = mt5.order_send(request)
        print(f"{order_type} for {symbol} placed")

# Function to start Meta Trader 5 (MT5), remove pending orders, and send new pending orders
def start_mt5_and_send_orders(username, password, server, path):
    # Ensure that all variables are the correct type
    uname = int(username)
    pword = str(password)
    trading_server = str(server)
    filepath = str(path)

    print("Attempting to start MT5...")
    # Attempt to start MT5
    if mt5.initialize(login=uname, password=pword, server=trading_server, path=filepath):
        print("MT5 Initialized successfully.")
        # Login to MT5
        if mt5.login(login=uname, password=pword, server=trading_server):
            print("Login successful.")

            # User input section
            while True:
                print("\nMenu:")
                print("1. Delete All Pending Orders")
                print("2. Place New Pending Orders")
                print("3. Exit")

                choice = input("Enter your choice (1, 2, or 3): ")

                if choice == '1':
                    delete_all_pending_orders()
                elif choice == '2':
                    send_pending_orders()
                elif choice == '3':
                    print("Exiting the script.")
                    mt5.shutdown()
                    return True
                else:
                    print("Invalid choice. Please enter a valid option.")

        else:
            print("Login failed.")
            raise PermissionError("Login failed")
    else:
        print("MT5 Initialization Failed")
        raise ConnectionAbortedError("MT5 Initialization failed")

# Execute Script
try:
    login_details = read_login_details()
    start_mt5_and_send_orders(**login_details)
except (PermissionError, ConnectionAbortedError) as e:
    print(f"Error: {e}")

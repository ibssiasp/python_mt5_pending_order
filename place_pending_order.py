import MetaTrader5 as mt5
import pandas as pd

# Function to read lot size from 'lot.txt'
def read_lot_size():
    with open('lot.txt', 'r') as file:
        lot_size = float(file.read().strip())
    return lot_size

# Function to delete all pending orders
def delete_all_pending_orders():
    # Define pending order types
    pending_order_types = [
        mt5.ORDER_TYPE_BUY_LIMIT,
        mt5.ORDER_TYPE_SELL_LIMIT,
        mt5.ORDER_TYPE_BUY_STOP,
        mt5.ORDER_TYPE_SELL_STOP,
        mt5.ORDER_TYPE_BUY_STOP_LIMIT,
        mt5.ORDER_TYPE_SELL_STOP_LIMIT
    ]

    # Get all pending orders
    orders = mt5.orders_get()
    
    # Delete each pending order
    for order in orders:
        if order['type'] in pending_order_types:
            result = mt5.order_delete(order['ticket'])
            if result:
                print(f"Pending order {order['ticket']} deleted")
            else:
                print(f"Failed to delete pending order {order['ticket']}")

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


# Function to start Meta Trader 5 (MT5) and send pending orders
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
            # Call the function to delete pending orders
            delete_all_pending_orders()
            # Call the function to send pending orders
            send_pending_orders()
            return True
        else:
            print("Login failed.")
            raise PermissionError("Login failed")
    else:
        print("MT5 Initialization Failed")
        raise ConnectionAbortedError("MT5 Initialization failed")

# Example usage
try:
    start_mt5_and_send_orders(username=123456789, password='YourPassword', server='Broker-Server', path=r"C:\Program Files\MetaTrader 5\terminal64.exe")
except (PermissionError, ConnectionAbortedError) as e:
    print(f"Error: {e}")

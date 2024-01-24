#Python MetaTrader 5 Pending Order Script

This script leverages the MetaTrader 5 (MT5) platform to automate the execution of pending orders based on predefined criteria. The key functionalities include reading lot size from a 'lot.txt' file, deleting all existing pending orders, and placing new pending orders using data from an 'orderlist.xlsx' file.

## Functions:

1. **read_lot_size():**
   - Reads lot size from the 'lot.txt' file.

2. **delete_all_pending_orders():**
   - Deletes all pending orders, including buy/sell limits and stop orders.

3. **send_pending_orders():**
   - Reads order details from 'orderlist.xlsx' and sends pending orders to the market.

4. **start_mt5_and_send_orders(username, password, server, path):**
   - Initializes and logs into MT5 using the provided credentials.
   - Calls the `delete_all_pending_orders()` function.
   - Calls the `send_pending_orders()` function to place new pending orders.

5. Remember to input your MT5 login detail in login_details.json
```

**Note:** Ensure that the required files ('lot.txt' and 'orderlist.xlsx') exist and are correctly formatted for the script to function as expected. Adjust the example usage parameters according to your MT5 account details and file paths.

**only works on the Windows operating system
**if you find difficulties installing 'pip MetaTrader5', try to use/install python 3.10

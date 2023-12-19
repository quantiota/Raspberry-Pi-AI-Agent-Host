import datetime
import threading
import websocket
import json
import psycopg2
import psycopg2.extras

def create_questdb_table():
    # Connect to QuestDB (update host, user, password, and database name as necessary)
    conn = psycopg2.connect(
        dbname='qdb', 
        user='admin', 
        password='quest', 
        host='docker_host_ip_address', 
        port='8812'
    )
    cur = conn.cursor()


    # Create table SQL command
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS binance_trades (
        symbol STRING,
        trade_id DOUBLE,
        price DOUBLE,
        quantity DOUBLE,
        buyer_order_id LONG,
        seller_order_id LONG,
        is_buyer_market_maker BOOLEAN,
        trade_time TIMESTAMP   
    ) TIMESTAMP(trade_time) PARTITION BY DAY;
    """
    cur.execute(create_table_sql)
    conn.commit()

    # Close the connection
    cur.close()
    conn.close()

def insert_into_questdb(data):
    try:
        # Connect to QuestDB
        conn = psycopg2.connect(
            dbname='qdb', 
            user='admin', 
            password='quest', 
            host='docker_host_ip_address', 
            port='8812'
        )
        cur = conn.cursor()

        # SQL Insert statement
        insert_sql = """
        INSERT INTO binance_trades (symbol, trade_id, price, quantity, buyer_order_id, 
                                   seller_order_id, is_buyer_market_maker, trade_time) 
        VALUES (%s, %s, %s, %s, %s, %s,  %s, %s)
        """
        # Convert trade_time from milliseconds to a datetime object
        trade_time_datetime = datetime.datetime.utcfromtimestamp(int(data['T']) / 1000.0)



        # Data extraction
        trade_data = (
            data['s'],  # symbol
            data['t'],  # trade_id
            float(data['p']),  # price
            float(data['q']),  # quantity
            data['b'],  # buyer_order_id
            data['a'],  # seller_order_id
            data['m'],  # is_buyer_market_maker
            trade_time_datetime  # trade_time in seconds
        )

        # Execute SQL statement
        cur.execute(insert_sql, trade_data)
        conn.commit()

        # Close the connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error inserting into QuestDB: {e}")

def on_message(ws, message):
    print("Received Message:")
    data = json.loads(message)
    print(data)
    insert_into_questdb(data)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### Closed ###")
    print("Close status code: ", close_status_code)
    print("Close message: ", close_msg)


def on_open(ws):
    print("Connection opened")

def start_websocket(url, on_open):
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()






if __name__ == "__main__":
    websocket.enableTrace(True)
    
    # Create the database table in QuestDB
    create_questdb_table()

    # Start WebSocket connections
    btcusdt_url = "wss://stream.binance.com:9443/ws/btcusdt@trade"

    ethusdt_url = "wss://stream.binance.com:9443/ws/ethusdt@trade"



  # Start WebSocket connections in separate threads
    btc_thread = threading.Thread(target=start_websocket, args=(btcusdt_url, lambda: print("BTC/USDT Connection opened")))
    eth_thread = threading.Thread(target=start_websocket, args=(ethusdt_url, lambda: print("ETH/USDT Connection opened")))

    btc_thread.start()
    eth_thread.start()

    btc_thread.join()
    eth_thread.join()
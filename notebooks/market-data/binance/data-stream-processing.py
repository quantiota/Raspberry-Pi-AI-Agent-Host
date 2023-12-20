import datetime
import json
import logging
import os
import psycopg2
import psycopg2.pool
import threading
import websocket
from concurrent.futures import ThreadPoolExecutor

# Configuration
DB_NAME = os.getenv('DB_NAME', 'qdb')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'quest')
DB_HOST = os.getenv('DB_HOST', 'docker_host_ip_address')
DB_PORT = os.getenv('DB_PORT', '8812')

# Logging Configuration
logging.basicConfig(level=logging.INFO)

# Initialize connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10,
                                                     dbname=DB_NAME,
                                                     user=DB_USER,
                                                     password=DB_PASSWORD,
                                                     host=DB_HOST,
                                                     port=DB_PORT)

def create_questdb_table():
    """Create a table in QuestDB."""
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cur:
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS binance_trades (
                symbol STRING,
                trade_id DOUBLE,
                price DOUBLE,
                quantity DOUBLE,
                buyer_order_id LONG,
                seller_order_id LONG,
                is_buyer_market_maker BOOLEAN,
                timestamp TIMESTAMP
            ) TIMESTAMP(timestamp) PARTITION BY DAY;
            """
            cur.execute(create_table_sql)
            conn.commit()
    except Exception as e:
        logging.error(f"Error creating QuestDB table: {e}")
    finally:
        connection_pool.putconn(conn)

def insert_into_questdb(data):
    """Insert data into QuestDB."""
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cur:
            insert_sql = """
            INSERT INTO binance_trades (symbol, trade_id, price, quantity, buyer_order_id, seller_order_id, is_buyer_market_maker, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            trade_time_datetime = datetime.datetime.utcfromtimestamp(int(data['T']) / 1000.0)
            trade_data = (
                data['s'],
                data['t'],
                float(data['p']),
                float(data['q']),
                data['b'],
                data['a'],
                data['m'],
                trade_time_datetime
            )
            cur.execute(insert_sql, trade_data)
            conn.commit()
    except Exception as e:
        logging.error(f"Error inserting into QuestDB: {e}")
    finally:
        connection_pool.putconn(conn)

def on_message(ws, message):
    """Handle incoming WebSocket messages."""
    logging.info("Received Message")
    data = json.loads(message)
    insert_into_questdb(data)

def on_error(ws, error):
    """Handle WebSocket errors."""
    logging.error(error)

def on_close(ws, close_status_code, close_msg):
    """Handle WebSocket closure."""
    logging.info("### Closed ###")
    logging.info(f"Close status code: {close_status_code}")
    logging.info(f"Close message: {close_msg}")

def on_open(ws):
    """Handle opening of WebSocket connection."""
    logging.info("Connection opened")

def start_websocket(url, on_open):
    """Start a WebSocket connection."""
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    create_questdb_table()

    # URLs for WebSocket connections
    urls = ["wss://stream.binance.com:9443/ws/btcusdt@trade",
            "wss://stream.binance.com:9443/ws/ethusdt@trade"]

    # Start WebSocket connections in separate threads
    with ThreadPoolExecutor(max_workers=len(urls)) as executor:
        for url in urls:
            executor.submit(start_websocket, url, lambda: logging.info(f"{url} Connection opened"))

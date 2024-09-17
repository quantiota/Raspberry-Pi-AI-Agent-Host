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
QDB_PG_NAME = os.getenv('QDB_PG_NAME', 'qdb')
QDB_PG_USER = os.getenv('QDB_PG_USER', 'admin')
QDB_PG_PASSWORD = os.getenv('QDB_PG_PASSWORD', 'quest')
QDB_PG_HOST = os.getenv('QDB_PG_HOST', 'docker_host_ip_address')
QDB_PG_PORT = os.getenv('QDB_PG_PORT', '8812')

# Logging Configuration
logging.basicConfig(level=logging.INFO)

# Initialize connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10,
                                                     dbname=QDB_PG_NAME,
                                                     user=QDB_PG_USER,
                                                     password=QDB_PG_PASSWORD,
                                                     host=QDB_PG_HOST,
                                                     port=QDB_PG_PORT)

def create_questdb_table():
    """Create a table in QuestDB for order book data."""
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cur:
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS binance_order_book (
                symbol TEXT,
                update_id BIGINT,
                bid_price DOUBLE PRECISION,
                bid_quantity DOUBLE PRECISION,
                ask_price DOUBLE PRECISION,
                ask_quantity DOUBLE PRECISION,
                event_time TIMESTAMP
            ) TIMESTAMP(event_time) PARTITION BY DAY;
            """
            cur.execute(create_table_sql)
            conn.commit()
    except Exception as e:
        logging.error(f"Error creating QuestDB table: {e}")
    finally:
        connection_pool.putconn(conn)

def insert_into_questdb(data, symbol):
    """Insert order book data into QuestDB."""
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cur:
            insert_sql = """
            INSERT INTO binance_order_book (symbol, update_id, bid_price, bid_quantity, ask_price, ask_quantity, event_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            event_time_datetime = datetime.datetime.utcfromtimestamp(int(data['E']) / 1000.0)
            for bid in data['b']:
                bid_data = (
                    symbol,
                    data['u'],
                    float(bid[0]),
                    float(bid[1]),
                    None,
                    None,
                    event_time_datetime
                )
                cur.execute(insert_sql, bid_data)
            for ask in data['a']:
                ask_data = (
                    symbol,
                    data['u'],
                    None,
                    None,
                    float(ask[0]),
                    float(ask[1]),
                    event_time_datetime
                )
                cur.execute(insert_sql, ask_data)
            conn.commit()
    except Exception as e:
        logging.error(f"Error inserting into QuestDB: {e}")
    finally:
        connection_pool.putconn(conn)

def on_message(ws, message, symbol):
    """Handle incoming WebSocket messages for order book."""
    logging.info("Received Message")
    data = json.loads(message)
    insert_into_questdb(data, symbol)

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

def start_websocket(url, symbol):
    """Start a WebSocket connection for order book."""
    ws = websocket.WebSocketApp(url,
                                on_message=lambda ws, msg: on_message(ws, msg, symbol),
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    create_questdb_table()

    # URLs for WebSocket connections to order book streams
    order_book_streams = {
        "wss://stream.binance.com:9443/ws/btcusdt@depth@100ms": "BTCUSDT",
        "wss://stream.binance.com:9443/ws/ethusdt@depth@100ms": "ETHUSDT"
    }

    # Start WebSocket connections in separate threads
    with ThreadPoolExecutor(max_workers=len(order_book_streams)) as executor:
        for url, symbol in order_book_streams.items():
            executor.submit(start_websocket, url, symbol)
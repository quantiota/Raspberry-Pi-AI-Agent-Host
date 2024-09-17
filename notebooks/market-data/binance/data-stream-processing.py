import datetime
import json
import logging
import os
import psycopg2
import psycopg2.pool
import threading
import websocket
import signal
from concurrent.futures import ThreadPoolExecutor
import traceback

# Configuration
QDB_PG_NAME = os.getenv('QDB_PG_NAME', 'qdb')
QDB_PG_USER = os.getenv('QDB_PG_USER', 'admin')
QDB_PG_PASSWORD = os.getenv('QDB_PG_PASSWORD', 'quest')
QDB_PG_HOST = os.getenv('QDB_PG_HOST', 'docker_host_ip_address')
QDB_PG_PORT = os.getenv('QDB_PG_PORT', '8812')

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Initialize connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10,
                                                     dbname=QDB_PG_NAME,
                                                     user=QDB_PG_USER,
                                                     password=QDB_PG_PASSWORD,
                                                     host=QDB_PG_HOST,
                                                     port=QDB_PG_PORT)
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
        logging.error(traceback.format_exc())
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
                data.get('s'),  # symbol
                data.get('t'),  # trade_id
                float(data.get('p', 0.0)),  # price
                float(data.get('q', 0.0)),  # quantity
                data.get('b', None),  # buyer_order_id
                data.get('a', None),  # seller_order_id
                data.get('m', False),  # is_buyer_market_maker
                trade_time_datetime  # timestamp
            )
            cur.execute(insert_sql, trade_data)
            conn.commit()
    except Exception as e:
        logging.error(f"Error inserting into QuestDB: {e}")
        logging.error(traceback.format_exc())
    finally:
        connection_pool.putconn(conn)


def on_message(ws, message):
    """Handle incoming WebSocket messages."""
    logging.info("Received Message")
    try:
        data = json.loads(message)
        insert_into_questdb(data)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        logging.error(traceback.format_exc())
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        logging.error(traceback.format_exc())

def on_error(ws, error):
    """Handle WebSocket errors."""
    logging.error(f"WebSocket error: {error}")
    logging.error(traceback.format_exc())

def on_close(ws, close_status_code, close_msg):
    """Handle WebSocket closure."""
    logging.info("### Closed ###")
    logging.info(f"Close status code: {close_status_code}, message: {close_msg}")

def on_open(ws):
    """Handle opening of WebSocket connection."""
    logging.info("Connection opened")

def start_websocket(url):
    """Start a WebSocket connection."""
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = lambda ws: logging.info(f"Connection opened to {url}")
    ws.run_forever()

def shutdown(signum, frame):
    """Handle shutdown signals."""
    logging.info(f"Received shutdown signal: {signum}")
    connection_pool.closeall()
    logging.info("Connection pool closed")
    os._exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    create_questdb_table()

    # URLs for WebSocket connections
    urls = [
        "wss://stream.binance.com:9443/ws/btcusdt@trade",
        "wss://stream.binance.com:9443/ws/ethusdt@trade"
    ]

    # Start WebSocket connections in separate threads
    with ThreadPoolExecutor(max_workers=len(urls)) as executor:
        for url in urls:
            executor.submit(start_websocket, url)



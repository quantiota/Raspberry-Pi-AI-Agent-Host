import json
from websocket import create_connection, WebSocketConnectionClosedException
import psycopg2

# Connect to Coinbase Websocket
ws = create_connection("wss://ws-feed.exchange.coinbase.com")
ws.send(
    json.dumps(
        {
            "type": "subscribe",
            "product_ids": ["BTC-USD", "ETH-USD"],
            "channels": ["matches"],
        }
    )
)

# Connect to QuestDB
conn = psycopg2.connect(
    dbname="qdb",
    user="admin",
    password="quest",
    host="docker_host_ip_address",
    port="8812"
)

# Create the necessary table if it doesn't exist
with conn:
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coinbase_matches (
        symbol STRING, 
        id DOUBLE, 
        price DOUBLE,        
        size DOUBLE, 
        side STRING,
        type STRING,  
        maker_order_id STRING, 
        taker_order_id STRING, 
        sequence DOUBLE,
        timestamp TIMESTAMP 
    ) TIMESTAMP(timestamp) PARTITION BY DAY;
    """)

while True:
    try:
        data = json.loads(ws.recv())
        
        with conn:
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO coinbase_matches (symbol, id, price, size, side, type, maker_order_id, taker_order_id, sequence, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
            cursor.execute(insert_query, (data['product_id'], data['trade_id'], float(data['price']), float(data['size']), data['side'], data['type'], data['maker_order_id'], data['taker_order_id'], data['sequence'], data['time']))
            conn.commit()

    except WebSocketConnectionClosedException:
        print("Connection closed, retrying...")
        ws = create_connection("wss://ws-feed.exchange.coinbase.com")
    except Exception as e:
        print(e)
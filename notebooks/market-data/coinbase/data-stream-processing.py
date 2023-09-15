import json
from websocket import create_connection, WebSocketConnectionClosedException
import psycopg2
from math import pi, cos, sin
from datetime import datetime

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

# Create the necessary table if it doesn't exist, adding columns for cospath and sinpath
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
        timestamp TIMESTAMP,
        frequency DOUBLE,
        theta DOUBLE,
        cospath DOUBLE,
        sinpath DOUBLE
    ) TIMESTAMP(timestamp) PARTITION BY DAY;
    """)

previous_size = None
previous_time = None
theta = 0
cospath = 0
sinpath = 0

while True:
    try:
        data = json.loads(ws.recv())
        
        # If the message type is 'subscriptions', skip it
        if data.get('type') == 'subscriptions':
            continue


        current_size = float(data['size'])
        current_time = datetime.strptime(data['time'], '%Y-%m-%dT%H:%M:%S.%fZ')

        # Compute frequency w if previous data is available
        if previous_size is not None and previous_time is not None:
            delta_size = current_size - previous_size
            delta_time = (current_time - previous_time).total_seconds()

            if delta_time != 0:  # avoid division by zero
                frequency = (2 * pi / previous_size) * (delta_size / delta_time)

                # Update theta
                theta += frequency * delta_time
            else:
                frequency = 0

            # Update cospath and sinpath
            cospath += cos(theta)
            sinpath += sin(theta)

            # Insert into the database
            with conn:
                cursor = conn.cursor()
                insert_query = """
                    INSERT INTO coinbase_matches (symbol, id, price, size, side, type, maker_order_id, taker_order_id, sequence, timestamp, frequency, theta, cospath, sinpath)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """
                cursor.execute(insert_query, (data['product_id'], data['trade_id'], float(data['price']), current_size, data['side'], data['type'], data['maker_order_id'], data['taker_order_id'], data['sequence'], data['time'], frequency, theta, cospath, sinpath))
                conn.commit()

        # Store current data for the next iteration's calculation
        previous_size = current_size
        previous_time = current_time

    except WebSocketConnectionClosedException:
        print("Connection closed, retrying...")
        ws = create_connection("wss://ws-feed.exchange.coinbase.com")
    except Exception as e:
        print(e)
# Raspberry Pi AI Agent Host


## Simplified Summary

 The AI Agent Host can be complex given that it involves several aspects such as AI, edge computing, Docker, and Raspberry Pi. Let me attempt to simplify it:  

The AI Agent Host is essentially a setup that allows you to run AI applications directly on a Raspberry Pi, which is a small, low-cost computer often used in various tech projects.  

The AI Agent Host functions as a "host" for an AI "agent". These applications can interact with live data, coming from either online sources (APIs) or the Raspberry Pi's own sensors, to make decisions or predictions.  

Moreover, the AI Agent Host is designed to be modular, which means you can add or remove different components depending on what your project needs. For example, if you need a specific database or visualization tool, you can add it to the setup.  

Also, you can use this setup in combination with a powerful GPU server. So, if you have tasks that are too demanding for the Raspberry Pi, you can send them to this server for processing. This is made possible with the inclusion of CodeServer and remote connection to a JupyterHub installed on the GPU server.  

Finally, the AI Agent Host uses lightweight services like QuestDB and Grafana, suitable for the Raspberry Pi's limited resources, and is optimized for DietPi, a lightweight operating system ideal for single-board computers like Raspberry Pi.  

I hope this explanation helps simplify the concept of the AI Agent Host. If you have any further questions or if something is still unclear, feel free to ask!  

## Features

The AI Agent Host, designed specifically for AI development, offers several key features making it an ideal solution for Raspberry Pi 4 with 8GB RAM, especially when running DietPi OS:

1. **Modular Environment**: The AI Agent Host is built as a module-based system, allowing different components to be added or removed based on the requirements of the project. This is perfect for the customizable nature of Raspberry Pi. Furthermore, by adding an AI Agent container, the AI Agent Host can be transformed into an AI Agent Lab, expanding its capabilities for AI development and experimentation.

2. **Live Data Interaction**: With the ability to work with live data from both APIs and Raspberry Pi's own sensors, AI Agent Host becomes a powerful tool for real-time data analysis, modeling, and decision-making.

3. **Lightweight Services**: Services like QuestDB and Grafana used in the AI Agent Host are lightweight yet robust, making them suitable for the Raspberry Pi's limited hardware resources compared to larger servers.

4. **Remote Development Capabilities**: The inclusion of Code-Server allows you to connect to a remote JupyterHub installed on a powerful GPU Server when necessary, using Raspberry Pi as the Docker host.

5. **Data Handling and Visualization**: QuestDB for efficient data handling and Grafana for intuitive data visualization are integral for any AI and machine learning projects.

6. **Optimized for DietPi**: The AI Agent Host's compatibility with DietPi, a lightweight OS optimized for single-board computers like Raspberry Pi, ensures efficient use of the Raspberry Pi's hardware resources.

7. **Community Support**: With active communities for both Raspberry Pi and AI Agent Host, you can expect robust support and resources for your AI development projects.

These features make the AI Agent Host a dynamic, effective, and efficient environment for AI development on a Raspberry Pi 4 with 8GB RAM, especially for projects involving real-time or sensor data.


## AI Agent Host: A Novel Approach to Edge Computing

The AI Agent Host offers an innovative setup, connecting edge devices like the Raspberry Pi to a JupyterHub on a remote GPU server. This unique configuration, part of a broader trend known as edge computing, enables real-time data analysis and decision-making on the edge while offloading computationally intensive tasks to a GPU server in the cloud.

While this specific setup is not commonly seen or standardized, it adds significant value to fields that require real-time data analysis and decision-making capabilities at the edge. Potential applications include autonomous vehicles, Internet of Things (IoT), robotics, and more.

One of the primary challenges in edge computing is developing an infrastructure that allows for seamless communication and integration between edge devices and cloud servers. The AI Agent Host provides a powerful solution to this challenge, offering a framework that could potentially standardize these interactions.

As the AI industry continues to evolve rapidly, this innovative approach may become more commonplace. The AI Agent Host is at the forefront of this technological development, paving the way for new use cases and implementations.

Please note that while we strive to keep this document up-to-date, the field of AI is continuously evolving. For the latest information and developments, we recommend staying active in relevant online communities and keeping up with the latest research.

Real-time Synchronization of Coinbase Trades to QuestDB using WebSockets in Python
This script achieves real-time synchronization between Coinbase, a popular cryptocurrency exchange, and QuestDB, a high-performance, time-series database. Initially, it establishes a connection to Coinbase's Websocket feed and subscribes to match events for BTC-USD and ETH-USD trading pairs. Concurrently, it connects to a QuestDB instance running on a Docker host. If not already present, a table named 'coinbase_matches' is created to store trading match details. The script continuously listens for new data from Coinbase, and upon receiving, inserts the data into the 'coinbase_matches' table in QuestDB. If the websocket connection closes unexpectedly, it attempts a reconnection. Additionally, if any other unexpected errors occur during data retrieval or insertion, the script prints the error for debugging purposes.

Real-time Synchronization of Coinbase Trades to QuestDB using QuestDB with Producer/Consumer Pattern in Julia Notebook.
The Julia notebook sets up a producer/consumer pattern to build a cryptocurrency trade database using QuestDB. The Trade struct is created to store trade data, with a RemoteChannel (from the Distributed package) created to store trades. The WebSocket feed from CoinbasePro is connected, and the relevant fields from incoming JSON objects are parsed and stored as trades in the RemoteChannel. The notebook sets up a QuestDB connection and creates a table with the columns corresponding to the Trade struct. A consumer process reads from the RemoteChannel and writes data to the QuestDB table. The end result is a database of trades that can be queried for further analysis.

Set up parameter:

using Sockets
function save_trades_quest(trades)
    cs = connect("docker_host_ip_address", 9009)
    while true
        payload = build_payload(take!(trades))
        write(cs, (payload))
    end
    close(cs)
end
Remember to replace <docker_host_ip_address> with the actual IP address of the Docker host where your server is running.

Update the jupyter extension to the pre-release version and then click on the reload button.

To establish a remote JupyterHub connection from code-server, refer to this Tutorial for guidance. Create an API token and use the provided URL:

https://<your-hub-url>/user/<your-hub-user-name>/?token=<your-token>
Configure port forwarding.
If you are using JupyterHub on a remote server, you'll need to configure port forwarding either on the server itself or on any intermediate network devices, such as routers or firewalls.

Server-level port forwarding: Configure port forwarding on the server so that it forwards incoming connections on port 9009 to the Docker host's IP address and the same port (9009).

Network device port forwarding: If there are intermediate network devices between the JupyterHub server and the Docker host, configure port forwarding on these devices to route traffic from the desired source IP and port to the Docker host's IP and port (9009).

After configuring the port forwarding, you should test it. You can do this by attempting to connect to the Docker host's IP address on port 9009 from the JupyterHub server. For example, you can use the following command:

telnet docker_host_ip_address 9009

Remember to replace <docker_host_ip_address> with the actual IP address of the Docker host where your server is running.

Run the Data Stream Processing Notebook
Click on the 'Run All' button in the toolbar and then check the Grafana dashboard for real-time visualization of market data.

SQL Queries for Real-Time Analytics and Aggregations on Trades Table in QuestDB
SQL query written for QuestDB, a time-series database optimized for high-performance querying and real-time analytics. The queries select data from a "trades" table, specifically focusing on the timestamp, price, and size columns. They perform various aggregations such as capturing the first price for each 1-second interval for Ethereum (ETH) and Bitcoin (BTC), as well as summing up the trading volume (size) for Ethereum (ETH). The WHERE clause filters the dataset to include only trades for the symbols "ETH-USD" and "BTC-USD" with timestamps within the last day. The queries sample the data in 1-second intervals, aligned to the calendar, making them ideal for high-frequency time-series analysis. The result set includes columns for the Ethereum and Bitcoin prices and also provides the summed trading volume for Ethereum.

Grafana Dashboard for Time-Series Data Visualization of ETH (Ethereum) and BTC (Bitcoin) with QuestDB Data Source and SQL Query
JSON dashboard file for Grafana, a platform for monitoring and visualizing metrics from various data sources. The dashboard has an ID of 1 and showcases time-series data for both ETH (Ethereum) and BTC (Bitcoin). The data is pulled from a QuestDB data source with the use of SQL queries that fetch metrics like real-time prices for the past 24 hours. The dashboard features two panels: one for displaying the prices of ETH and BTC, and another focusing on the price and volume of ETH.

dashboard coinbase

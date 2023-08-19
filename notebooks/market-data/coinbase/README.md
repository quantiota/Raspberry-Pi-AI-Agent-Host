## Building a Cryptocurrency Trade Database using QuestDB with Producer/Consumer Pattern in Julia Notebook.
The Julia notebook sets up a producer/consumer pattern to build a cryptocurrency trade database using QuestDB. The Trade struct is created to store trade data, with a RemoteChannel (from the Distributed package) created to store trades. The WebSocket feed from CoinbasePro is connected, and the relevant fields from incoming JSON objects are parsed and stored as trades in the RemoteChannel. The notebook sets up a QuestDB connection and creates a table with the columns corresponding to the Trade struct. A consumer process reads from the RemoteChannel and writes data to the QuestDB table. The end result is a database of trades that can be queried for further analysis.

Set up parameter:


```
using Sockets
function save_trades_quest(trades)
    cs = connect("docker_host_ip_address", 9009)
    while true
        payload = build_payload(take!(trades))
        write(cs, (payload))
    end
    close(cs)
end
```

1. Remember to replace **<docker_host_ip_address>** with the actual IP address of the Docker host where your server is running.

2. Update the jupyter extension to the pre-release version and then click on the reload button.

3. To establish a remote JupyterHub connection from code-server, refer to this [Tutorial](https://code.visualstudio.com/docs/datascience/jupyter-notebooks#_connect-to-a-remote-jupyter-server) for guidance. Create an [API token](https://jupyterhub.readthedocs.io/en/stable/howto/rest.html#create-an-api-token) and use the provided URL:

```
https://<your-hub-url>/user/<your-hub-user-name>/?token=<your-token>
```

3. Configure port forwarding.

 If you are using JupyterHub on a remote server, you'll need to configure port forwarding either on the server itself or on any intermediate network devices, such as routers or firewalls.

- **Server-level port forwarding**: Configure port forwarding on the server so that it forwards incoming connections on port 9009 to the Docker host's IP address and the same port (9009).

- **Network device port forwarding**: If there are intermediate network devices between the JupyterHub server and the Docker host, configure port forwarding on these devices to route traffic from the desired source IP and port to the Docker host's IP and port (9009).

After configuring the port forwarding, you should test it. You can do this by attempting to connect to the Docker host's IP address on port 9009 from the JupyterHub server. For example, you can use the following command:

```
telnet docker_host_ip_address 9009

```

Remember to replace **<docker_host_ip_address>** with the actual IP address of the Docker host where your server is running.


3. Run the Data Stream Processing Notebook

Click on the '**Run All**' button in the toolbar and then check the Grafana dashboard for real-time visualization of market data.



## SQL Query for Real-Time Analytics and Aggregations on Trades Table in QuestDB
SQL query written for QuestDB, a relational database management system designed for high-performance querying and real-time analytics. The query selects various columns from a "trades" table, including the timestamp, price, and size, and performs aggregations such as finding the first and last prices and sizes, as well as calculating the percentage change. The WHERE clause filters the results to only include trades for the "ETH-USD" symbol with a timestamp within the last day. The query also samples the results at 1-minute intervals aligned to the calendar. The result set includes columns for the open and close prices, volume, and cosine of the sum of the sizes.

## Grafana Dashboard for Time-Series Data Visualization of ETH (Ethereum) with QuestDB Data Source and SQL Query
JSON dashboard file for Grafana, a platform for visualizing and analyzing data from various sources. The dashboard has an ID of 2 and displays time-series data for ETH (Ethereum). The data is retrieved from a QuestDB data source using a SQL query that retrieves information such as the opening and closing prices, volume, and percentage change for the past day. The dashboard contains options for tooltip display and legend placement, and field configurations for customizing the visualization of the data. The targets section specifies the data source and SQL query to be executed to retrieve the data.

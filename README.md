# Raspberry Pi AI Agent Host

The [AI Agent Host](https://github.com/quantiota/AI-Agent-Host), designed specifically for AI development, offers several key features making it an ideal solution for Raspberry Pi 4 with 8GB RAM, especially when running DietPi OS:

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


## Usage

To test the AI Agent Host, follow these steps:

1. Set up or use an existing environment with Docker installed.

Run dietpi-software from the command line.

```
dietpi-software
```

Choose Browse Software and select Docker Compose, Docker and Git. Finally select Install.
DietPi will do all the necessary steps to install and start these software items.


```

             │  [*] 134  Docker Compose: Manage multi-container Docker applications                 
             │  [ ] 142  MicroK8s: The simplest production-grade upstream K8s, light and focused     
             │  [*] 162  Docker: Build, ship, and run distributed applications    

             |  [*] 17   Git: Clone and manage Git repositories locally                                  

```

2. Clone the AI Agent Host repository and navigate to the docker directory.

```
git clone https://github.com/quantiota/AI-Agent-Host.git
cd AI-Agent-Host/docker

```

## Prerequisites

**Note**: A **fully qualified domain name**  (FQDN) is mandatory for running any notebooks from VSCode over **HTTPS**.


### 1 Generate Certificates with Certbot

We will use the Certbot Docker image to generate certificates. This service will bind on ports 80 and 443, which are the standard HTTP and HTTPS ports, respectively. It will also bind mount some directories for persistent storage of certificates and challenge responses. 

If you want to obtain separate certificates for each subdomain, you will need to run the **certbot certonly** command for each one. You can specify the subdomain for which you want to obtain a certificate with the -d option, like this:

```
docker compose -f init.yaml run certbot certonly -d vscode.yourdomain.tld
```


```
docker compose -f init.yaml run certbot certonly -d questdb.yourdomain.tld
```


```
docker compose -f init.yaml run certbot certonly -d grafana.yourdomain.tld
```

**Important:** Replace **'yourdomain.tld'** with your actual domain in the commands above.

Please note that the **certonly** command will obtain the certificate but not install it. You will have to configure your Nginx service to use the certificate. Additionally, make sure that your domain points to the server on which you're running this setup, as Let's Encrypt validates domain ownership by making an HTTP request.

Also, remember to periodically renew your certificates, as Let's Encrypt's certificates expire every 90 days. You can automate this task by setting up a cron job or using a similar task scheduling service.


```
# /etc/cron.d/certbot: crontab entries for the certbot package (5 am, every monday)
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

 0 5 * * 1 docker compose run certbot renew

```

### 2 Setup Environment Variables

Firstly, you will want to create an '**.env**' file in the docker folder with the following variables:

```

# VSCode
PASSWORD=yourpassword

# Grafana
GRAFANA_QUESTDB_PASSWORD=quest

# QuestDB
QDB_PG_USER=admin
QDB_PG_PASSWORD=quest

```
and to define your domain name in the '**nginx.env**' file:

```
    # nginx/nginx.env

    DOMAIN=yourdomain
```

Remember to replace the placeholders with your actual domain, passwords, and usernames. 

The environment variables will be replaced directly within the Nginx configuration file when the Docker services are started.


### 3 Generate dhparam.pem file

The **dhparam.pem** file is used for Diffie-Hellman key exchange, which is part of establishing a secure TLS connection. You can generate it with OpenSSL. Here's how to generate a 2048-bit key:

```
openssl dhparam -out ./nginx/certs/dhparam.pem 2048
```

Generating a dhparam file can take a long time. For a more secure (but slower) 4096-bit key, simply replace 2048 with 4096 in the above command.

### 4 Generate .htpasswd file for QuestDB 

The user/password are the default one: admin:admin

The **.htpasswd** file is used for basic HTTP authentication. You can change it using the **htpasswd** utility, which is part of the Apache HTTP Server package. Here's how to create an **.htpasswd** file with a user named **yourusername**:
```
htpasswd -c ./nginx/.htpasswd yourusername
```
This command will prompt you for the password for **yourusername**. The **-c** flag tells **htpasswd** to create a new file. **Caution**: Using the **-c** flag will overwrite any existing **.htpasswd** file. 

If **htpasswd** is not installed on your system, you can install it with **apt** on Ubuntu:

```
sudo apt-get install apache2-utils
```

### 5 Launch the AI Agent Host using the provided docker-compose configuration.
After completing these steps, you can bring up the Docker stack using the following command:

```
docker compose up --build -d
```
This will start all services as defined in your **docker-compose.yaml** file.


## Usage

### 1 Once the services are up and running, you can access the AI Agent Host interfaces:

- QuestDB: Visit https://questdb.domain.tld in your web browser.
- Grafana: Visit https://grafana.domain.tld in your web browser.
- Code-Server: Visit https://vscode.domain.tld in your web browser.

### 2 To connect the AI Agent Host to a remote JupyterHub environment from Code-Server:

1. Set up or use an existing remote JupyterHub that includes the necessary dependencies for working with your notebooks and data.

2. Connect to the remote JupyterHub environment from within the Code-Server interface provided by the AI Agent Host

### 3 Start working with your notebooks and data, using the pre-installed tools and libraries included in your remote environment.

You can also run the existing notebook in the project folder within VSCode. Follow this [tutorial](https://github.com/quantiota/AI-Agent-Host/tree/main/notebooks/market-data/coinbase) for guidance.




## Frequently Asked Questions

1. **What is the AI Agent Host?**
   The AI Agent Host is a Dockerized environment designed for AI development. It's built on a modular system that allows different components to be added or removed based on the requirements of the project.

2. **Why use the AI Agent Host on a Raspberry Pi 4 8GB?**
   The AI Agent Host is lightweight yet powerful, making it suitable for the Raspberry Pi's limited hardware resources. It's designed to work with live data from both APIs and Raspberry Pi's own sensors, making it a powerful tool for real-time data analysis, modeling, and decision-making.

3. **Which services does the AI Agent Host include?**
   The AI Agent Host includes services such as Code-Server (a code editor), Grafana (a visualization tool), and QuestDB (a database). Additional services can be added or removed as needed.

4. **What do I need to connect to the Code-Server from a browser with HTTPS?**
   A fully qualified domain name (FQDN) is necessary to connect to the Code-Server from a browser using HTTPS. The FQDN ensures that the secure connection is correctly established.

5. **Can the AI Agent Host on a Raspberry Pi be used in combination with a remote JupyterHub installed on a GPU server?**

   Yes, this is one of the unique and powerful features of the AI Agent Host setup. You can use the AI Agent Host installed on a Raspberry Pi for real-time data analysis and decision making at the edge, while also connecting remotely to a JupyterHub installed on a GPU server for handling computationally intensive tasks. This innovative setup opens up new possibilities for AI development, especially in fields like IoT and edge computing.

6. **Can I use the AI Agent Host with other versions of the Raspberry Pi?**
   While the AI Agent Host has been tested and works well on the Raspberry Pi 4 8GB model, it should theoretically work on other models with sufficient hardware capabilities. However, performance may vary.

7. **Which operating systems are compatible with the AI Agent Host?**
   The AI Agent Host has been tested and found to be compatible with DietPi. Compatibility with other Linux distributions hasn't been extensively tested.

8. **Can I add my own services to the AI Agent Host?**
   Absolutely! The AI Agent Host is designed to be modular, allowing you to add or remove Docker containers as needed. This means you can customize the environment to include the exact tools and services that best suit your specific project's needs.

9. **What if I need help or support with the AI Agent Host?**
   There are active communities for both Raspberry Pi and AI Agent Host where you can expect robust support and resources for your AI development projects.


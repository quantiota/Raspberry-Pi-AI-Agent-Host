## How to test

The AI Agent Host was tested on DietPi installed on a Raspberry Pi 4 8GB. No other Linux distributions have been tested, but the instructions should be reasonably straightforward to adapt.

When testing the AI Agent Host, you can expect several types of test results depending on the specific aspects you are testing. Here are some common types of test results you might encounter:

1. **Successful deployment**: This result indicates that your Docker Compose configuration successfully deploys and starts all the services defined in your configuration file. It means that the containers are running, and the services are accessible as expected.

2. **Connectivity tests**: These tests verify whether the services within your Docker Compose setup can communicate with each other. They ensure that the networking between the containers is properly configured, and the services can interact as intended.

3. **Functional tests**: These tests assess the functionality of the services running within the Docker Compose setup. For example, if you have a web application container, you might test whether it responds correctly to HTTP requests, processes user input, and produces the expected output. Additionally, you can add the possibility to run notebooks as part of your functional tests. For instance, if your Docker Compose setup includes a Jupyter Notebook, you can design tests that execute specific notebook cells or workflows and verify the expected results. This allows you to validate the functionality of your notebooks and ensure that they produce the desired outcomes when running within the Docker Compose environment. Running notebooks as functional tests can help you ensure the correctness and reliability of your data processing, analysis, or machine learning workflows encapsulated in the notebooks within the Docker Compose environment.

4. **Integration tests**: These tests evaluate how well the different services integrated within your Docker Compose configuration work together. They validate whether the services can cooperate and exchange information or perform complex tasks as expected.

5. **Performance tests**: These tests focus on assessing the performance characteristics of your Docker Compose setup. They might involve measuring response times, throughput, resource utilization, or scalability under different workloads or stress conditions.

6. **Error handling tests**: These tests check how your Docker Compose configuration handles various error scenarios. For example, you might deliberately simulate a service failure and observe if the system gracefully recovers or if error conditions are properly handled.

7. **Security tests**: These tests assess the security posture of your Docker Compose setup. They might involve vulnerability scanning, penetration testing, or checking for misconfigurations that could expose your services to potential threats.

The specific test results you will obtain depend on the test cases you execute and the quality of your Docker Compose configuration. It's important to design and execute a comprehensive set of tests to ensure the reliability, performance, and security of your Dockerized application.

## Getting Started

To test the AI Agent Host, follow these steps:

1. Set up or use an existing environment with Docker installed.

With root:dietpi login credentials:

Run dietpi-software from the command line.

```
dietpi-software
```

Choose Browse Software and select I2C, Prometheus Node Exporter, Docker Compose, Docker and Git. Finally select Install.
DietPi will do all the necessary steps to install and start these software items.


```
             |  [*] 72  I2C: enables support for I2C based hardware

             |  [*] 99   Prometheus Node Exporter: Prometheus exporter for hardware and OS metrics

             │  [*] 134  Docker Compose: Manage multi-container Docker applications                 
                 
             │  [*] 162  Docker: Build, ship, and run distributed applications    

             |  [*] 17   Git: Clone and manage Git repositories locally                                  

```

2. Clone the AI Agent Host repository and navigate to the docker directory.

with dietpi:dietpi login credentials:

```
umask 0002
git clone https://github.com/quantiota/Raspberry-Pi-AI-Agent-Host.git
umask 0022
cd AI-Agent-Host/docker

```
## Prerequisites

**Note**: A **fully qualified domain name**  (FQDN) is mandatory for running any notebooks from VSCode over **HTTPS**.


### 1 Generate Certificates with Certbot

We will use the Certbot Docker image to generate certificates. This service will bind on ports 80 and 443, which are the standard HTTP and HTTPS ports, respectively. It will also bind mount some directories for persistent storage of certificates and challenge responses. 

If you want to obtain separate certificates for each subdomain, you will need to run the **certbot certonly** command for each one. You can specify the subdomain for which you want to obtain a certificate with the -d option, like this:

```
sudo docker compose -f init.yaml run certbot certonly -d vscode.yourdomain.tld
```


```
sudo docker compose -f init.yaml run certbot certonly -d questdb.yourdomain.tld
```


```
sudo docker compose -f init.yaml run certbot certonly -d grafana.yourdomain.tld
```

**Important:** Replace **'yourdomain.tld'** with your actual domain in the commands above.

Please note that the **certonly** command will obtain the certificate but not install it. You will have to configure your Nginx service to use the certificate. Additionally, make sure that your domain points to the server on which you're running this setup, as Let's Encrypt validates domain ownership by making an HTTP request.

Also, remember to periodically renew your certificates, as Let's Encrypt's certificates expire every 90 days. You can automate this task by setting up a cron job or using a similar task scheduling service.


```
# /etc/cron.d/certbot: crontab entries for the certbot package (5 am, every monday)
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

 0 5 * * 1 sudo docker compose run certbot renew

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
sudo openssl dhparam -out ./nginx/certs/dhparam.pem 2048
```

Generating a dhparam file can take a long time. For a more secure (but slower) 4096-bit key, simply replace 2048 with 4096 in the above command.

### 4 Generate .htpasswd file for QuestDB 

The user/password are the default one: admin:admin

The **.htpasswd** file is used for basic HTTP authentication. You can change it using the **htpasswd** utility, which is part of the Apache HTTP Server package. Here's how to create an **.htpasswd** file with a user named **yourusername**:
```
sudo htpasswd -c ./nginx/.htpasswd yourusername
```
This command will prompt you for the password for **yourusername**. The **-c** flag tells **htpasswd** to create a new file. **Caution**: Using the **-c** flag will overwrite any existing **.htpasswd** file. 

If **htpasswd** is not installed on your system, you can install it with **apt** on Ubuntu:

```
sudo apt-get install apache2-utils
```

### 5 Configure the Dockerfile for your specific needs.

When working with Docker, the ***Dockerfile*** acts as a blueprint for building containerized applications. While it's possible to utilize a standard or generic **Dockerfile**, it's often essential to tailor it to your project's unique demands, especially when working with Python applications and their dependencies. Customizing your **Dockerfile** allows you to effectively manage dependencies using a [**requirements.txt**](https://github.com/quantiota/Raspberry-Pi-AI-Agent-Host/blob/main/docker/vscode/requirements.txt) file, streamlining and tracking the exact package versions your project requires.


### 6 Set up device mappings

Before initiating your services with Docker Compose, it's crucial to set up [device mappings](https://github.com/quantiota/Raspberry-Pi-AI-Agent-Host/tree/main/docs/weather-station), especially if any of your services require direct access to hardware devices on the host machine.

In our configuration
```
services:
  vscode:
    devices:
      - "/dev/i2c-1:/dev/i2c-1"

```
We've explicitly mapped the **/dev/i2c-1** device from the host to **/dev/i2c-1** inside the container. By doing so, when the service **vscode** is launched, it will have the necessary permissions to directly interface with the I2C device as if the service were running directly on the host.

Failing to set up this mapping before running **docker compose up** might lead to issues, as the service won't be able to access or communicate with the desired device, potentially causing errors or incomplete functionality.

It's essential to map these devices in the Docker Compose configuration **before** launching the service to ensure that the required hardware interactions function seamlessly within the containerized environment.


### 7 Launch the AI Agent Host using the provided docker-compose configuration.
After completing these steps, you can bring up the Docker stack using the following command:

```
sudo docker compose up --build -d
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




## References


1. Connect to a JupyterHub from Visual Studio Code. [Visual Studio Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks#_connect-to-a-remote-jupyter-server)

2. Create an API Token. [JupyterHub](https://jupyterhub.readthedocs.io/en/stable/howto/rest.html#create-an-api-token)

3. [Visual Studio Code](https://code.visualstudio.com/)

4. [QuestDB - The Fastest Open Source Time Series Database](https://questdb.io/)

5. [Grafana - The open observability platform](https://grafana.com/)

6. [Langchain](https://python.langchain.com)


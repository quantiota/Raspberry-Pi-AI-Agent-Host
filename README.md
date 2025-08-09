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


## Getting Started 

To use the AI Agent Host, follow these steps:

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
2. Reboot

```
sudo shutdown -r now
```

3. Clone the AI Agent Host repository and navigate to the docker directory.

with dietpi:dietpi login credentials:

```
umask 0002
git clone https://github.com/quantiota/Raspberry-Pi-AI-Agent-Host.git
umask 0022
cd Raspberry-Pi-AI-Agent-Host/docker

```

Then follow the prerequisites section in this [Tutorial](https://github.com/quantiota/Raspberry-Pi-AI-Agent-Host/tree/main/installation) for guidance.


## Usage

### 1 Once the services are up and running, you can access the AI Agent Host interfaces:

- QuestDB: Visit https://questdb.domain.tld in your web browser.
- Grafana: Visit https://grafana.domain.tld in your web browser.
- Code-Server: Visit https://vscode.domain.tld in your web browser.

### 2 To connect the AI Agent Host to a remote JupyterHub environment from Code-Server:

1. Set up or use an existing remote JupyterHub that includes the necessary dependencies for working with your notebooks and data.

2. Connect to the remote JupyterHub environment from within the Code-Server interface provided by the AI Agent Host

### 3 Start working with your notebooks and data, using the pre-installed tools and libraries included in your remote environment.

You can also run the existing notebooks in the project folder within VSCode. 

[Weather Station](https://github.com/quantiota/Raspberry-Pi-AI-Agent-Host/tree/main/notebooks/weather-station) 

[GPS Tracker](https://github.com/quantiota/Raspberry-Pi-AI-Agent-Host/tree/main/notebooks/vehicle-tracking) 


## AI Agent Hosting Example: Claude Code

This example shows how to add an **AI agent** to the Raspberry Pi AI Agent Host **without changing** the core stack. The agent runs in its own service and talks **directly** to Code-Server, QuestDB and Grafana over the internal Docker network, preserving the Host’s role as an **agentic environment**.

Claude Code is functioning like a **human developer with terminal access** — using `curl`, database clients, and file operations rather than AI-specific middleware layers.  
The *agentic* behavior comes from its ability to autonomously chain these basic system tools together, not from specialized AI agent frameworks.

### What This Adds
- Updated `docker/vscode/Dockerfile` to include Claude Code installation.
- Updated `docker/docker-compose.yaml` to mount persistent config/data volumes for Claude Code.
- instructions `README.md` to run Claude Code

### Folder Layout

```
└── 📁claude-code
    └── 📁docker
        └── 📁vscode
            ├── Dockerfile
        ├── docker-compose.yaml
    └── README.md
```



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
   The AI Agent Host has been tested and found to be compatible with DietPi and Raspberry Pi OS 64 Bit installed on a Raspberry Pi 4 8GB. Compatibility with other Linux distributions hasn't been extensively tested.

8. **Can I add my own services to the AI Agent Host?**
   Absolutely! The AI Agent Host is designed to be modular, allowing you to add or remove Docker containers as needed. This means you can customize the environment to include the exact tools and services that best suit your specific project's needs.

9. **What if I need help or support with the AI Agent Host?**
   There are active communities for both Raspberry Pi and AI Agent Host where you can expect robust support and resources for your AI development projects.


### AI Agent Host Architecture Diagram

 ![AI Agent Host diagram](./ai-agent-host-diagram.png)
 
:pencil: High resolution diagram [Application architecture diagram](https://raw.githubusercontent.com/quantiota/Raspberry-Pi-AI-Agent-Host/master/ai-agent-host-diagram.png)


   ## References


1. Connect to a JupyterHub from Visual Studio Code. [Visual Studio Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks#_connect-to-a-remote-jupyter-server)

2. Create an API Token. [JupyterHub](https://jupyterhub.readthedocs.io/en/stable/howto/rest.html#create-an-api-token)

3. [Visual Studio Code](https://code.visualstudio.com/)

4. [QuestDB - The Fastest Open Source Time Series Database](https://questdb.io/)

5. [Grafana - The open observability platform](https://grafana.com/)

6. [Langchain](https://python.langchain.com)




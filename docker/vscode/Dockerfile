# Use the specified base image
FROM codercom/code-server:4.16.1

# Switch to root user for permissions
USER root

# Update, and install python3-dev and python3-pip
RUN apt-get update && apt-get install -y python3-dev python3-pip

# Copy the requirements file to the container
COPY requirements.txt /tmp/

# Install Python packages from the requirements file
RUN python3 -m pip install -r /tmp/requirements.txt

# Additional setup (e.g., group and user modifications)
RUN groupadd -g 995 i2cgroup
RUN usermod -aG i2cgroup coder

# Switch to coder user
USER coder

# Install the Visual Studio Code extensions
RUN code-server --install-extension ms-toolsai.jupyter \
                --install-extension ms-toolsai.vscode-jupyter-powertoys \
                --install-extension ms-python.python

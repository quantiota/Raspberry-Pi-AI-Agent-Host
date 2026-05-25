# Use the specified base image
FROM codercom/code-server:4.113.1

# Switch to root user for permissions
USER root

# Update, and install python3-dev, python3-pip, and curl, then clean up apt cache
RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    python3-venv \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Python virtual environment (PEP 668 compliant) ----
RUN python3 -m venv /opt/venv

# Make venv the default Python
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip inside venv
RUN pip install --upgrade pip

# Copy requirements and install them
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Additional setup (e.g., group and user modifications)
# Replace 995 with the gid you find for the I2C Interface
RUN groupadd -g 995 i2cgroup
RUN usermod -aG i2cgroup coder


# Add the coder user to the dialout group for GPS communication with serial port /dev/ttyUSB*
RUN usermod -aG dialout coder

# Switch to coder user
USER coder


# Install the Visual Studio Code extensions
RUN code-server --install-extension ms-toolsai.jupyter@2025.9.1 \
                --install-extension ms-toolsai.vscode-jupyter-powertoys \
                --install-extension ms-python.python


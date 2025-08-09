# Use the specified base image
FROM codercom/code-server:4.16.1

# Switch to root user for permissions
USER root

# Update, and install python3-dev, python3-pip, and Node.js
RUN apt-get update && apt-get install -y python3-dev python3-pip curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Copy the requirements file to the container
COPY requirements.txt /tmp/

# Install Python packages from the requirements file
RUN python3 -m pip install -r /tmp/requirements.txt

# Additional setup (e.g., group and user modifications)
# Replace 995 with the gid you find for the I2C Interface
RUN groupadd -g 995 i2cgroup
RUN usermod -aG i2cgroup coder

# Create and set permissions for Claude directories
RUN mkdir -p /home/coder/.claude /home/coder/.config/claude-code && \
    chown -R coder:coder /home/coder/.claude /home/coder/.config && \
    chmod -R u+rwX /home/coder/.claude /home/coder/.config

# Add the coder user to the dialout group for GPS communication with serial port /dev/ttyUSB*
RUN usermod -aG dialout coder

# Switch to coder user
USER coder

# Configure npm global directory and install Claude Code
RUN mkdir -p ~/.npm-global && \
    npm config set prefix '~/.npm-global' && \
    echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc && \
    npm install -g @anthropic-ai/claude-code

# Install the Visual Studio Code extensions
RUN code-server --install-extension ms-toolsai.jupyter@2023.4.1001091014 \
                --install-extension ms-toolsai.vscode-jupyter-powertoys \
                --install-extension ms-python.python

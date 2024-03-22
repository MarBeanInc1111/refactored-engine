# Use an official Python 3.11 image as the base image
FROM python:3.11-slim

# Update package lists and install wget for downloading the ttyd binary
RUN apt-get update && apt-get install -y wget && \
    xz-utils && \

    # Download the precompiled ttyd binary from GitHub releases
    wget https://github.com/tsl0922/ttyd/releases/download/1.6.3/ttyd.x86_64.tar.xz && \
    tar xf ttyd.x86_64.tar.xz -C /usr/bin && \

    # Make the ttyd binary executable
    chmod +x /usr/bin/ttyd && \

    # Remove wget, xz-utils and clean up package lists
    apt-get remove -y wget xz-utils && apt-get autoremove -y && \

    # Remove package lists to save disk space
    rm -rf /var/lib/apt/lists/*

# Set the NVM_DIR environment variable for the Node Version Manager
ENV NVM_DIR /root/.nvm

# Install Node.js using the nvm (Node Version Manager)
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && nvm install node && nvm use node

# Set the working directory for the application
WORKDIR /usr/src/app

# Copy the current directory (i.e., the root directory of the repository) to the working directory
COPY . .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create a virtual environment for the application
RUN python -m venv pilot-env

# Activate the virtual environment
ENV PATH=/usr/src/app/pilot-env/bin:$PATH

# Install Python dependencies from requirements.txt within the virtual environment
RUN pip install -r requirements.txt

# Set environment variables
ENV NODE_ENV=production
ENV PORT=8000

# Expose the port
EXPOSE 8000

# Start the application
CMD ["npm", "start"]

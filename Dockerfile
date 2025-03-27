FROM nvidia/cuda:12.4.1-base-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV CMDARGS="--listen"

# Install dependencies in one RUN step to reduce layers and avoid unnecessary cache
RUN apt-get update -y && \
    apt-get install -y \
    curl \
    libgl1 \
    libglib2.0-0 \
    python3-pip \
    python-is-python3 \
    git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements_docker.txt requirements_versions.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements_docker.txt -r /tmp/requirements_versions.txt && \
    rm -f /tmp/requirements_docker.txt /tmp/requirements_versions.txt

# Install xformers
RUN pip install --no-cache-dir xformers==0.0.23 --no-dependencies

# Download and install frpc for gradio
RUN curl -fsL -o /usr/local/lib/python3.10/dist-packages/gradio/frpc_linux_amd64_v0.2 \
    https://cdn-media.huggingface.co/frpc-gradio-0.2/frpc_linux_amd64 && \
    chmod +x /usr/local/lib/python3.10/dist-packages/gradio/frpc_linux_amd64_v0.2

# Create a non-root user and directories for app and data
RUN adduser --disabled-password --gecos '' user && \
    mkdir -p /content/app /content/data && \
    chown -R user:user /content

# Copy the entrypoint script and set appropriate permissions
COPY entrypoint.sh /content/
RUN chmod +x /content/entrypoint.sh

# Set working directory and switch to non-root user
WORKDIR /content
USER user

# Copy the application code and models directory
COPY --chown=user:user . /content/app
RUN mv /content/app/models /content/app/models.org

# Set the entrypoint command
CMD ["sh", "-c", "/content/entrypoint.sh ${CMDARGS}"]

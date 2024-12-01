FROM python:3.10-slim

# Set working directory early
WORKDIR /workspace

# Copy requirements first
COPY .devcontainer/requirements.txt /workspace/

# Install system dependencies
RUN apt-get update && apt-get install -y git curl build-essential sudo && rm -rf /var/lib/apt/lists/*

# Set up non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install Python requirements
RUN pip3 install -r requirements.txt

# Copy the rest of the application
COPY . /workspace

# Set workspace permissions
RUN chown -R $USERNAME:$USERNAME /workspace

# Set the default shell and user
ENV SHELL /bin/bash
USER $USERNAME
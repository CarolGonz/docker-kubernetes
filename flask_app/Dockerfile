FROM ubuntu:18.04

# Specify accept-bind-to-port LABEL for inference pipelines to use SAGEMAKER_BIND_TO_PORT
# https://docs.aws.amazon.com/sagemaker/latest/dg/inference-pipeline-real-time.html
LABEL com.amazonaws.sagemaker.capabilities.accept-bind-to-port=true

# See http://bugs.python.org/issue19846
# Set locale and environment variables
ENV LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=TRUE \
    PYTHONDONTWRITEBYTECODE=TRUE \
    LD_LIBRARY_PATH='/usr/local/lib:$LD_LIBRARY_PATH'

# ENV PATH="/opt/program:${PATH}"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        gnupg2 \
        ca-certificates \
        emacs \
        git \
        wget \
        vim \
        libbz2-dev \
        liblzma-dev \
        libffi-dev \
        build-essential \
        zlib1g-dev \
        openssl \
        libssl1.1 \
        libreadline-gplv2-dev \
        libncursesw5-dev \
        libssl-dev \
        libsqlite3-dev \
        tk-dev \
        libgdbm-dev \
        libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Install nginx and njs module
RUN curl -s http://nginx.org/keys/nginx_signing.key | apt-key add - \
    && echo 'deb http://nginx.org/packages/ubuntu/ bionic nginx' >> /etc/apt/sources.list \
    && apt-get update && apt-get install -y --no-install-recommends \
        nginx \
        nginx-module-njs \
    && rm -rf /var/lib/apt/lists/*


# Install python3.9
ARG PYTHON=python3.9
ARG PYTHON_PIP=python3-pip
ARG PIP=pip3
ARG PYTHON_VERSION=3.9.15

RUN wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz \
    && tar -xvf Python-$PYTHON_VERSION.tgz \
    && cd Python-$PYTHON_VERSION \
    && ./configure && make && make install \
    && make && make install && rm -rf ../Python-$PYTHON_VERSION* \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && ln -s /usr/bin/pip3 /usr/bin/pip

COPY requirements.txt /requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --no-cache-dir -r /requirements.txt

WORKDIR /opt/program

# Copy source code
COPY src/ /opt/program

# Set files permissions
RUN chmod -R 777 /opt/program

# Set entrypoint
ENTRYPOINT ["python3", "routes.py"]

# Use Ubuntu latest as base image
FROM ubuntu:latest

# Prevent timezone prompt during package installation
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Seoul

# Set environment variables for Python and Poetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYTHON_VERSION=3.11

# Set work directory
WORKDIR /

# Install system dependencies and Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    curl \
    build-essential \
    git \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-dev \
    python${PYTHON_VERSION}-venv \
    python3-pip \
    && ln -s /usr/bin/python${PYTHON_VERSION} /usr/bin/python3 \
    && ln -s /usr/bin/python${PYTHON_VERSION} /usr/bin/python \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-root --no-dev

# Copy project files
COPY ./app /app

# Install project
RUN poetry install --no-dev

# Command to run the application
CMD ["poetry", "run", "python", "-m", "app.main"]
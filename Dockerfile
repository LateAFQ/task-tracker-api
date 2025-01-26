FROM python:3.12

WORKDIR /usr/src/project

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.7.1


# System deps:
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y


RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy only requirements to cache them in docker layer

COPY poetry.lock pyproject.toml  /usr/src/project/
ENV PATH="/root/.cargo/bin:${PATH}"
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .
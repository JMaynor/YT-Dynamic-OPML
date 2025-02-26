FROM ghcr.io/astral-sh/uv:python3.13-alpine

# Copy the project into the image
ADD . /app
WORKDIR /app

RUN uv sync --frozen

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

CMD ["python", "/app/src/main.py"]

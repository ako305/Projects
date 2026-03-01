# 1. THE BASE (The Kitchen)
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# 2. THE WORKSPACE (The Countertop)
WORKDIR /app

# 3. PREPARING INGREDIENTS (Dependencies)
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen

# 4. ADDING THE SECRET SAUCE (Your Code)
COPY . .

# 5. OPENING THE WINDOW (The Port)
EXPOSE 8000

# 6. STARTING THE STOVE (The Run Command)
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
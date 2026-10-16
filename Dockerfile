FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8001

# Copy requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy all application code
COPY . /app

# Ensure CLI wrapper is executable
RUN chmod +x /app/dough

EXPOSE 8001

CMD ["python3", "-m", "pizza_agent.server"]

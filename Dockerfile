FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bot ./bot
COPY data ./data
COPY engine ./engine
COPY store ./store
CMD ["python", "-m", "bot.main"]

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 6006

CMD ["python", "-m", "uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "6006"]

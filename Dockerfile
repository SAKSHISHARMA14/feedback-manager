FROM python:3.13-slim
WORKDIR /app

COPY requirements.txt .
COPY app/ ./app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app/main.py"]

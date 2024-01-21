FROM python:3.11

WORKDIR /app

COPY requirements.txt .

COPY . .

RUN pip install -r ./requirements.txt --no-cache-dir

EXPOSE 80

CMD ["uvicorn", "v1.main:app", "--host", "0.0.0.0", "--port", "80"]
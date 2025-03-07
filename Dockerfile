FROM python:3.9
WORKDIR /app

COPY data_generator.py worker.py . 

RUN pip install kafka-python psycopg2

CMD ["python", "data_generator.py"]

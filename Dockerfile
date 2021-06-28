from python:3.7

WORKDIR /job
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./main.py"]
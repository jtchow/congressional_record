from python:3

WORKDIR /job
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./main.py"]
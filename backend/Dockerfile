FROM python:alpine

EXPOSE 8080

WORKDIR /app
ADD . /app

# Using pip:
RUN python3 -m pip install -r requirements.txt
CMD ["python3", "main.py"]

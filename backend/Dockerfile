FROM python:3-alpine3.18

EXPOSE 8080

WORKDIR /app
ADD . /app

# Using pip:
RUN python3 -m pip install -r requirements.txt
CMD ["python3", "main.py"]

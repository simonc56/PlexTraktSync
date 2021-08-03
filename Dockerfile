FROM python:3-alpine
WORKDIR /usr/src/app
COPY requirements.txt .
RUN apk add --no-cache tzdata \
 && python3 -m pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "main.py"]

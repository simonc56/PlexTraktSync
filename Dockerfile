FROM python:3-alpine
WORKDIR /usr/src/app
COPY . .
RUN apk add --no-cache tzdata \
 && pip install --no-cache-dir -r requirements.txt
CMD ["python", "./main.py"]

FROM python:3-alpine
WORKDIR /usr/src/app
COPY . .
RUN apk add --no-cache tzdata \
 && apk add --no-cache --virtual .build-deps python3-dev gcc build-base \
 && pip install --no-cache-dir -r requirements.txt \
 && apk del .build-deps
CMD ["python", "./main.py"]

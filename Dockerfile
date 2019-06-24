FROM alpine:latest

RUN apk add --no-cache python3-dev openssl-dev libffi-dev gcc \
    && pip3 install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements_short.txt

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["run.py"]


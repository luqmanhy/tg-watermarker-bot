FROM python:3.12.3-alpine3.19

RUN apk update && apk upgrade
RUN pip install --upgrade pip
RUN pip install gunicorn

COPY app/ /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:app"]
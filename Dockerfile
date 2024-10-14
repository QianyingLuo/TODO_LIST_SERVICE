FROM python:3.11-alpine as base

RUN pip install --upgrade pip
RUN apk update && apk add --no-cache --update git

COPY requirements.txt ./
RUN ls
RUN pwd
RUN pip install -r requirements.txt

FROM python:3.11-alpine as deploy

COPY --from=base . .
COPY . .

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
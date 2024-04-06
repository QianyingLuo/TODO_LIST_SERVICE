FROM python:3.11-alpine as base

RUN pip install --upgrade pip
RUN apk update && apk add --no-cache --update git

COPY requirements.txt ./
RUN pip install -r .\requirements.txt

FROM python:3.11-alpine as deploy

COPY --from=base . .
COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
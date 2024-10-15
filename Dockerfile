FROM python:3.11-alpine as base

RUN pip install --upgrade pip
RUN apk update && apk add --no-cache --update git

COPY requirements.txt ./
RUN ls
RUN pwd
RUN pip install -r requirements.txt

FROM python:3.11-alpine as deploy

RUN pip install waitress
COPY --from=base . .
COPY . .

CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "main:app"]
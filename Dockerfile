# base image
FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

COPY initialize.sh initialize.sh
RUN chmod +x initialize.sh

ENTRYPOINT ["./initialize.sh"]

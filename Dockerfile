# base image
FROM python:3.11

WORKDIR /app

COPY purchase .

RUN pip install -r requirements.txt

EXPOSE 8000

COPY initialize.sh initial.sh
RUN chmod +x initail.sh

ENTRYPOINT ["./initial.sh"]

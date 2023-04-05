from ubuntu:latest
WORKDIR /catalogue
ENV FLASK_APP=application.py
ENV DATABASE_TYPE=SQLITE
COPY . /catalogue
RUN apt update
RUN apt upgrade -y
RUN apt-get install python3-pip -y
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"] 
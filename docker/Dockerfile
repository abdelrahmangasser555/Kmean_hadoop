FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install numpy pandas scikit-learn

RUN apt-get update && \
    apt-get install -y openjdk-11-jdk

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

CMD ["python","src/driver.py"]
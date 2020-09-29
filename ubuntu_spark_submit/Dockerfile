FROM ubuntu:18.04

ENV SPARK_VERSION=3.0.1
ENV HADOOP_VERSION=2.7

RUN apt-get update -qq && \
    apt-get install -qq -y gnupg2 wget openjdk-8-jdk scala

WORKDIR /
RUN wget --no-verbose http://www.gtlib.gatech.edu/pub/apache/spark/spark-3.0.1/spark-3.0.1-bin-hadoop2.7.tgz

RUN tar -xzf /spark-3.0.1-bin-hadoop2.7.tgz && \
    mv spark-3.0.1-bin-hadoop2.7 spark && \
    echo "export PATH=$PATH:/spark/bin" >> ~/.bashrc



RUN apt-get upgrade -qq python3
RUN apt-get install -qq python3-pip
RUN apt-get install -qq vim
RUN pip3 install pyspark graphframes splink

ENV PYSPARK_PYTHON=python3

COPY simple_script.py simple_script.py
COPY run_script.sh run_script.sh

RUN wget --no-verbose https://github.com/moj-analytical-services/splink/raw/master/jars/scala-udf-similarity-0.0.6.jar


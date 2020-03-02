FROM jupyter/all-spark-notebook:latest

COPY . ${HOME}
USER root

RUN git clone https://github.com/moj-analytical-services/splink.git
RUN pip install splink/
RUN pip install altair


RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}


FROM jupyter/all-spark-notebook:latest

COPY . ${HOME}
USER root

RUN git clone -b break_lineage_api https://github.com/moj-analytical-services/splink.git

RUN pip install splink/
RUN pip install altair
RUN pip install graphframes


RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}


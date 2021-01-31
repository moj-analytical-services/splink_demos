FROM jupyter/all-spark-notebook:703d8b2dcb88

COPY . ${HOME}
USER root

RUN git clone https://github.com/moj-analytical-services/splink.git

RUN pip install splink/
RUN pip install altair
RUN pip install graphframes
RUN pip install typeguard


RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}


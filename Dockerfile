FROM jupyter/pyspark-notebook:29edefbcb06a


COPY . ${HOME}
USER root

RUN pip install splink
RUN pip install altair
RUN pip install graphframes
RUN pip install typeguard
RUN pip install splink-visualise-clusters==0.0.4

# Don't know why this is needed - something to do with root permissions?
# RUN conda install pyspark

RUN chown -R ${NB_UID} ${HOME}

USER ${NB_USER}

ENV PYTHONPATH "${PYTHONPATH}:/usr/local/spark/python:/usr/local/spark/python/lib/py4j-0.10.9-src.zip"

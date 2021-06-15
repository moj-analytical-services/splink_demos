FROM jupyter/pyspark-notebook:29edefbcb06a


COPY . ${HOME}
USER root

RUN pip install splink
RUN pip install altair
RUN pip install graphframes
RUN pip install typeguard
RUN pip install "git+https://github.com/moj-analytical-services/splink_graph.git"

# Don't know why this is needed - something to do with root permissions?
# RUN conda install pyspark


RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}


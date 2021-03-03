FROM jupyter/all-spark-notebook:5cb007f03275


COPY . ${HOME}
USER root

RUN git clone https://github.com/moj-analytical-services/splink.git

RUN pip install splink/
RUN pip install altair
RUN pip install graphframes
RUN pip install typeguard

# Don't know why this is needed - something to do with root permissions?
RUN pip install pyspark


RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}


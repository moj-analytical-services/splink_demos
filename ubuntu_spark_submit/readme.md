## Ubuntu `spark-submit` example

This folder contains a Dockerfile and associated files that demonstrate how to set up Spark and Splink in Ubuntu

You can build the Dockerfile like:

```
 docker build -t ubunspark .
```

Then run a bash terminal within the Docker container with:

```
docker run -it ubunspark /bin/bash
```

Once inside the Docker container, there's a script that uses the splink jar and graphframes that can be executed with:

```
spark-submit \
  --jars=scala-udf-similarity-0.0.6.jar \
  --packages=graphframes:graphframes:0.8.0-spark3.0-s_2.12 \
  simple_script.py
```

If this executes without error, then you know you have everything you need for Splink to work.


It's also possible to run the spark-submit script directly with:

```
docker run ubunspark /bin/bash /run_script.sh
```


The expected output is a bunch of logging output, plus the following outputs:

```
+------------------+
|  similarity_score|
+------------------+
|0.9066666666666667|
+------------------+

GraphFrame(v:[id: string], e:[src: string, dst: string])
+---+-----------+
| id|  component|
+---+-----------+
|  a| 8589934592|
|  b| 8589934592|
|  c| 8589934592|
|  d|51539607552|
+---+-----------+
```
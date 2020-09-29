spark-submit \
  --jars=scala-udf-similarity-0.0.6.jar \
  --packages=graphframes:graphframes:0.8.0-spark3.0-s_2.12 \
  simple_script.py
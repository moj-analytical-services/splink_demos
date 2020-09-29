from graphframes import *

from pyspark.context import SparkContext, SparkConf
from pyspark.sql import SparkSession, Window
from pyspark.sql.types import StructType
import pyspark.sql.functions as f

# point Spark to the locatino of the jar on your computer - you'll need to edit the path in the below lines to point to the location on your machine
conf = SparkConf()
conf.setMaster("local")
conf.set('spark.driver.extraClassPath', '/scala-udf-similarity-0.0.6.jar')
conf.set('spark.jars', '/scala-udf-similarity-0.0.6.jar')

# Also ensure graphframes is available
conf.set('spark.jars.packages', 'graphframes:graphframes:0.8.0-spark3.0-s_2.12')

# Configure settings - for your larger machine you will want to set RAM to however much RAM your machine has (16g?)
# and shuffle partitions to probably something like 5x the number of CPU cores
conf.set('spark.driver.memory', '4g')
conf.set("spark.sql.shuffle.partitions", "8")

sc = SparkContext.getOrCreate(conf=conf)
sc.setCheckpointDir("temp_graphframes/")
spark = SparkSession(sc)

# Register the doublemetaphone and jarowinkler functions so they are available to Splink in Spark SQL
from pyspark.sql import types
spark.udf.registerJavaFunction('jaro_winkler_sim', 'uk.gov.moj.dash.linkage.JaroWinklerSimilarity', types.DoubleType())
spark.udf.registerJavaFunction('Dmetaphone', 'uk.gov.moj.dash.linkage.DoubleMetaphone', types.StringType())



# test whether the similarity functinos work

sql = """
select jaro_winkler_sim('Robin', 'Robyn') as similarity_score
"""

spark.sql(sql).show()

# test whether graphframes work

vertices = spark.createDataFrame([
  ("a",),
  ("b",),
  ("c",),
  ("d",)
], ["id"])

edges = spark.createDataFrame([
  ("a", "b"),
  ("b", "c")
], ["src", "dst"])

g = GraphFrame(vertices, edges)
print(g)

result = g.connectedComponents()
result.show()
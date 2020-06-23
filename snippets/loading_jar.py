from pyspark.context import SparkContext, SparkConf
from pyspark.sql import SparkSession
conf=SparkConf()
conf.set('spark.driver.extraClassPath', 'jars/scala-udf-similarity-0.0.6.jar')
conf.set('spark.jars', 'jars/scala-udf-similarity-0.0.6.jar')

spark = SparkSession(sc)
sc = SparkContext.getOrCreate(conf=conf)
udfs = [
    ('jaro_winkler_sim', 'JaroWinklerSimilarity',DoubleType()),
    ('jaccard_sim', 'JaccardSimilarity',DoubleType()),
    ('cosine_distance', 'CosineDistance',DoubleType()),
    ('Dmetaphone', 'DoubleMetaphone',StringType()),
    ('QgramTokeniser', 'QgramTokeniser',StringType())
]

for a,b,c in udfs:
    spark.udf.registerJavaFunction(a, 'uk.gov.moj.dash.linkage.'+ b, c)
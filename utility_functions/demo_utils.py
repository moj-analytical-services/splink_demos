from IPython.display import display, Markdown
from splink.validate import _get_schema

from pyspark.context import SparkContext, SparkConf
from pyspark.sql import SparkSession, Window
from pyspark.sql.types import StructType
import pyspark.sql.functions as f

from splink.jar_location import similarity_jar_location



def get_spark():
    conf = SparkConf()

    # Load in a jar that provides extended string comparison functions such as Jaro Winkler.
    # Splink

    loc = similarity_jar_location()
    
    # The folowing line was needed in Spark 2.4.5 but not Spark 3.0
    # conf.set("spark.driver.extraClassPath", f"{loc")

    conf.set("spark.jars",f"{loc},jars/graphframes-0.8.0-spark3.0-s_2.12.jar")


    # WARNING:
    # These config options are appropriate only if you're running Spark locally!!!
    conf.set("spark.driver.memory", "4g")
    conf.set("spark.sql.shuffle.partitions", "8")

    sc = SparkContext.getOrCreate(conf=conf)
    sc.setCheckpointDir("temp_graphframes/")
    spark = SparkSession(sc)

    # Register UDFs
    from pyspark.sql import types

    spark.udf.registerJavaFunction(
        "jaro_winkler_sim",
        "uk.gov.moj.dash.linkage.JaroWinklerSimilarity",
        types.DoubleType(),
    )
    spark.udf.registerJavaFunction(
        "Dmetaphone", "uk.gov.moj.dash.linkage.DoubleMetaphone", types.StringType()
    )
    return spark


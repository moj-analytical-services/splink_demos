import sys
import os

from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

from pyspark.sql.types import DoubleType, StringType


from splink import Splink

from splink_settings import settings

sc = SparkContext()
glueContext = GlueContext(sc)
logger = glueContext.get_logger()
spark = glueContext.spark_session


def add_udfs(spark):
    # Register UDFs
    udfs = [
        ('jaro_winkler_sim', 'JaroWinklerSimilarity',DoubleType()),
        ('jaccard_sim', 'JaccardSimilarity',DoubleType()),
        ('cosine_distance', 'CosineDistance',DoubleType()),
        ('Dmetaphone', 'DoubleMetaphone',StringType()),
        ('QgramTokeniser', 'QgramTokeniser',StringType())
    ]

    for a,b,c in udfs:
        spark.udf.registerJavaFunction(a, 'uk.gov.moj.dash.linkage.'+ b, c)

add_udfs(spark)

df = spark.read.parquet("s3://path_to_input_dataset/")

OUTPUT_PATH = "s3://path_to_splink_outputs/"

def persist_params_settings(params, settings):
    it_num = params.iteration

    params.all_charts_write_html_file(filename="sparklink_charts.html", overwrite=True)
    path = os.path.join(OUTPUT_PATH, f"charts/sparklink_charts_iteration_{it_num}.html")
    write_local_file_to_s3("sparklink_charts.html",path, overwrite=True)

    params.save_params_to_json_file("saved_params.json", overwrite=True)
    path = os.path.join(OUTPUT_PATH, f"params/saved_params_iteration_{it_num}.json")
    write_local_file_to_s3("saved_params.json", path, overwrite=True)

# Lineage breaking functions
def blocked_comparisons_to_s3(df, spark):
    df = df.repartition(50)
    path = os.path.join(OUTPUT_PATH, "data/df_gammas/")
    df.write.mode("overwrite").parquet(path)
    df_new = spark.read.parquet(path)
    return df_new

def scored_comparisons_to_s3(df, spark):

    path = os.path.join(OUTPUT_PATH, "data/df_e/")
    df.write.mode("overwrite").parquet(path)
    df_new = spark.read.parquet(path)
    return df_new

from splink import Splink
linker = Splink(settings,
                spark,
                df=df,
                save_state_fn=persist_params_settings,
                break_lineage_blocked_comparisons = blocked_comparisons_to_s3,
                break_lineage_scored_comparisons = scored_comparisons_to_s3
               )
df_e = linker.get_scored_comparisons()

write_local_file_to_s3("saved_params.json", path, overwrite=True)

df_e.write.mode("overwrite").parquet(path)
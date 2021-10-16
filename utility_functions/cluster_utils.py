from pyspark.sql.dataframe import DataFrame
from graphframes import GraphFrame
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import expr

def clusters_at_thresholds(
    df_nodes: DataFrame,
    df_edges: DataFrame,
    threshold_values: list,
    cluster_colnames: list,
    spark: SparkSession,
    uid_df_nodes_col="unique_id",
    uid_col_l="unique_id_l",
    uid_col_r="unique_id_r",
    score_colname="match_probability",
    join_node_details=True,
):
    """Generated a table of clusters at one or more threshold_values
    from a table of scored edges (scored pairwise comparisons)

    Args:
        df_nodes (DataFrame): Dataframe of nodes (original records from which pairwise comparisons are derived)
        df_edges (DataFrame): Dataframe of edges (pairwise record comparisons with scores)
        threshold_values (list): A list of threshold values above which edges will be considered matches.  e.g. [0.5, 0.95, 0.99]
        cluster_colnames (list): A list of column names used for the clusters, e.g. ["cluster_low", "cluster_medium", "cluster_high"]
        spark (SparkSession): The pyspark.sql.session.SparkSession
        uid_df_nodes_col (str, optional): The name of the unique id column in the df_nodes table. Alternatively, a SQL expression defining a unique column. Defaults to "unique_id".  Used only if
            df_nodes is not None.
        uid_col_l (str, optional): Name of the 'left' column containing unique IDs in the edges table.  Alternatively, a SQL expression defining a unique column. Defaults to "unique_id_l".
        uid_col_r (str, optional): The name of the 'right' column containing unique IDs in the edges table.   Alternatively, a SQL expression defining a unique column. Defaults to "unique_id_r".
        score_colname (str, optional): The name of the score column to which the thresholds apply. Defaults to "match_probability".
        join_node_details (bool, optional):  Defaults to True.  If true, return the clusters against the full nodes table.  If false, return just IDs and clusters.

    """
    df_nodes.createOrReplaceTempView("df_nodes")
    df_edges.createOrReplaceTempView("df_edges")
    # note UNION as opposed to UNION ALL has the effect of deduping IDs

    sql = f"""
    select {uid_df_nodes_col} as id
    from df_nodes
    """
    df_nodes_id = spark.sql(sql)

    cc_thresholds = []
    for v in threshold_values:
        sql = f"""
        select
            {uid_col_l} as src,
            {uid_col_r} as dst
        from df_edges
        where {score_colname} > {v}
        """
        edges_above_thres = spark.sql(sql)
        g = GraphFrame(df_nodes_id, edges_above_thres)
        cc = g.connectedComponents()
        cc_thresholds.append(cc)

    for cc, cc_col_name in zip(cc_thresholds, cluster_colnames):
        df_nodes_id = df_nodes_id.join(cc, on=["id"], how="left")
        df_nodes_id = df_nodes_id.withColumnRenamed("component", cc_col_name)

    if join_node_details:
        df_nodes_id.createOrReplaceTempView("df_nodes_id")

        df_nodes = df_nodes.withColumn("___id__", expr(uid_df_nodes_col))
        df_nodes.createOrReplaceTempView("df_nodes")

        names = [f"df_nodes_id.{c}" for c in cluster_colnames]
        cluster_sel = ", ".join(cluster_colnames)

        sql = f"""
        select {cluster_sel}, df_nodes.*
        from df_nodes
        left join df_nodes_id
        on df_nodes_id.id = df_nodes.___id__

        """
        df_nodes = spark.sql(sql)
        df_nodes = df_nodes.drop("___id__")
    else:
        df_nodes = df_nodes_id

    return df_nodes


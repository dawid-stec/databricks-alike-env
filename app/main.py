from datetime import datetime

from delta import DeltaTable
from pyspark.sql import SparkSession

from load_delta import load_test_data

spark_session = (
    SparkSession.builder.appName("app")
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0")
    .config("spark.sql.extensions", "io.delta:sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)
spark_session.sql("SET spark.databricks.delta.formatCheck.enabled=false")

load_test_data(spark_session)

timestamp_before_load = datetime.now()

table_name = "test_table"
table_metadata = spark_session.sql(f"DESCRIBE DETAIL {table_name}")
table_path = table_metadata.select("location").head()[0]

delta_table = DeltaTable.forPath(spark_session, table_path)
last_operation_timestamp = delta_table.history(1).select("timestamp").collect()[0][0]

delta_df = (
    spark_session.read.format("delta")
    .option("startingTimestamp", timestamp_before_load)
    .option("endingTimestamp", last_operation_timestamp)
    .table(table_name)
)

delta_df.show()

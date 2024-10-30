from pyspark.sql import DataFrame, SparkSession


def delta_table_exists(spark_session: SparkSession, table_name, db_name='default'):
    return spark_session.catalog.tableExists(f"{db_name}.{table_name}")


def load_data_to_table(spark_session: SparkSession, table_name, data: DataFrame):
    if delta_table_exists(spark_session, table_name):
        data.write.format("delta").mode("append").saveAsTable(table_name)
    else:
        data.write.format("delta").mode("overwrite").saveAsTable(table_name)


def load_test_data(spark_session: SparkSession):
    test_file_path = "../test_file.csv"
    test_df = spark_session.read.option("header", True).csv(test_file_path)
    load_data_to_table(spark_session, "test_table", test_df)

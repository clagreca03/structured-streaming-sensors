from pyspark.sql import SparkSession


# Initialize Spark session
spark = SparkSession.builder \
    .appName("TestApp") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .getOrCreate()

# Set log level to ERROR
spark.sparkContext.setLogLevel("ERROR")

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "test") \
    .load()
df.selectExpr("CAST(value AS STRING)")

query = df.writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

query.awaitTermination()
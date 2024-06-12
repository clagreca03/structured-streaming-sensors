from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, concat, lit
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, IntegerType, ArrayType


# Initialize Spark session
spark = SparkSession.builder \
    .appName("Sensor Data") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Set log level to ERROR
spark.sparkContext.setLogLevel("ERROR")

# Define the schema for the JSON data
schema = StructType([
    StructField("event_id", StringType()),
    StructField("event_time", StringType()),
    StructField("sensor_id", StringType()),
    StructField("sensor_name", StringType()),
    StructField("sensor_type", StringType()),
    StructField("latitude", DoubleType()),
    StructField("longitude", DoubleType())
])

# Read a Streaming Source
input_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "sensor-data") \
    .load()

# Transform to Output DataFrame
value_df = input_df.select(from_json(col("value").cast("string"), schema).alias("value"))
value_df = value_df.selectExpr("value.*").withColumn("geolocation", concat(col("latitude").cast("string"), lit(","), col("longitude").cast("string")))
output_df = value_df

# Output to console for debugging
query = output_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()


# Uncomment for debugging
# query.awaitTermination()
# exit()


# Write to Sink
query = output_df.writeStream \
    .outputMode("append") \
    .format("org.elasticsearch.spark.sql") \
    .option("es.nodes", "elastic") \
    .option("es.port", "9200") \
    .option("es.resource", "sensor-data") \
    .option("es.write.operation", "index") \
    .option("es.spark.sql.streaming.sink.log.enabled", "true") \
    .option("es.spark.sql.streaming.sink.log.path", "sensor-data-log") \
    .option("checkpointLocation", "/tmp/sensor-data/checkpoint") \
    .start()

query.awaitTermination()
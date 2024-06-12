from pyspark.sql import SparkSession


# Initialize Spark session
spark = SparkSession.builder \
    .appName("ElasticTest") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Set log level to ERROR
spark.sparkContext.setLogLevel("ERROR")

# Create DataFrame
data = [("John", "Doe"), ("Jane", "Doe"), ("Sam", "Smith")]
columns = ["FirstName", "LastName"]
df = spark.createDataFrame(data, columns)

# Write the DataFrame to an Elasticsearch index
df.write.format("org.elasticsearch.spark.sql") \
    .mode("append") \
    .option("es.nodes", "elastic") \
    .option("es.port", "9200") \
    .option("es.resource", "test") \
    .option("es.write.operation", "index") \
    .save()

# Stop the SparkSession
spark.stop()


Fabric End to end Project - Silver Notebook

***
from pyspark.sql.functions import col, isnull, when
from pyspark.sql.types import TimestampType
from datetime import date, timedelta

***
# Remove this before running Data Factory Pipeline
start_date = date. today() - timedelta(7)

***
# Load the JSON data into a Spark DataFrame
df = spark.read.option("multiline", "true").json(f"Files/{start_date}_earthquake_data.json")

***
# Reshape earthquake data
df = (
    df
    .select(
        'id',
        col('geometry.coordinates').getItem(0).alias('longitude'),
        col('geometry.coordinates').getItem(1).alias('latitude'),
        col('geometry.coordinates').getItem(2).alias('elevation'),
        col('properties.title').alias('title'),
        col('properties.place').alias('place_description'),
        col('properties.sig').alias('sig'),
        col('properties.mag').alias('mag'),
        col('properties.magType').alias('magType'),
        col('properties.time').alias('time'),
        col('properties.updated').alias('updated')
    )
)

***
# Validate data: Check for missing or null values
df = (
    df
    .withColumn('longitude', when(isnull(col('longitude')), 0).otherwise(col('longitude')))
    .withColumn('latitude', when(isnull(col('latitude')), 0).otherwise(col('latitude')))
    .withColumn('time', when(isnull(col('time')), 0).otherwise(col('time')))
)

***
# Convert 'time' and 'updated' to timestamp
df = (
    df
    .withColumn('time', (col('time') / 1000).cast(TimestampType()))
    .withColumn('updated', (col('updated') / 1000).cast(TimestampType()))
)

***
# Append to the silver table
df.write.mode('append').saveAsTable('earthquake_events_silver')


from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext

def main():
    spark = SparkSession.builder.appName("RealisticUberRides").getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, 0.3)

    rides = ssc.socketTextStream("localhost", 9999)
    
    def process_rdd(time, rdd):
        if not rdd.isEmpty():
            df = spark.read.json(rdd)
            df.show()
            df.createOrReplaceTempView("rides")
            result = spark.sql("""
                SELECT location, COUNT(*) AS total_rides, AVG(fare) AS avg_fare, AVG(distance) AS avg_distance
                FROM rides
                GROUP BY location
            """)
            result.show()
            result.write.csv(path="./sparkoutput", mode="overwrite", header=True)

            # Saving unique starting locations to another path
            unique_locations = df.select("starting_location_name", "starting_location_lat", "starting_location_lon").distinct()
            unique_locations.show()
            unique_locations.write.csv(path="./mapoutput", mode="overwrite", header=True)

    rides.foreachRDD(process_rdd)

    ssc.start()
    ssc.awaitTermination()

if __name__ == "__main__":
    main()

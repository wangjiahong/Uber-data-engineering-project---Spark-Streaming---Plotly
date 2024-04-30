import requests
from pyspark.sql import SparkSession

# Function to fetch data from the API
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Main Spark application
def main():
    # Initialize Spark Session
    spark = SparkSession.builder.appName("APIFetch").getOrCreate()

    # API URL
    url = "https://jsonplaceholder.typicode.com/posts"

    # Fetch data
    data = fetch_data(url)
    if data is not None:
        # Save data to a temporary JSON file
        temp_file = "/tmp/posts.json"
        with open(temp_file, 'w') as f:
            f.write(str(data))

        # Read JSON data using Spark
        df = spark.read.json(temp_file)

        # Perform a simple transformation: Select only the title of each post
        titles = df.select("title")

        # Show the result
        titles.show(5)  # Display the titles of the first 5 posts

    else:
        print("Failed to fetch data from the API.")

    # Stop Spark Session
    spark.stop()

if __name__ == "__main__":
    main()

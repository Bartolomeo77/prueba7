from pyspark.sql import SparkSession
from pyspark.sql.functions import col,date_format

def init_spark():
  sql = SparkSession.builder\
    .appName("trip-app")\
    .config("spark.jars", "/opt/spark-apps/postgresql-42.2.22.jar")\
    .getOrCreate()
  sc = sql.sparkContext
  return sql,sc

def read_data_from_postgres(sql, url, properties, table):
    df = sql.read.jdbc(url=url, table=table, properties=properties, numPartitions=10)
    return df

def main():

    url = "jdbc:postgresql://demo-database:5432/movilens"
    properties = {
        "user": "postgres",
        "password": "casa1234",
        "driver": "org.postgresql.Driver"
    }

    table = "base20"
    sql,sc = init_spark()
    

    # Leer datos desde PostgreSQL y crear DataFrame
    data_df = read_data_from_postgres(sql, url, properties, table)

    # Muestra los primeros 5 registros del DataFrame
    data_df.show(10)

    # Contar y mostrar la cantidad total de datos en el DataFrame
    total_count = data_df.count()
    print(f"Total de datos: {total_count}")
  
if __name__ == '__main__':
  main()

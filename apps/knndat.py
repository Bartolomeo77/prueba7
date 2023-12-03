from pyspark.sql import SparkSession
from pyspark.sql.functions import col,date_format
from pyspark.sql.functions import avg
def init_spark():
    
    sql = SparkSession.builder\
      .appName("trip-app")\
      .config("spark.jars", "/opt/spark-apps/postgresql-42.2.22.jar")\
      .getOrCreate()
    sc = sql.sparkContext
    return sql,sc

def main():
    
    file = "/opt/spark-data/ratings20.csv"
    sql,sc = init_spark()

    df = sql.read.load(file, format="csv", inferSchema="true", header=True)  \
          .select("userid", "movieid", "rating") 
          #.repartition(100000)
   
    consolidated_df = df.groupBy('userid', 'movieid').agg(avg('rating').alias('mean_rating'))

    # Pivot the data to create a user-item matrix
    consolidated_df = consolidated_df.groupBy('userid').pivot('movieid').agg(avg('mean_rating'))

    consolidated_df = consolidated_df.na.fill(0)  

    #Mejorado , casi ni se siente la carga

    # Definir la función manhattan_distance correctamente
    def manhattan_distance(array1, array2):
        return sum(abs(a - b) for a, b in zip(array1, array2))

    # Define el usuario objetivo
    target_user_id = 1

    # Filtrar datos del usuario objetivo de manera eficiente
    target_user_data = consolidated_df.filter(col("userId") == target_user_id).select(*consolidated_df.columns[1:]).collect()

    if not target_user_data:
        print(f"No hay datos para el usuario {target_user_id}")
    else:
        target_user_data = target_user_data[0]

    # Calcular distancias utilizando operaciones vectorizadas
    distances = consolidated_df.filter(col("userId") != target_user_id).rdd.map(
        lambda row: (row.userId, manhattan_distance(row[1:], target_user_data))
    ).collect()

    # Ordenar las distancias
    sorted_distances = sorted(distances, key=lambda x: x[1])

    print(f"Vecinos más cercanos para el Usuario {target_user_id}: {sorted_distances}")

if __name__ == '__main__':
  main()

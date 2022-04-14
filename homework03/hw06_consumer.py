#importing packages
import time
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
stream_df = (spark.readStream.format('socket')
                             .option('host', 'localhost')
                             .option('port', 22223)
                             .load())

json_df = stream_df.selectExpr("CAST(value AS STRING) AS payload")

writer = (
    json_df.writeStream
           .queryName('iss')
           .format('memory')
           .outputMode('append')
)

streamer = writer.start()


for _ in range(5):
    df = spark.sql("""
    SELECT CAST(get_json_object(payload, '$.iss_position.latitude') AS FLOAT) AS latitude,
           CAST(get_json_object(payload, '$.iss_position.longitude') AS FLOAT) AS longitude 
    FROM iss
    """)
    
    #df.show(10)
    
    #print(df)
    time.sleep(5)
    
streamer.awaitTermination(timeout=3600)
print('streaming done!')

# df = pd.read_csv('latlon.csv')
latitude_list=[]
longitude_list=[]
for i,x in zip(df.select('latitude').collect(), df.select('longitude').collect()):
    latitude_list.append(i[0])
    longitude_list.append(x[0])
dfmap = pd.DataFrame(list(zip(latitude_list, longitude_list)),
               columns =['Latitude', 'Longitude'])
   
plt.rcParams["figure.figsize"] = (15,10)    
gdf = geopandas.GeoDataFrame(
    dfmap, geometry=geopandas.points_from_xy(dfmap.Longitude, dfmap.Latitude))
    
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))


# We can now plot our ``GeoDataFrame``.
gdf.plot(ax=world.plot(
    color='white', edgecolor='black'), color='red')
plt.title('International Space Station Location ', fontsize= 18)
plt.xlabel('Longitude', fontsize = 15)
plt.ylabel('Latitude', fontsize = 15)
plt.savefig('hw06_map.jpg')
plt.show()

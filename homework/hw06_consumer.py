import socket
import pandas as pd
import ast
import chart_studio.plotly as py
import plotly.graph_objs as go 
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True) 
import plotly.express as px

#taking the server name and port name
HOST = '127.0.0.1'
PORT = 22228

#creating a socket at client side
#using TCP/IP Protocol
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#connect it to server and port
#number on local computer
s.connect((HOST, PORT))

#receive message strinf from
#server, at a time 1024 
msg = s.recv(1024)

# timestamp = []
# longitude = []
# latitude = []
# while msg:
#     #print(msg.decode("UTF-8"))
#     row=ast.literal_eval(msg.decode("UTF-8"))
#     msg = s.recv(1024)
   
#     print(row)
#     #print(type(res))
#     #print(res['timestamp'])
#     #print(res['iss_position'])
#     timestamp.append(res['timestamp'])
#     longitude.append(res['iss_position']['longitude'])
#     latitude.append(res['iss_position']['latitude'])
    
df=pd.DataFrame()
while msg:
    row=ast.literal_eval(msg.decode("UTF-8"))
    print(row)
    timestampe=row["timestamp"]
    longitude=row["iss_position"]["longitude"]
    latitude=row["iss_position"]["latitude"]
    dict={"timestamp": timestampe, "longitude":longitude, "latitude": latitude}
    entry=pd.DataFrame.from_dict([dict])
    df=pd.concat([df, entry], ignore_index=True)
    msg = s.recv(1024)
s.close()

#df

df['date_time'] = pd.to_datetime(df['timestamp'], unit = 's')
df['time'] = df['date_time'].dt.time

plt.figure(figsize = (12,8))
fig = px.scatter_geo(df,lat='latitude',lon = 'longitude',hover_name = 'time')

fig.show()



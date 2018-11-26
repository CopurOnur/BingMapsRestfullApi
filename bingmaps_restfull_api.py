import urllib.request
import json
import pandas as pd
import requests

# put your bing maps api key key here
bingMapsKey = ""

routeUrl = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key=" + bingMapsKey

#------------------- JSON BODY FORMAT -----------------------
"""
{
    "origins": [{
        "latitude": lat0,
        "longitude": lon0
    },
    {
        "latitude": latM,
        "longitude": lonM
    }],
    "destinations": [{
        "latitude": lat0,
        "longitude": lon0
    }, 
    {
        "latitude": latN,
        "longitude": lonN
    }],
    "travelMode": travelMode,
    "startTime": startTime,
    "timeUnit": timeUnit
}
"""
    
#------------------ example data preproceesing for json post body --------------------
#size should be at mos t 50 because api can request at most 2500 queries at a time 
size=50
origins=[]
destinations=[]
#paste path of the excel file containing the coordinates just an example file 
path=""
matrix=pd.read_excel(path)
df=pd.DataFrame(data={"latitude":matrix["DBLKOORDINATX"],"longitude":matrix["DBLKOORDINATY"]})

#create the origins (you can select any 50 origin points from the data by changing the start and end indicies of range function)
for i in range(size):
    dicts=df.iloc[i].to_dict()
    origins.append(dicts)

#create the destinations (you can select any 50 origin points from the data by changing the start and end indicies of range function)
for i in range(size):
    dicts=df.iloc[i].to_dict()
    destinations.append(dicts)
    
restfull={"origins":origins,"destinations":destinations,"travelMode": "driving"}

#--------------- REQUEST--------------------

response = requests.post(routeUrl, data=json.dumps(restfull))

results=response.json()
dist_mat=[]
for i in range(size * size):
    distance = results["resourceSets"][0]["resources"][0]["results"][i]["travelDistance"]
    dist_mat.append(distance)
    
#print the results
print(dist_mat)




###### Update details for Place id in Details Table ######
import MySQLdb
import json
import requests
import datetime
import os
import location_data_cleanup_config_reader
import location_data_cleanup_csv_reader
import location_data_cleanup_place_finder

dirname = os.path.dirname(__file__)
logFile = os.path.join(dirname,"details_update_log")
logFile = open (logFile, "w+")

try:
    db = MySQLdb.connect(host=location_data_cleanup_config_reader.host, user=location_data_cleanup_config_reader.user, passwd=location_data_cleanup_config_reader.passwd, db=location_data_cleanup_config_reader.db)
    cursor = db.cursor()
except:
    logFile.write("Error: connecting to the database failed" + "\n")

db.set_character_set('utf8')
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

Detailurl = "https://maps.googleapis.com/maps/api/place/details/json?fields=opening_hours/weekday_text,formatted_address,formatted_phone_number,geometry,name,url,website"

cursor.execute("""SELECT PlaceID FROM DetailsID""")

timestamp = datetime.datetime.now()

for row in cursor.fetchall():
    PlaceIDurl = "https://maps.googleapis.com/maps/api/place/details/json"
    querystring = {"key":location_data_cleanup_config_reader.placesAPIKey,"placeid":row[0],"fields":"place_id"}
    response = requests.request("GET", PlaceIDurl, params=querystring)
    if response.status_code == 200:   
        jsonResponse = response.text
        loadedJson = json.loads(jsonResponse)
        print(loadedJson)
        result = loadedJson.get('result')
        print(result)
        print("")
        print("")
        if result != None:
            placeID = result.get('place_id')
            
            querystring = {"placeid": row[0],"key":location_data_cleanup_config_reader.placesAPIKey}
            response = requests.request("GET", Detailurl, params=querystring)

            jsonResponse = response.text
            loadedJson = json.loads(jsonResponse)
            result = loadedJson.get('result')

            cursor.execute('UPDATE DetailsID SET Details = %s WHERE PlaceID = %s', (result,row[0]))
            cursor.execute('UPDATE DetailsID SET DateUpdated = %s WHERE PlaceID = %s', (timestamp,row[0]))
            cursor.execute('UPDATE DetailsID SET PlaceID = %s WHERE PlaceID = %s', (placeID, row[0]))
            db.commit()
        else:
            logFile.write(response.text + "\n")    
            cursor.execute("""INSERT INTO FailureTable (ReferenceId,PlaceId,Details,DateCreated) VALUES (%s, %s, %s, %s)""",(0,row[0],response.text,timestamp))
    else:
        logFile.write(response.text + "\n")    
        cursor.execute("""INSERT INTO FailureTable (ReferenceId,PlaceId,Details,DateCreated) VALUES (%s, %s, %s, %s)""",(0,row[0],response.text,timestamp))
            
db.commit()
logFile.close()

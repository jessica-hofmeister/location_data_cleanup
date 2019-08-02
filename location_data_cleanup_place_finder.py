###### Request id from Places api ######
import MySQLdb
import json
import requests
import os
import datetime
import location_data_cleanup_config_reader
import location_data_cleanup_csv_reader
#import location_data_cleanup_database_prep

dirname = os.path.dirname(__file__)
logFile = os.path.join(dirname,"place_finder_log")
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

url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

cursor.execute("""SELECT Id,QueryInput,InputType,Type,Processed,ReferenceId FROM relationshipTable""")

timestamp = datetime.datetime.now()

for row in cursor.fetchall():
    if row[4] == '0':
        params = row[1]
        print(params)
        querystring = {"key":location_data_cleanup_config_reader.placesAPIKey,"input":params,"inputtype":row[2]}

        response = requests.request("GET", url, params=querystring)
        print(response.text)
        if response.status_code == 200:   
            jsonResponse = response.text
            loadedJson = json.loads(jsonResponse)
            print(loadedJson)
            responseStatus = loadedJson.get('status')
            if responseStatus == "OK":
                result = loadedJson.get('candidates')
                if len(result) >= 1:
                    result = loadedJson.get('candidates')[0]
                    placeID = result.get('place_id')
                    #placeID = 'ChIJEVgOu9E754cRZ8TsR4r0LsI'
                    placeIDDuplicate = False
                    PlaceIDCursor = db.cursor()
                    PlaceIDCursor.execute("""SELECT Placeid FROM DetailsID""")
                    allPlaceIDsInDetailsIDTable = PlaceIDCursor.fetchall()
                    for i in range (len(allPlaceIDsInDetailsIDTable)):
                        if placeID in allPlaceIDsInDetailsIDTable[i]:
                            placeIDDuplicate = True
                    if placeIDDuplicate == False:
                        PlaceIDCursor.execute("""INSERT INTO DetailsID (PlaceID,Details,DateCreated) VALUES (%s,%s,%s)""",(placeID,"",timestamp))

                    PlaceIDCursor.execute('UPDATE relationshipTable SET PlaceID = %s WHERE ID = %s', (placeID,row[0]))
                    PlaceIDCursor.execute('UPDATE relationshipTable SET Processed = %s WHERE ID = %s', (True,row[0]))
                    PlaceIDCursor.execute('UPDATE relationshipTable SET Tags = %s WHERE ID = %s', (location_data_cleanup_config_reader.tags,row[0]))
                    PlaceIDCursor.execute('UPDATE relationshipTable SET DateProcessed = %s WHERE ID = %s', (timestamp,row[0]))
                    db.commit()
                else:
                    logFile.write(jsonResponse + "\n")    
                    cursor.execute("""INSERT INTO FailureTable (ReferenceId,PlaceId,Details,DateCreated) VALUES (%s, %s, %s, %s)""",(row[5],"NA",jsonResponse,timestamp)) 
            else:
                logFile.write(jsonResponse + "\n")    
                cursor.execute("""INSERT INTO FailureTable (ReferenceId,PlaceId,Details,DateCreated) VALUES (%s, %s, %s, %s)""",(row[5],"NA",jsonResponse,timestamp))
        else:
            logFile.write(jsonResponse + "\n")    
            cursor.execute("""INSERT INTO FailureTable (ReferenceId,PlaceId,Details,DateCreated) VALUES (%s, %s, %s, %s)""",(row[5],"NA",jsonResponse,timestamp))
    row = cursor.fetchone()

db.commit()
logFile.close()

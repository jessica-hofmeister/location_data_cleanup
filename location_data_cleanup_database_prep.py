######  Prep table with unprocessed data from csv file  ######
import MySQLdb
import datetime
import os
import location_data_cleanup_config_reader
import location_data_cleanup_csv_reader

dirname = os.path.dirname(__file__)
logFile = os.path.join(dirname,"database_prep_log")
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
timestamp = datetime.datetime.now()

######  Test that the table schema is correct ######
columnNamesRelationshipTable = []
expectedColumnNamesRelationshipTable = ["DateCreated", "DateProcessed", "Id", "InputType", "PlaceId", "Processed", "QueryInput", "ReferenceId", "Tags", "Type"]
columnNamesDetailsTable = []
expectedColumnNamesDetailsTable = ["DateCreated", "DateUpdated", "Details", "Id", "PlaceID"]

cursor.execute('SHOW columns FROM relationshipTable')
for column in cursor.fetchall():
    columnNamesRelationshipTable.append(column[0])
columnNamesRelationshipTable.sort()
cursor.execute('DESCRIBE DetailsID')
for column in cursor.fetchall():
    columnNamesDetailsTable.append(column[0])
columnNamesDetailsTable.sort()

if columnNamesRelationshipTable == expectedColumnNamesRelationshipTable and columnNamesDetailsTable == expectedColumnNamesDetailsTable:
    for row in location_data_cleanup_csv_reader.valueList:
        cursor.execute("""INSERT INTO relationshipTable (ReferenceId,QueryInput,InputType,Type,Tags,PlaceId,Processed,DateCreated,DateProcessed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",(row[0],row[1],location_data_cleanup_config_reader.inputtype,row[2],location_data_cleanup_config_reader.tags,"None",False,timestamp,None))
        db.commit()
else: logFile.write("The Tables you are trying to update do not match the required schema.  If you really want to use this database, consider running location_data_cleanup_database_seed.py.  This will delete and recreate the required tables, so please be sure you know what you're doing!" + "\n")
db.commit()
logFile.close()

######  Seed for tables in case you have to start fresh  ######
import MySQLdb
import os
import location_data_cleanup_config_reader
dirname = os.path.dirname(__file__)                     #Determine which directory we are in 

logFile = os.path.join(dirname,"seed_log")
logFile = open (logFile, "w+")

try:
    db = MySQLdb.connect(host=location_data_cleanup_config_reader.host, user=location_data_cleanup_config_reader.user, passwd=location_data_cleanup_config_reader.passwd, db=location_data_cleanup_config_reader.db)
    cursor = db.cursor()
except:
    logFile.write("Error: connecting to the database failed" + "\n")


cursor.execute("DROP TABLE IF EXISTS relationshipTable")
cursor.execute("CREATE TABLE relationshipTable(Id INT PRIMARY KEY AUTO_INCREMENT,ReferenceId INT(25),QueryInput VARCHAR(200),InputType VARCHAR(25),Type VARCHAR(25),Tags VARCHAR(25),PlaceId VARCHAR(50),Processed VARCHAR(25),DateCreated Datetime,DateProcessed Datetime)")

cursor.execute("DROP TABLE IF EXISTS DetailsID")
cursor.execute("CREATE TABLE DetailsID (Id INT PRIMARY KEY AUTO_INCREMENT,PlaceID VARCHAR(50),Details VARCHAR(500),DateCreated Datetime,DateUpdated Datetime)")

cursor.execute("DROP TABLE IF EXISTS FailureTable")
cursor.execute("CREATE TABLE FailureTable (Id INT PRIMARY KEY AUTO_INCREMENT,ReferenceId INT(25),PlaceID VARCHAR(50),Details VARCHAR(500),DateCreated Datetime)")

logFile.close()

import json 
import os
dirname = os.path.dirname(__file__)                #Determine which directory we are in 
logFile = os.path.join(dirname,"json_reader_log")    #Assign this logfile to the same directory 
logFile = open (logFile, "w+")

jsonFile = os.path.join(dirname,'location_data_cleanup_config.json')    #Assign this logfile to the same directory 

try:
    with open(jsonFile) as jFile:
        loadedJson = json.load(jFile)
        #print (json.dumps(loadedJson, indent=4))
        #print(loadedJson[0])
        host = loadedJson[0].get('host')
        if host == None: logFile.write("Error: host does not exist. Checking spelling of variable name" + "\n")
        
        user = loadedJson[0].get("user")
        if user == None: logFile.write("Error: user does not exist. Checking spelling of variable name" + "\n")
        
        passwd = loadedJson[0].get("passwd")
        if passwd == None: logFile.write("Error: passwd does not exist. Checking spelling of variable name" + "\n")
        
        db = loadedJson[0].get("db")
        if db == None: logFile.write("Error: db does not exist. Checking spelling of variable name" + "\n")

        placesAPIKey = loadedJson[0].get("placesAPIKey")
        if placesAPIKey == None: logFile.write("Error: placesAPIKey does not exist. Checking spelling of variable name" + "\n")
        
        tags = loadedJson[0].get("tags")
        if tags == None: logFile.write("Error: tags does not exist. Checking spelling of variable name" + "\n")

        csvWithInputData = loadedJson[0].get("csvWithInputData")
        if csvWithInputData == None: logFile.write("Error: csvWithInputData does not exist. Checking spelling of variable name" + "\n")
        
        inputtype = loadedJson[0].get('inputtype')
        if inputtype == None: logFile.write("Error: inputtype does not exist. Checking spelling of variable name" + "\n")
except:
    logFile.write("Error: location_data_cleanup_config.json does not exist. Checking spelling of config file name" + "\n")


    logFile.close()

######  Reads and organizes data from CSV file ######
import os
import csv
import location_data_cleanup_config_reader

csvWithInputData = location_data_cleanup_config_reader.csvWithInputData

dirname = os.path.dirname(__file__)                     #Determine which directory we are in 
filename = os.path.join(dirname, csvWithInputData)

logFile = os.path.join(dirname,"csv_reader_log")
logFile = open (logFile, "w+")

filterList = []
valueList = []

try:
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter= ";")
        filterList = next(readCSV, None)        #strip headers into their own list

        counter = 1
        for row in readCSV:
            if len(row)==len(filterList):
                valueList.append(row)   #append first item in csv row to first list      
            else:
                logFile.write("CSV file is incorrectly formatted on line: " + str(counter) + "\n")
                break
        counter+=1
except:
    logFile.write("Specified CSV file is not found. Please check spelling of file name in config file." + "\n") 
logFile.close()


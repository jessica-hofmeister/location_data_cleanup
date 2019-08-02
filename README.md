README for Location Data Cleanup Project

This project is written in Python 3.6 using Google Places api and MySQL

Description
---
This project takes location information (address, name, or phone number), checks it against Google Places to get the most accurate data, and updates a specified Database Table with that information

Requirements
--
Information required to run:

1. Database Host

2. Database Username

3. Database Password

4. Google Places API Key

5. [inputtype](https://developers.google.com/places/web-service/search#FindPlaceRequests) for query
    1. `textquery`
    2. `phonenumber` (information on required phonenumber formatting can be found [here](https://developers.google.com/places/web-service/search#FindPlaceRequests))

6. Name of `CSV` file with location/phone number information

How It Works
---
On execution:

1. Optional: `location_data_cleanup_seed.py` creates tables with required schema (also deletes existing tables with the same name, so exercise caution here)

2. `location_data_cleanup_config_reader.py` and `location_data_cleanup_csv_reader.py` read and prepare user input from `location_data_cleanup_config.json` and the `CSV` file specified in the configurations

3. `location_data_cleanup_database_prep.py` takes the prepared data from `location_data_cleanup_csv_reader.py` and inserts it into `RelationshipTable` in preparation for making Places api calls

4. `location_data_cleanup_find_places.py` runs through all unprocessed entries in `RelationshipTable` (processed entries are flagged to prevent redundant api requests, therefore allowing the user to add rows to the table and run the script at any time with no wasteful cost) and makes a GET request to the Google Places API. The request returns Google's top location suggestion based on the `CSV` place data, with which the script will update the record in `RelationshipTable`

5. Also, if the location returned from the GET request has never been returned before (it has a unique place Id), the place Id is inserted into `DetailsTable` which contains all unique places that have been searched and the all available detailed information about it (hours, lat, lng, phone number, address, website, etc)

6. `location_data_cleanup_details_update.py` runs through all records in `DetailsTable` and updates the details for each place through a GET request to the Places API.  Note it only makes a request if the `Details` field is empty or the `DateUpdated` is earlier than Google's last update of the place

Things to Consider
---
1. The GET requests made to the Places API cost money. Each initial request for a place (based on `CSV` input and Processed field in `RelationshipTable`) costs $0.017 and each update request (based on place id and DateUpdated field in `DetailsTable`) costs $0.003. Please be aware of that so as to avoid large bills due to frivolous requests. Overall pricing information can be found [here](https://cloud.google.com/maps-platform/pricing/sheet/?__utma=102347093.2103585298.1563202231.1563302763.1563302763.1&__utmb=102347093.0.10.1563302763&__utmc=102347093&__utmx=-&__utmz=102347093.1563302763.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)&__utmv=-&__utmk=120154248&_ga=2.80602519.1462146930.1563292851-2103585298.1563202231), initial request pricing [here](https://developers.google.com/places/web-service/usage-and-billing#find-place), and detail update request pricing [here](https://developers.google.com/places/web-service/usage-and-billing#contact-data).

2. Place details are returned as a json object and dumped unceremoniously into a single field. SQL magic is requrired for any formatted extraction of data from that field.

3. It is important that the quotation marks are maintained in the `location_data_cleanup_config.json` file and in the `CSV` file specified in the config file.  If they are not, the api calls to Tableau will not work.

4. Commas and other seperating characters are not necessary in the `CSV` query data if textquery is specified. All non-alphanumeric data will be stripped out for GET request compatability

5. The "Record Id" column in the `CSV` file is not used in any way by the script. It is simply transferred to the `RelationshipTable` for trackability if pulling data from another database or table.  If not needed, simply set to an empty string.

6. "Type" refers to the type of establishment being searched for in the Places API. The list of supported types can be found [here](https://developers.google.com/places/web-service/supported_types).

7. The stance taken on bad requests (aka PlaceIds that become obsolete (due to the business closing, moving, etc) or no places matching a given description) is to not update them. Instead, these records are placed in a Failures Table for error tracking.


Modules and Packages used:
---
* MySQLdb (specifically mysqlclient)
* requests
* os
* path
* csv
* json

Example of a properly formatted `CSV` file 
---
A properly formatted `CSV` file looks as such, with the first row as headers and the following rows as corresponding values:

"Record Id";"Query Input";"Type"

"2345";"First Baptist Church North 7th Street";"Church"

"3344";"Lily's Daycare 123 West Sycamore New York, NY";"Daycare"

"2234";"Harry's Pet Store 332 South St. Huston, TX";"Pet store"


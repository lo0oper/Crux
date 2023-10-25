
# Crux
Crux a data visualizer application
=======

### ➡️ Click [here](https://www.loom.com/share/dd2c5c7bceaa4840a09753211c08c031) to see the demo of the application. I keep updating the demo with each functionality that I add to the application
### About Application
This is django application with no authentication right now, utilising sqlite database to store data.
Steps to run the application 
1. Go inside curx folder which is in parallel to manage.py by running  `cd Graphs/crux`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Run `python manage.py makemigrations`
This will start the application on port 8000 on your localhost.

### Functionalities
This application has the following endpoints currently. Inorder to user the application provide the openAI key in .env file as shown in env.example
#### Available endpoints - 
1. GET `/api/v1/csv` or `/api/v1/csv?file_id=${file_id}` to fetch all the files or a single file using fileid.
2. POST `/api/v1/csv`
sample curl
```
curl --location 'http://127.0.0.1:8000/api/v1/csv' \
--form 'document=@"/Users/ankushpandey/Downloads/csvs/Perform a trend analysis considering '\''spends'\'' and '\''clicks'\''.csv"' \
--form 'title="5th type of csv"' \
--form 'description="5th type of csv"'
```
3. GET `/api/v1/csv/config?file_id=${file_id}` to fetch schema configuration of an uploaded file using file_id.
4. GET `/api/v1/csv/config?file_id=${file_id}&possible_graphs=true` to fetch schema configuration and possible graphs as well.
5. POST `/api/v1/csv/graphs` to fetch possible graphs for provided config
req body:
```json
{
    "csv_config": {
        "Campaign Id": {
            "type": "string"
        },
        "Campaign Type": {
            "type": "string"
        },
        "Total Spend": {
            "type": "number"
        },
        "Total Revenue": {
            "type": "number"
        },
        "Combined Acos": {
            "type": "number"
        }
    }
}
```


### Steps to create the project
1. Created a project in Pycharm
2. Installed django using `pip install django`
3. Created django project `graph_analyser` using `django-admin startproject graph_analyser`
4. Go inside graph_analyser folder.
5. Run `python manage.py migrate` to manage migrations.
5. Run `python manage.py runserver` to start the server.




### Features
1. Used `livesync` for hot reloading django server.
2. Installed pgadmin to manage postgres server from web-browser like mysql workbench.
3. For accessing and viewing the database use this [sqlite chrome extension](https://chrome.google.com/webstore/detail/sqlite-manager/njognipnngillknkhikjecpnbkefclfe/related)
4. `csv_manager_csvdata` table has the csv files in document field


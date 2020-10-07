# PEAKY-dj
## Description
peaky_api is a Django API to manage mountain peaks with gepspatial data allows users to:
* Do CRUD operations for mountain peaks
* Manage all rejected connections coming from users not in withelisted country, with Django administration page.

## Technical stack
The API technical stack is as follows:
* Django Rest Framework
* PostgreSQL 11 wih Postgis extension
* geoip2 for ip filtering
* docker-compose

## Endpoints
* http://localhost:8080/admin/ : to manage models : AttemptFail model which trace rejected connections, and see locations in map for Peak model
* http://localhost:8080/api/peaks: to get all peaks, update or create peaks, delete all peaks
* http://localhost:8080/api/peaks/<int:pk>/: to get by one, update or crate by one, delete by one
* http://localhost:8080/api/peaks/<str:xmin>/<str:ymin>/<str:xmax>/<str:ymax>/: to get all peaks located in bounding box, the user must put at least for values to create bbox(Polygone) 
* http://localhost:8080/api/docs/: to get swagger docs

## Improvements
* Data base initialisation:
  Prepare dataset to import into the databse, would be better to use peaky.
* Improve CRUD process:
  Add Django validators to check upcoming data, and exceptions to treat the error cases.
* Configure correctly docker-compose :
  Currently, docker can translate the database host name 'HOST': 'db' to the right value.Probably because of the conflict between peaky_api localhost and my other projects localhost
* Add unit test, Testcase for example.


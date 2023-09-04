# sqlalchemy-challenge
- jupyter notebook and python file are within the SurfsUP folder.
- files downloaded are within the Resources folder.

# On the dynamic APIs: 
- /api/v1.0/start_date/<start_date> route will accept a start date as a parameter from the URL, and you can access this parameter in the route function using the start_date parameter. For example, if you want to get temperature statistics for the date "2016-08-23," you can use the URL /api/v1.0/start_date/2016-08-23.
- /api/v1.0/start__end_date/<start_date>/<end_date> route will accept a start date and an end date as parameters from the URL, and you can access these parameters in the  start_end_date route function as start_date and end_date. For example, if you want to get temperature statistics for the date range "2016-08-23  to 2017-07-15" you can use the URL /api/v1.0/start_end_date/2016-08-23/2017-07-15
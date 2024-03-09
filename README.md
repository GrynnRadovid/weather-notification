# Weather Notification
The scope of this project is to pull data from Current Weather data API and then compare the new data with the old data from a previous run, and if the treshold is exceeded, an email will be sent to the email address specified in config.json

As it is configured, the way threshold works is that if the previous value of the temperature +- treshold exceeds the newest value, a notification mail will be sent.

Server and Client can be run independently as a shared space is used to share data between them, in this case a mySQL database
## Setup dependencies
### System environment variables

**EMAIL_PASSWORD** - APP Password generated from gmail 2FA

**API_KEY** - API Token from http://api.openweathermap.org

**DB_PASSWORD** - Password for mySQL DB

### Virtual Environment and python dependencies
From the root of the project run:
```
./setup.sh
```
It should create the venv and install everything inside requirements.txt
### Database config
Current config uses:
```
    'user': 'TEST_USER',
    'password': os.getenv('DB_PASSWORD'),
    'host': '127.0.0.1',
    'database': '   weather_data'
```
To create it use:
```
CREATE DATABASE IF NOT EXISTS weather_data;
USE weather_data;

CREATE TABLE IF NOT EXISTS weather_updates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT,
    humidity FLOAT
);
```

### Config setup
Inside root of the project there is a config.json, replace values with an email address that you own, currently it is setup so that the mail is sent by that mail and the receiver is also that email address

After all of the above were set you should be able to run server.py and client.py independently using venv

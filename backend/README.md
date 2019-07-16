## run application on your machine

* ensure python3 is installed
* run the following command
```
pip3 install -r requirements.txt
python main.py
```

## run application as docker
```
docker-compose up
or
docker-compose up --build
```

## send notification

By default, it will use the console notification, this just print the notification to stdout.
If you want to use spark, use change the config referring to `config.py`.
Or you can write your own if you write your provider inheriting the `notification.Provider`

### setup webex-teams(spark)

* create a robot referring to https://developer.cisco.com/webex-teams/, you will get the token
* create a webex-teams room and add the robot to that team
* go to https://developer.webex.com/docs/api/v1/rooms/list-rooms to get the new created room id
* put the above info to the `config.py`

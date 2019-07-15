# TODO

## Todos
* move send spark notification part to a separted notification service. perhaps: celery with redis
* when used in docker, log will delay for quite a lot of time
* md5 for the image content, performance?
* spark send notification policy
* change image name, md5 for 2M data
* Keep the images for sometime, cronjob
* the GET API get the data ordered by date desc?
* add some token for security check
* sending request sometimes hang there when using AWS
* use celery to send spark msg
* ratelimit
* use ansible for deploy
* deploy the service in k3s
* image policy issue
* restrict IP to access the page
* make the pic short lived, use redis
* cronjob to create picture
* slow in the AWS machine

## Done

* apply for a new AWS machine
* alpine image cannot install eventlet
* add mock data

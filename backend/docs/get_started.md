
* change `/etc/hosts`
```
127.0.0.1 ppe-backend
```
* build image
```
docker build . -t containers.cisco.com/cocreate/ppe-backend
or
docker build . -f Dockerfile.prod -t containers.cisco.com/cocreate/ppe-backend:prod
```

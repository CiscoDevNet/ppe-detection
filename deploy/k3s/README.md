## Run PPE client in k3s

### In the master machine. (change the IP to your master IP)

* download binary and run master
```
curl -OL https://github.com/rancher/k3s/releases/download/v0.5.0/k3s | xargs chmod a+x
cp k3s /usr/local/bin/
k3s server --disable-agent --bind-address 10.140.92.58 --tls-san 10.140.92.58 --no-deploy traefik --no-flannel
```
* get the token
```
cat ~/.rancher/k3s/server/node-token
```

### in your jetson
```
curl -L https://github.com/rancher/k3s/releases/download/v0.5.0/k3s-arm64 -o k3s | xargs chmod a+x
cp k3s-arm64 /usr/local/bin/

export MASTER_ADDR=https://10.140.92.58:6443
export NODE_TOKEN=K10d5269251b8f3eeb7445ba67cb5c3781da83895d4336a1423f07669c2a4078f8d::node:somethingtotallyrandom

sudo k3s agent -s $MASTER_ADDR -t $NODE_TOKEN --no-flannel --docker --kubelet-arg image-gc-high-threshold=99 --kubelet-arg image-gc-low-threshold=98 --kubelet-arg network-plugin=
```


### in your own machine
* download kubectl
```
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl | xargs chmod a+x
chmod a+x
```
* get the kubeconfig and set env
```
scp master:~/.kube/k3s.yaml .
export KUBECONFIG=./k3s.yaml
```
* set host to access k8s dashboard, the IP is the jetson IP
```
10.140.41.135 dashboard.k3s.com
```
* deploy traefik
```
kubectl apply -f traefik.yml
```
* deploy kube dashboard
```
kubectl apply -f kubernetes-dashboard.yml
```
* get login token
```
kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep kubernetes-dashboard | awk '{print $1}') | awk '$1=="token:"{print $2}'
```
* open `dashboard.k3s.com`, use the token above to login

#### deploy ppe-demo client
* load the docker image `ppe-client`
* get the model, and move it to directory `/opt/ppe/model/`
* plugin USB camera
* on the machine your want show the screen(typicall the jetson with screen), let mark this machine as display-machine, run:
```
apt-get install socat
export DISPLAY=:0
xhost +
socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CONNECT:/tmp/.X11-unix/X0
```
* change the `DISPLAY` env to other the IP:0 of the display-machine in ppe.yml
* change the `camera_id` arg in command to camera2 if you want to set the second machine.
* make other changes to the env if neccessary. like full-screen, etc
* run start the kubectl
```
kubectl apply -f ppe.yml
```
* It may take several minutes for the ppe-client to begin to process video, just wait
* when it get started, visit the frontend URI to view the result

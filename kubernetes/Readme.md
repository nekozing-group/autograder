
`kubectl create serviceaccount my-server-sa`
kubectl apply -f my-server-role.yaml
kubectl apply -f my-server-rolebinding.yaml
kubectl apply -f your-deployment-file.yaml


create the deployment `kubectl apply -f autograder-deployment.yaml`  
`kubectl get pods -l app=autograder`
`kubectl delete service autograder-service`

```
eval $(minikube docker-env)
docker build -t autograder .
```

Run  
`kubectl apply -f autograder-deployment.yaml`  
  
Stop  
`kubectl delete service autograder-service`  
  
See logs  
`kubectl logs -f autograder-deployment-dbdcddd6-82skp` (whatever the deployment name is)  `kubectl get pods`
  
  
Exposing the service  
`kubectl expose deployment autograder-deployment --type=NodePort --port=8001`  
  
Find the nodeport  
`kubectl get svc`
  
Access the service  
`http://[NODE_IP]:[NODE_PORT]`  
  
To get the IP:  
`minikube ip`




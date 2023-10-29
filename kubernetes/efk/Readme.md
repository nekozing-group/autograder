minikube mount /home/nekozing/autograder-es-data-pv:/home/nekozing/autograder-es-data-pv  

kubectl port-forward es-cluster-0 9200:9200 --namespace=kube-logging  

kubectl exec -it es-cluster-0 -n kube-logging -- /bin/bash  


minikube mount /home/nekozing/autograder-es-data-pv:/home/nekozing/autograder-es-data-pv

kubectl port-forward es-cluster-0 9200:9200 --namespace=kube-logging
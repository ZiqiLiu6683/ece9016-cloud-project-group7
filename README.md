### ECE 9016 Cloud Project - Group 7
A flask web application connected to MySQL database, deployed on Google Kubernetes Engine (GKE).

## Prerequisites
Python 3.11+
MySQL Server
Docker
Google Cloud SDK (gcloud CLI)
kubectl

## Local Deployment
# Step1: Set Up Virtual Environment
python3 -m venv .venv
source .venv/bin/activate
# Step2: Install Dependencies
pip install -r requirements.txt
# Step3: Initialize Database
mysql -u root -p < db/init.sql
# Step4: Set Environment Variables
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=products_db
# Step5: Run Flask Application
cd app
python app.py
# Step6: Access Through Browser
http://127.0.0.1:5005

## Docker Build and Push
# Step1: Authenticate Docker with GCR
gcloud auth configure-docker
# Step2: Build Image
docker build -t gcr.io/ece9016-cloudproject-group7/webapp:v1 .
# Step3: Push Image
docker push gcr.io/ece9016-cloudproject-group7/webapp:v1

## Development Environment (Single Node Cluster)
# Step1: Create Cluster
gcloud container clusters create dev-cluster --num-nodes=1 --machine-type=e2-medium --disk-size=20GB --zone=us-central1-a
# Step2: Connect to Cluster
gcloud container clusters get-credentials dev-cluster --zone us-central1-a
# Step3: Deploy Database and Web App
kubectl apply -f k8s/dev/dev-db-pod.yaml
kubectl apply -f k8s/dev/dev-db-service.yaml
kubectl apply -f k8s/dev/dev-web-pod.yaml
kubectl apply -f k8s/dev/dev-web-service.yaml
# Step4: Initialize Database
kubectl exec -i db-pod -- mysql -u root -prootpassword < db/init.sql
# Step5: Verify and Access
kubectl get pods
kubectl get svc web-service
# Access through the EXTERNAL-IP shown by the command above

## Production Environment (3 Node Cluster, High Availability)
# Step1: Create Cluster (--disk-size=20GB to stay within GCP free-tier quota)
gcloud container clusters create prod-cluster --num-nodes=3 --machine-type=e2-medium --disk-size=20GB --zone=us-central1-a
# Step2: Connect to Cluster
gcloud container clusters get-credentials prod-cluster --zone us-central1-a
# Step3: Deploy All Resources
kubectl apply -f k8s/prod/
# Step4: Initialize Database
kubectl get pods -l app=db
kubectl exec -i <DB_POD_NAME> -- mysql -u root -prootpassword < db/init.sql
# Step5: Verify Pods Are Distributed Across Nodes
kubectl get pods -o wide
# Step6: Access Through Browser
kubectl get svc web-service
# Access through the EXTERNAL-IP shown by the command above

## High Availability Test
# Step1: List Running Pods
kubectl get pods -o wide
# Step2: Delete One Web Pod
kubectl delete pod <WEB_POD_NAME>
# Step3: Watch Recovery (~15 seconds)
kubectl get pods -o wide
# App stays accessible through the external IP the whole time

## Cleanup
gcloud container clusters delete dev-cluster --zone us-central1-a
gcloud container clusters delete prod-cluster --zone us-central1-a
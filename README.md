- How to use fastapi, postgresql and kubernetes.

### 1. Jenkinsfile

``` 
pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        DOCKER_IMAGE = 'hanoguz00/fastapi-app'
        DOCKER_TAG = 'latest'
        FASTAPI_DEPLOYMENT_FILE = 'fastapi-deployment.yaml'
        FASTAPI_SERVICE_FILE = 'fastapi-service.yaml'
        POSTGRES_DEPLOYMENT_FILE = 'postgres-deployment.yaml'
        POSTGRES_SERVICE_FILE = 'postgres-service.yaml'
        POSTGRES_PVC_FILE = 'postgres-pvc.yaml'
        INGRESS_FILE = 'ingress.yaml'
        NAMESPACE = 'default'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/KuserOguzHan/pipeline_postgresql_1.git'
            }
        }

        stage('Docker Login') {
            steps {
                script {
                    echo 'Logging into Docker Hub...'
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
                }
            }
        }

        stage('Push Docker Image to Hub') {
            steps {
                script {
                    echo 'Pushing Docker image to Docker Hub...'
                    sh 'docker push $DOCKER_IMAGE:$DOCKER_TAG'
                }
            }
        }

        stage('Deploy PostgreSQL') {
            steps {
                script {
                    echo 'Deploying PostgreSQL...'
                    sh 'kubectl --kubeconfig=$KUBE_CONFIG apply -f $POSTGRES_PVC_FILE -n $NAMESPACE'
                    sh 'kubectl --kubeconfig=$KUBE_CONFIG apply -f $POSTGRES_DEPLOYMENT_FILE -n $NAMESPACE'
                    sh 'kubectl --kubeconfig=$KUBE_CONFIG apply -f $POSTGRES_SERVICE_FILE -n $NAMESPACE'
                }
            }
        }

        stage('Check PostgreSQL Deployment Status') {
            steps {
                script {
                    echo 'Checking PostgreSQL deployment status...'
                    sh 'kubectl get pods -n $NAMESPACE'
                    sh 'kubectl get services -n $NAMESPACE'
                }
            }
        }

        stage('Deploy FastAPI App') {
            steps {
                script {
                    echo 'Deploying FastAPI application...'
                    sh 'kubectl --kubeconfig=$KUBE_CONFIG apply -f $FASTAPI_DEPLOYMENT_FILE -n $NAMESPACE'
                    sh 'kubectl --kubeconfig=$KUBE_CONFIG apply -f $FASTAPI_SERVICE_FILE -n $NAMESPACE'
                }
            }
        }

        stage('Check FastAPI Deployment Status') {
            steps {
                script {
                    echo 'Checking FastAPI deployment status...'
                    sh 'kubectl get pods -n $NAMESPACE'
                    sh 'kubectl get services -n $NAMESPACE'
                }
            }
        }

        stage('Deploy Ingress') {
            steps {
                script {
                    echo 'Deploying Ingress for FastAPI application...'
                    sh 'kubectl --kubeconfig=$KUBE_CONFIG apply -f $INGRESS_FILE -n $NAMESPACE'
                }
            }
        }

        stage('Check Ingress Status') {
            steps {
                script {
                    echo 'Checking Ingress status...'
                    sh 'kubectl get ingress -n $NAMESPACE'
                }
            }
        }

        stage('Access FastAPI Service via Minikube') {
            when {
                expression {
                    return sh(script: 'minikube status', returnStatus: true) == 0
                }
            }
            steps {
                script {
                    echo 'Accessing FastAPI service using Minikube...'
                    sh 'minikube service fastapi -n $NAMESPACE'
                }
            }
        }
    }
}

``` 

### 2. Connect Databese

``` 
kubectl get pods
``` 

```
kubectl exec -it <postgres-pod-name> -- psql -U postgres -d postgres
```

```
\l
```
### Show Tables

```
\dt
```
### Show information

```
select * from create_data;
```


### 3. Use information of project data

Samsung,64.0,4.0,6.5,5000.0,8.0,48.0,2.0,2.0,2.0,2.999
```
{
  "memory": 64.0,
  "ram": 4.0,
  "screen_size": 6.5,
  "power": 5000,
  "front_camera": 8.0,
  "rc1": 48.0,
  "rc3": 2.0,
  "rc5": 2.0,
  "rc7": 2.0
}
```

Samsung,128.0,6.0,6.5,4500.0,32.0,12.0,12.0,8.0,0.0,6.849

```
{
  "memory": 128.0,
  "ram": 6.0,
  "screen_size": 6.5,
  "power": 4500,
  "front_camera": 32.0,
  "rc1": 12.0,
  "rc3": 12.0,
  "rc5": 8.0,
  "rc7": 0.0
}
```

Oppo,64.0,4.0,6.52,4230.0,8.0,13.0,2.0,2.0,0.0,2.749
```
{
  "memory": 64.0,
  "ram": 4.0,
  "screen_size": 6.52,
  "power": 4230,
  "front_camera": 8.0,
  "rc1": 13.0,
  "rc3": 2.0,
  "rc5": 2.0,
  "rc7": 0.0
}
```

Xiaomi,64.0,3.0,6.53,5000.0,5.0,13.0,0.0,0.0,0.0,2.692
```
{
  "memory": 64.0,
  "ram": 3.0,
  "screen_size": 6.53,
  "power": 5000,
  "front_camera": 5.0,
  "rc1": 13.0,
  "rc3": 0.0,
  "rc5": 0.0,
  "rc7": 0.0
}
```

iPhone,64.0,4.0,6.1,3110.0,12.0,12.0,12.0,0.0,0.0,11.199
```
{
  "memory": 64.0,
  "ram": 4.0,
  "screen_size": 6.1,
  "power": 3110,
  "front_camera": 12.0,
  "rc1": 12.0,
  "rc3": 12.0,
  "rc5": 0.0,
  "rc7": 0.0
}
```






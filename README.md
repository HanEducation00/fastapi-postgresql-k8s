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
        TEST_DEPLOYMENT_FILE = 'k8s.test/fastapi-deployment-test.yaml'            // Test için deployment dosyan
        TEST_SERVICE_FILE = 'k8s.test/fastapi-service-test.yaml'                  // Test için service dosyan
        TEST_POSTGRES_DEPLOYMENT_FILE = 'k8s.test/postgres-deployment-test.yaml'  // Test için PostgreSQL deployment dosyan
        TEST_POSTGRES_SERVICE_FILE = 'k8s.test/postgres-service-test.yaml'        // Test için PostgreSQL service dosyan
        TEST_POSTGRES_PVC_FILE = 'k8s.test/postgres-pvc-test.yaml'                // Test için PostgreSQL PVC dosyan
        TEST_INGRESS_FILE = 'k8s.test/ingress-test.yaml'                          // Test ortamı için Ingress dosyan
        PROD_DEPLOYMENT_FILE = 'k8s.prod/fastapi-deployment-prod.yaml'            // Prod için deployment dosyan
        PROD_SERVICE_FILE = 'k8s.prod/fastapi-service-prod.yaml'                  // Prod için service dosyan
        PROD_POSTGRES_DEPLOYMENT_FILE = 'k8s.prod/postgres-deployment-prod.yaml'  // Prod için PostgreSQL deployment dosyan
        PROD_POSTGRES_SERVICE_FILE = 'k8s.prod/postgres-service-prod.yaml'        // Prod için PostgreSQL service dosyan
        PROD_POSTGRES_PVC_FILE = 'k8s.prod/postgres-pvc-prod.yaml'                // Prod için PostgreSQL PVC dosyan
        PROD_INGRESS_FILE = 'k8s.prod/ingress-prod.yaml'                          // Prod ortamı için Ingress dosyan
        APP_DEPLOYMENT_FILE = 'k8s.app/fastapi-deployment.yaml'                   // App için genel deployment dosyan
        APP_SERVICE_FILE = 'k8s.app/fastapi-service.yaml'                         // App için genel service dosyan
        APP_POSTGRES_DEPLOYMENT_FILE = 'k8s.app/postgres-deployment.yaml'         // App için genel PostgreSQL deployment dosyan
        APP_POSTGRES_SERVICE_FILE = 'k8s.app/postgres-service.yaml'               // App için genel PostgreSQL service dosyan
        APP_POSTGRES_PVC_FILE = 'k8s.app/postgres-pvc.yaml'                       // App için genel PostgreSQL PVC dosyan
        APP_INGRESS_FILE = 'k8s.app/ingress-prod.yaml'                            // App ortamı için Ingress dosyan
        TEST_NAMESPACE = 'test'                                                   // Test ortam namespace'i
        PROD_NAMESPACE = 'prod'                                                   // Prod ortam namespace'i
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

        stage('Deploy PostgreSQL to Test') {
            steps {
                script {
                    echo 'Deploying PostgreSQL in Test environment...'
                    sh 'kubectl apply -f $TEST_POSTGRES_PVC_FILE -n $TEST_NAMESPACE'
                    sh 'kubectl apply -f $TEST_POSTGRES_DEPLOYMENT_FILE -n $TEST_NAMESPACE'
                    sh 'kubectl apply -f $TEST_POSTGRES_SERVICE_FILE -n $TEST_NAMESPACE'
                }
            }
        }

        stage('Check PostgreSQL Deployment Status in Test') {
            steps {
                script {
                    echo 'Checking PostgreSQL deployment status in Test environment...'
                    sh 'kubectl get pods -n $TEST_NAMESPACE'
                    sh 'kubectl get services -n $TEST_NAMESPACE'
                }
            }
        }

        stage('Deploy FastAPI to Test') {
            steps {
                script {
                    echo 'Deploying FastAPI application to Test environment...'
                    sh 'kubectl apply -f $TEST_DEPLOYMENT_FILE -n $TEST_NAMESPACE'
                    sh 'kubectl apply -f $TEST_SERVICE_FILE -n $TEST_NAMESPACE'
                    sh 'kubectl apply -f $TEST_INGRESS_FILE -n $TEST_NAMESPACE'
                }
            }
        }

        stage('Check FastAPI Test Deployment Status') {
            steps {
                script {
                    echo 'Checking FastAPI deployment status in Test environment...'
                    sh 'kubectl get pods -n $TEST_NAMESPACE'
                    sh 'kubectl get services -n $TEST_NAMESPACE'
                    sh 'kubectl get ingress -n $TEST_NAMESPACE'
                }
            }
        }

        stage('Deploy PostgreSQL to Prod') {
            steps {
                script {
                    echo 'Deploying PostgreSQL in Prod environment...'
                    sh 'kubectl apply -f $PROD_POSTGRES_PVC_FILE -n $PROD_NAMESPACE'
                    sh 'kubectl apply -f $PROD_POSTGRES_DEPLOYMENT_FILE -n $PROD_NAMESPACE'
                    sh 'kubectl apply -f $PROD_POSTGRES_SERVICE_FILE -n $PROD_NAMESPACE'
                }
            }
        }

        stage('Check PostgreSQL Deployment Status in Prod') {
            steps {
                script {
                    echo 'Checking PostgreSQL deployment status in Prod environment...'
                    sh 'kubectl get pods -n $PROD_NAMESPACE'
                    sh 'kubectl get services -n $PROD_NAMESPACE'
                }
            }
        }

        stage('Deploy FastAPI to Prod') {
            steps {
                script {
                    echo 'Deploying FastAPI application to Prod environment...'
                    sh 'kubectl apply -f $PROD_DEPLOYMENT_FILE -n $PROD_NAMESPACE'
                    sh 'kubectl apply -f $PROD_SERVICE_FILE -n $PROD_NAMESPACE'
                    sh 'kubectl apply -f $PROD_INGRESS_FILE -n $PROD_NAMESPACE'
                }
            }
        }

        stage('Check FastAPI Prod Deployment Status') {
            steps {
                script {
                    echo 'Checking FastAPI deployment status in Prod environment...'
                    sh 'kubectl get pods -n $PROD_NAMESPACE'
                    sh 'kubectl get services -n $PROD_NAMESPACE'
                    sh 'kubectl get ingress -n $PROD_NAMESPACE'
                }
            }
        }

        // Deploy App Environment aşaması kaldırıldı.

        stage('Access FastAPI Service in Prod via Minikube') {
            when {
                expression {
                    return sh(script: 'minikube status', returnStatus: true) == 0
                }
            }
            steps {
                script {
                    echo 'FastAPI servisine Minikube üzerinden erişiliyor...'
                    sh 'minikube service fastapi --url -n $PROD_NAMESPACE'
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
kubectl get pods -n prod

kubectl get svc -n prod

kubectl get deployments -n prod

kubectl get ingress -n prod

kubectl delete all --all -n prod

kubectl delete all --all -n test




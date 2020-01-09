
pipeline {
  agent {
    kubernetes {
      label 'jqueryFlask'
    
      yaml """
apiVersion: v1
kind: Pod
metadata:
labels:
  component: ci
spec:
  # Use service account that can deploy to all namespaces
  serviceAccountName: cicd
  containers:
  - name: kubectl
    image: lachlanevenson/k8s-kubectl:v1.8.0
    command:
    - cat
    tty: true
  - name: python
    image: cpattanayak/python:v3
    command:
    - cat
    tty: true
  - name: docker
    image: docker:latest
    command:
    - cat
    tty: true
    volumeMounts:
    - mountPath: /var/run/docker.sock
      name: docker-sock
  volumes:
    - name: docker-sock
      hostPath:
        path: /var/run/docker.sock
  
"""
}
   }
   
  stages {
    
   
    stage('Build image') {
      steps {
        container('docker') {
		 git 'https://github.com/CPattanayak/jqueryflask.git'

         
          script {
                        def image = docker.build("cpattanayak/jqueryflask:$BUILD_NUMBER")
                        docker.withRegistry( '', "dockerhubid") {
                            image.push()
                 }
          }
        }
      }
    }
	 stage('Deploy') {
            steps {
                
                    container('kubectl') {
                       
                       
                       script{
                        def checkDeployment = sh(script: "kubectl get deployments | grep db-deployment", returnStatus: true)
                        if(checkDeployment != 0) {
                            sh "kubectl apply -f db-deployment.yaml"
                        }
                        sh "sed 's/<imageid>/$BUILD_NUMBER/g' deployment.yaml > deploy.yaml"
                        sh "cat deploy.yaml"
                        sh "kubectl apply -f deploy.yaml"
                        sh 'chmod 777 depl-sh.sh'
                        sh 'sh depl-sh.sh'
						
                       
                    }
                }
            }
        }
		stage('Integration Test') {
            steps {
                
                    container('python') {
                       
                   
                    sh 'pip install behave-webdriver'
                    sh 'chmod 777 run-sh.sh'
                    sh 'sh run-sh.sh'
				    
				  
                       
                    }
                }
            }
    }
	
}


microserviceName = "jqueryFlask"
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
		 git 'https://github.com/CPattanayak/${microserviceName}.git'

         
          script {
                        def image = docker.build("cpattanayak/${microserviceName}:$BUILD_NUMBER")
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
                        sh "kubectl get pods"
						
                       
                    }
                }
            }
        }
    }
}


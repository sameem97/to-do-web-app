pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE_REPO = credentials('DOCKER_IMAGE_REPO')
        MINIKUBE_HOST = credentials('MINIKUBE_HOST')
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        SECRET_KEY = credentials('SECRET_KEY')
        DATABASE_URL = credentials('DATABASE_URL')
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/sameem97/to-do-web-app.git'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE_REPO}:${DOCKER_TAG} .'
            }
        }
        
        stage('Test') {
            steps {
                script {
                    // Run tests inside the built Docker image
                    // The --rm flag ensures the container is removed after the test
                    // The -v $(pwd)/tests:/app/tests maps your local tests directory into the container
                    // This assumes app.py is in the root of your repo
                    sh "docker run --rm -e SECRET_KEY=${SECRET_KEY} -e DATABASE_URL=${DATABASE_URL} ${DOCKER_IMAGE_REPO}:${DOCKER_TAG} python -m pytest"
                }
            }
        }
        
        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    sh 'echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin'
                    sh 'docker push ${DOCKER_IMAGE_REPO}:${DOCKER_TAG}'
                }
            }
        }
        
        stage('Deploy to Minikube') {
            steps {
                sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@${MINIKUBE_HOST} "kubectl set image deployment/todo-app todo-app=${DOCKER_IMAGE_REPO}:${DOCKER_TAG}"
                '''
            }
        }
    }
}
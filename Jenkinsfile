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
                sh 'docker build --no-cache -t ${DOCKER_IMAGE_REPO}:${DOCKER_TAG} .'
            }
        }
        
        stage('Test') {
            steps {
                script {
                    // Create database tables before running tests
                    sh """
                        docker run --rm --entrypoint python \
                            -e SECRET_KEY=${SECRET_KEY} \
                            -e DATABASE_URL=${DATABASE_URL} \
                            -e PYTHONPATH=/app \
                            ${DOCKER_IMAGE_REPO}:${DOCKER_TAG} \
                            -c 'from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()'
                    """
                    
                    // Run tests with verbose output and proper environment
                    sh """
                        docker run --rm --entrypoint python \
                            -e SECRET_KEY=${SECRET_KEY} \
                            -e DATABASE_URL=${DATABASE_URL} \
                            -e PYTHONPATH=/app \
                            ${DOCKER_IMAGE_REPO}:${DOCKER_TAG} \
                            -m pytest -v --tb=short
                    """
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
                withCredentials([sshUserPrivateKey(credentialsId: 'MINIKUBE_SSH_KEY', keyFileVariable: 'SSH_KEY_FILE', usernameVariable: 'SSH_USERNAME')]) {
                    sh '''
                        ssh -i ${SSH_KEY_FILE} -o StrictHostKeyChecking=no ${SSH_USERNAME}@${MINIKUBE_HOST} "kubectl set image deployment/todo-app todo-app=${DOCKER_IMAGE_REPO}:${DOCKER_TAG}"
                    '''
                }
            }
        }
    }
}
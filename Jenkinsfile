pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Код получен из репозитория'
                sh 'ls -la'
            }
        }
        stage('Check Python') {
            steps {
                sh 'python3 --version'
            }
        }
        stage('Check Docker') {
            steps {
                sh 'docker --version'
            }
        }
    }
}
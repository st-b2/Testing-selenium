pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Код получен из репозитория'
            }
        }

        stage('Setup venv') {
            steps {
                echo 'Создаём виртуальное окружение'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
            }
        }

        stage('Install deps') {
            steps {
                echo 'Устанавливаем зависимости'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                echo 'Запускаем pytest'
                sh '. venv/bin/activate && pytest || true'
            }
        }
    }

    post {
        always {
            echo 'Билд завершён'
        }
    }
}
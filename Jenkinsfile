pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Код получен из репозитория'
            }
        }

        stage('Start Selenium') {
            steps {
                echo 'Запускаем Chrome в Docker'
                sh '''
                    docker rm -f selenium-chrome 2>/dev/null || true
                    docker run -d --name selenium-chrome \
                        -p 4444:4444 -p 7900:7900 \
                        --shm-size=2g \
                        selenium/standalone-chrome:latest
                '''
                // Ждём, пока контейнер поднимется
                sh 'sleep 5'
            }
        }

        stage('Setup venv') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
            }
        }

        stage('Install deps') {
            steps {
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest --grid-url=http://localhost:4444 \
                           --headless \
                           --html=reports/report.html --self-contained-html
                '''
            }
        }
    }

    post {
        always {
            echo 'Останавливаем Selenium'
            sh 'docker rm -f selenium-chrome 2>/dev/null || true'
        }
    }
}
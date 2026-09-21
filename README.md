# Selenium + pytest + Jenkins CI

Проект автоматизации UI-тестирования на **Python + Selenium + pytest** с полным CI/CD-пайплайном в **Jenkins**, запуском браузера в **Docker** и публикацией HTML-отчётов.

---

## 📋 Содержание

- [🎯 Что делает проект](#-что-делает-проект)
- [🛠 Стек технологий](#-стек-технологий)
- [🏗 Архитектура CI/CD](#-архитектура-cicd)
- [⚙️ Требования](#-требования)
- [🚀 Установка и запуск локально](#-установка-и-запуск-локально)
- [🔧 Настройка Jenkins](#-настройка-jenkins)
- [📜 Jenkinsfile](#-jenkinsfile)
- [🧰 Полезные команды](#-полезные-команды)
- [⚠️ Известные проблемы](#-известные-проблемы)

---

## 🎯 Что делает проект

- Открывает веб-форму [practice-automation.com/form-fields](https://practice-automation.com/form-fields/)
- Заполняет поля: **Name**, **Password**, **Email**, **Message**
- Отмечает **чекбоксы** (напитки) и **radio-кнопки** (цвет)
- Выбирает значение в **dropdown** (Automation)
- Отправляет форму и **проверяет alert** с подтверждением
- Генерирует **HTML-отчёт** с результатами

Тест запускается:
- ✅ **Локально** — в реальном Chrome на вашей машине
- ✅ **В CI** — в headless Chrome внутри Docker-контейнера через Jenkins
- ✅ **Через Selenium Grid** — удалённое подключение к браузеру

---

## 🛠 Стек технологий

| Компонент | Версия | Назначение |
|---|---|---|
| Python | 3.11+ | Язык |
| Selenium | 4.20+ | Управление браузером |
| pytest | 8.0+ | Фреймворк тестов |
| pytest-html | 4.0+ | HTML-отчёты |
| Faker | 30.0+ | Генерация тестовых данных |
| Chrome / Firefox | latest | Браузеры |
| Docker | 20.10+ | Изоляция браузера |
| Jenkins | 2.400+ | CI/CD-сервер |
| Ubuntu Server | 22.04+ | ОС для Jenkins |

---


### Ключевые файлы

**`pages/base_page.py`** — базовый класс со «safe» методами  
**`conftest.py`** — поддержка двух режимов: локальный Chrome или Selenium Grid

---

## 🏗 Архитектура CI/CD
<img width="311" height="445" alt="Screenshot_1" src="https://github.com/user-attachments/assets/55fcc146-f2ae-4ceb-9b3b-b7f362b8cf8a" />

---
## ⚙️ Требования

Локально
```text
    Python 3.11+
    Google Chrome (последняя версия)
    (Опционально) Docker Desktop — для запуска через Selenium Grid
```
На CI-сервере (VM)
```text
    Ubuntu Server 22.04+
    Java 21+
    Jenkins LTS
    Python 3.11+, python3-venv, python3-pip
    Docker + добавление пользователя jenkins в группу docker
```
---

## 🚀 Установка и запуск локально

1. Клонировать репозиторий
```bash
git clone https://github.com/st-b2/Testing-selenium.git
cd Testing-selenium
```
2. Создать виртуальное окружение
```bash
# Вариант 1: conda
conda env create -f environment.yml
conda activate selenium_env

# Вариант 2: venv
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
# или venv\Scripts\activate  # Windows
```
3. Установить зависимости
```bash
pip install -r requirements.txt
```
4. Запустить тест в видимом Chrome
```bash
pytest tests/test_main.py -v -s
```
5. Запустить через Selenium Grid (Docker)
```bash
# Запустить браузер в контейнере
docker run -d --name chrome -p 4444:4444 -p 7900:7900 \
    --shm-size=2g selenium/standalone-chrome:latest

# Запустить тесты через Grid
pytest --grid-url=http://localhost:4444 --headless -v

# Остановить контейнер
docker rm -f chrome
```
6. Посмотреть, что делает браузер (VNC)
Открыть в браузере: http://localhost:7900 — пароль: secret.

---

## 🔧 Настройка Jenkins
1. Установка Jenkins
```bash
# Java
sudo apt install -y fontconfig openjdk-17-jre

# Jenkins (через .deb — надёжнее, чем apt-репозиторий)
cd /tmp
curl -fsSLO https://get.jenkins.io/debian-stable/jenkins_2.568.3_all.deb
sudo dpkg -i jenkins_2.568.3_all.deb
sudo apt --fix-broken install -y

# Запуск
sudo systemctl enable --now jenkins

# Первичный пароль
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
2. Установка Python и Docker
```bash
sudo apt install -y python3 python3-pip python3-venv docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```
3. Установка плагинов

Manage Jenkins → Plugins → Available plugins:
```text
    HTML Publisher — публикация отчётов

    Git — интеграция с GitHub (обычно уже стоит)

    Pipeline — декларативные пайплайны (стоит)
```

4. Настроить доступ к GitHub

Manage Jenkins → Credentials → Add Credentials:
```text
    Kind: Username with password
    Username: ваш GitHub-логин
    Password: Personal Access Token (scope repo)
    ID: github-token
```
5. Создать Pipeline Job
```text
    New Item → Pipeline → имя test_selenium
    Pipeline → Definition: Pipeline script from SCM
    SCM: Git
    Repository URL: https://github.com/st-b2/Testing-selenium.git
    Credentials: github-token
    Branch Specifier: */main
    Script Path: Jenkinsfile
```

---

## 📜 Jenkinsfile
Полный пайплайн:

```groovy
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
                sh '''
                    docker rm -f selenium-chrome 2>/dev/null || true
                    docker run -d --name selenium-chrome \
                        -p 4444:4444 -p 7900:7900 \
                        --shm-size=2g \
                        selenium/standalone-chrome:latest
                '''
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
                    pytest --grid-url=http://localhost:4444 --headless \
                           --html=reports/report.html --self-contained-html
                '''
            }
        }
    }

    post {
        always {
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Selenium Test Report'
            ])
            sh 'docker rm -f selenium-chrome 2>/dev/null || true'
        }
    }
}
```
---

## 🧰 Полезные команды
Локально
```bash

# Один тест, подробный вывод
pytest tests/test_main.py -v -s

# Собрать тесты без запуска
pytest --collect-only

# Только smoke-тесты
pytest -m smoke

# Параллельно (pytest-xdist)
pytest -n 4

# Повторить упавшие тесты
pytest --reruns 2 --reruns-delay 1
```
Docker / Selenium
```bash

# Запустить Chrome
docker run -d --name chrome -p 4444:4444 -p 7900:7900 \
    --shm-size=2g selenium/standalone-chrome:latest

# Статус
docker ps

# Логи
docker logs chrome

# Удалить все контейнеры
docker rm -f $(docker ps -aq)
```
Jenkins (на VM)
```bash

# Статус
sudo systemctl status jenkins

# Перезапуск
sudo systemctl restart jenkins

# Логи
sudo journalctl -u jenkins -n 100

# Первичный пароль
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

---

## ⚠️ Известные проблемы
`ElementClickInterceptedException`

*Причина*: элемент перекрыт баннером/футером/popup.  
*Решение*: используется BasePage.click — прокрутка + JS-fallback.

`ModuleNotFoundError: No module named 'utils'`

*Причина*: отсутствует utils/__init__.py или неверная структура.  
*Решение*: файлы проекта должны быть в корне репозитория, в каждом пакете — __init__.py.

`pytest: error: unrecognized arguments: --html`

*Причина*: не установлен pytest-html.  
*Решение*: pip install pytest-html.

`failed to connect to github.com port 443`

*Причина*: у VM пропал интернет.  
*Решение*: переключить сеть VirtualBox с Bridged на NAT + Port Forwarding.

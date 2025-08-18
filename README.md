# Telegram Bot with Payments and Private Channel Access

Этот проект реализует Telegram-бота, который принимает платежи от пользователей и выдает доступ в приватный канал или чат после успешной оплаты.

## 🚀 Возможности
- Прием платежей через провайдера (heleket.com)
- Автоматическая проверка и обработка статуса счетов
- Выдача приглашения в приватный канал/чат после оплаты
- Управление подпиской (продление на 31 день)

## 📦 Установка и запуск

### 1. Подключение к серверу
Подключитесь к вашему серверу по **SSH**:
```bash
ssh user@your_server_ip
```

### 2. Установка Docker и Docker Compose
Обновите систему и установите Docker и Docker Compose этой комбинированной командой (Подходит для ubuntu 22.04):
```bash
sudo apt update &&
sudo apt upgrade -y &&
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done &&
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
&&
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 3. Клонирование репозитория
Загрузите проект через **SFTP**:

### 4. Переход в директорию проекта
```bash
cd heleket-subscription-bot
```

### 5. Настройка переменных окружения
Скопируйте файл `.env.dist` в `.env` и отредактируйте его:
```bash
cp .env.dist .env
nano .env
```

Укажите токен Telegram-бота, данные БД, данные для входа в админ панель и ключи платежного провайдера.
Порт админки можно поменять на 80.

### 6. Запуск контейнеров
Запустите проект в Docker:
```bash
docker-compose up -d
```

## 🔑 Доступ
После успешного запуска бот будет доступен в Telegram.
Пользователь после оплаты получит приглашение в приватный канал или чат.
Админ панель будет находится по адресу: http://your_server_ip:80/admin
---
👨‍💻 Автор: *@lovebloodanddiamonds*

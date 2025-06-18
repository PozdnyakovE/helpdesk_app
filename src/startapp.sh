#!/bin/sh
set -e

echo "⏳ Ожидаем доступность базы данных на $DB_HOST:$DB_PORT..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  echo "🕐 База данных пока недоступна — ждем..."
  sleep 1
done
echo "✅ База данных доступна!"

echo "📦 Запускаем миграции и приложение..."
exec python main.py
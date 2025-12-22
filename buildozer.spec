[app]

# Название приложения
title = WoL Remote Control

# Имя пакета (домен в обратном порядке)
package.name = com.yourname.wolremote

# Домен (для Google Play)
package.domain = com.yourname

# Исходный код
source.dir = .

# Главный файл приложения
source.include_exts = py,png,jpg,kv,atlas,json

# Версия
version = 1.0

# Требуемые разрешения
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# Особенности Android
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 31

# Архитектура
android.arch = arm64-v8a,armeabi-v7a

# Ориентация
orientation = portrait

# Полноэкранный режим
fullscreen = 0

# Виджет
android.meta_data = android.appwidget.provider=widget_provider.xml

# Иконка
icon.filename = assets/icon.png

# Зависимости
requirements = python3,kivy,requests

# Пакеты для включения
android.add_packages =

# Исключения
android.ignore_path =

[buildozer]

# Логи
log_level = 2
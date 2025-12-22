[app]

# Название приложения
title = WoL Remote

# Имя пакета
package.name = wolremote
package.domain = com.github

# Исходный код
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt

# Версия
version = 1.0

# Автор
author = GitHub User

# Требуемые библиотеки Python
requirements = python3,kivy==2.2.1,requests==2.31.0

# Android настройки
android.api = 33
android.minapi = 21
android.ndk = 25b

# Используйте новое название android.archs вместо старого android.arch
android.archs = arm64-v8a,armeabi-v7a

# Разрешения Android
android.permissions = INTERNET

# Ориентация экрана
orientation = portrait

# Полноэкранный режим
fullscreen = 0

# Ускорение сборки
android.accept_sdk_license = True

[buildozer]
log_level = 2

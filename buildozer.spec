[app]

# Название приложения
title = WoL Remote

# Имя пакета
package.name = wolremote
package.domain = com.github

# Исходный код
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# Версия
version = 1.0

# Требуемые библиотеки (минимальный набор для начала)
requirements = python3,kivy==2.1.0

# Android настройки
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21

# Используйте android.archs вместо android.arch
android.archs = arm64-v8a

# Разрешения
android.permissions = INTERNET

# Ориентация
orientation = portrait

# Логирование
log_level = 2

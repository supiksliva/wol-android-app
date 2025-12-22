[app]
title = WoL Remote Control
package.name = wolremote
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0
requirements = python3,kivy==2.2.0,requests

# Упрощаем архитектуру для первой сборки
android.arch = arm64-v8a  # или armeabi-v7a

android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.ndk_api = 21

# Базовые разрешения
android.permissions = INTERNET

# Отключаем некоторые проверки для ускорения
android.skip_update = False

[buildozer]
log_level = 2

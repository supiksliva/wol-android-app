[app]
title = WoL Remote
package.name = wolremote
package.domain = com.github

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0
version.code = 1

requirements = python3,kivy==2.1.0

# Используем стабильные версии
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a

android.permissions = INTERNET

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

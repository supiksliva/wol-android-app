[app]
title = WoL Remote
package.name = wolremote
package.domain = com.github

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0
version.code = 1

# Начинаем только с python3
requirements = python3

# Используем наш установленный SDK
android.sdk_path = ~/android-sdk
android.ndk_path = ~/android-sdk/ndk/25.2.9519653
android.auto_sdk = 0
android.auto_ndk = 0

android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.build_tools_version = 33.0.0

android.permissions = INTERNET

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

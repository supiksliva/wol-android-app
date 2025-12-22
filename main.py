from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
import requests
import json
import threading
from datetime import datetime
import socket
import socks  # pip install PySocks

class XrayWoLApp(App):
    def build(self):
        self.store = JsonStore('xray_wol_config.json')
        self.config = self.load_config()
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Заголовок
        title = Label(text='⚡ Xray WoL Remote', font_size=26, size_hint_y=0.1)
        layout.add_widget(title)
        
        # Раздел Xray настройки
        xray_section = BoxLayout(orientation='vertical', spacing=5)
        xray_section.add_widget(Label(text='Xray Proxy Settings', font_size=18, bold=True))
        
        self.xray_server = TextInput(
            hint_text='Xray Server IP/Domain',
            multiline=False,
            text=self.config.get('xray_server', '')
        )
        xray_section.add_widget(self.xray_server)
        
        self.xray_port = TextInput(
            hint_text='Xray Port',
            multiline=False,
            text=self.config.get('xray_port', '443')
        )
        xray_section.add_widget(self.xray_port)
        
        self.api_key = TextInput(
            hint_text='API Key (from VPS)',
            multiline=False,
            password=True,
            text=self.config.get('api_key', '')
        )
        xray_section.add_widget(self.api_key)
        
        layout.add_widget(xray_section)
        
        # Раздел ПК
        pc_section = BoxLayout(orientation='vertical', spacing=5)
        pc_section.add_widget(Label(text='PC Configuration', font_size=18, bold=True))
        
        self.pc_name = TextInput(
            hint_text='PC Name (optional)',
            multiline=False,
            text=self.config.get('pc_name', 'My PC')
        )
        pc_section.add_widget(self.pc_name)
        
        self.pc_mac = TextInput(
            hint_text='MAC Address (AA:BB:CC:DD:EE:FF)',
            multiline=False,
            text=self.config.get('pc_mac', '')
        )
        pc_section.add_widget(self.pc_mac)
        
        layout.add_widget(pc_section)
        
        # Кнопки действий
        btn_layout = BoxLayout(spacing=10, size_hint_y=0.15)
        
        self.wake_btn = Button(
            text='🔌 Wake PC via Xray',
            background_color=(0.2, 0.7, 0.3, 1),
            font_size=16
        )
        self.wake_btn.bind(on_press=self.wake_via_xray)
        btn_layout.add_widget(self.wake_btn)
        
        test_btn = Button(
            text='📡 Test Connection',
            background_color=(0.3, 0.5, 0.9, 1)
        )
        test_btn.bind(on_press=self.test_connection)
        btn_layout.add_widget(test_btn)
        
        layout.add_widget(btn_layout)
        
        # Статус
        self.status = Label(
            text='Ready to connect',
            size_hint_y=0.1,
            color=(0.8, 0.8, 0.8, 1)
        )
        layout.add_widget(self.status)
        
        # Быстрые действия (виджетный стиль)
        quick_layout = BoxLayout(spacing=5, size_hint_y=0.15)
        
        quick_wake = Button(
            text='⚡ Quick Wake',
            background_color=(0, 0.8, 0, 1)
        )
        quick_wake.bind(on_press=self.quick_wake)
        quick_layout.add_widget(quick_wake)
        
        save_btn = Button(
            text='💾 Save Config',
            background_color=(0.9, 0.6, 0.1, 1)
        )
        save_btn.bind(on_press=self.save_config)
        quick_layout.add_widget(save_btn)
        
        layout.add_widget(quick_layout)
        
        # История
        self.history = Label(
            text='Last actions will appear here',
            size_hint_y=0.2,
            font_size=12,
            color=(0.6, 0.6, 0.6, 1)
        )
        layout.add_widget(self.history)
        
        return layout
    
    def load_config(self):
        """Загрузка конфигурации"""
        default = {
            'xray_server': '',
            'xray_port': '5000',
            'api_key': '',
            'pc_name': 'My PC',
            'pc_mac': '',
            'history': []
        }
        
        if self.store.exists('config'):
            return self.store.get('config')
        return default
    
    def save_config(self, instance=None):
        """Сохранение конфигурации"""
        self.config.update({
            'xray_server': self.xray_server.text,
            'xray_port': self.xray_port.text,
            'api_key': self.api_key.text,
            'pc_name': self.pc_name.text,
            'pc_mac': self.pc_mac.text
        })
        
        self.store.put('config', **self.config)
        self.show_message('Settings Saved', 'Configuration saved successfully!')
    
    def wake_via_xray(self, instance):
        """Отправка WoL через Xray прокси"""
        if not all([self.xray_server.text, self.api_key.text, self.pc_mac.text]):
            self.show_message('Error', 'Please fill all required fields!')
            return
        
        self.wake_btn.disabled = True
        self.status.text = 'Connecting through Xray...'
        self.status.color = (1, 1, 0, 1)  # Yellow
        
        thread = threading.Thread(target=self.send_wol_request)
        thread.daemon = True
        thread.start()
    
    def send_wol_request(self):
        """Отправка HTTP запроса через Xray прокси"""
        try:
            # Настройка прокси (если используется SOCKS через Xray)
            proxies = {
                'http': f'socks5://{self.xray_server.text}:{self.xray_port.text}',
                'https': f'socks5://{self.xray_server.text}:{self.xray_port.text}'
            }
            
            # ИЛИ прямое подключение (если сервер WoL доступен)
            url = f"http://{self.xray_server.text}:5000/api/wake"
            
            headers = {
                'X-API-Key': self.config['api_key'],
                'Content-Type': 'application/json'
            }
            
            data = {
                'mac': self.config['pc_mac'],
                'pc_name': self.config['pc_name'],
                'timestamp': datetime.now().isoformat()
            }
            
            # Вариант 1: Через прокси (если Xray предоставляет SOCKS)
            # response = requests.post(url, json=data, headers=headers, 
            #                         proxies=proxies, timeout=15)
            
            # Вариант 2: Прямое подключение к WoL серверу на VPS
            response = requests.post(url, json=data, headers=headers, timeout=15)
            
            Clock.schedule_once(lambda dt: self.handle_response(response))
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.handle_error(str(e)))
    
    def handle_response(self, response):
        """Обработка ответа от сервера"""
        self.wake_btn.disabled = False
        
        if response.status_code == 200:
            result = response.json()
            self.status.text = f"✅ Success! {result.get('message', 'PC waking up...')}"
            self.status.color = (0, 1, 0, 1)  # Green
            
            # Добавляем в историю
            self.add_to_history(True, result.get('message', 'PC woke up'))
            
            # Уведомление
            self.show_message('Success', 'WoL command sent successfully!')
            
        else:
            self.status.text = f"❌ Error: {response.status_code}"
            self.status.color = (1, 0, 0, 1)  # Red
            self.add_to_history(False, f"HTTP {response.status_code}")
    
    def handle_error(self, error):
        """Обработка ошибки"""
        self.wake_btn.disabled = False
        self.status.text = f"❌ Connection failed: {error[:30]}..."
        self.status.color = (1, 0, 0, 1)
        self.add_to_history(False, error)
    
    def test_connection(self, instance):
        """Тестирование подключения"""
        if not self.xray_server.text:
            self.show_message('Error', 'Enter Xray server address first!')
            return
        
        self.status.text = 'Testing connection to VPS...'
        
        thread = threading.Thread(target=self.test_vps_connection)
        thread.daemon = True
        thread.start()
    
    def test_vps_connection(self):
        """Тест подключения к VPS"""
        try:
            url = f"http://{self.xray_server.text}:5000/api/health"
            response = requests.get(url, timeout=10)
            
            Clock.schedule_once(lambda dt: self.show_test_result(response))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_test_error(str(e)))
    
    def show_test_result(self, response):
        if response.status_code == 200:
            self.status.text = "✅ VPS WoL server is online!"
            self.status.color = (0, 1, 0, 1)
        else:
            self.status.text = f"⚠️ VPS responded with {response.status_code}"
            self.status.color = (1, 0.5, 0, 1)
    
    def show_test_error(self, error):
        self.status.text = f"❌ Cannot reach VPS: {error[:30]}..."
        self.status.color = (1, 0, 0, 1)
    
    def quick_wake(self, instance):
        """Быстрое включение без диалогов"""
        if not self.config.get('pc_mac'):
            self.show_message('Error', 'Configure MAC address first!')
            return
        
        self.status.text = 'Quick wake sending...'
        
        thread = threading.Thread(target=self.send_quick_wake)
        thread.daemon = True
        thread.start()
    
    def send_quick_wake(self):
        """Отправка быстрой команды"""
        try:
            url = f"http://{self.config['xray_server']}:5000/api/wake"
            headers = {'X-API-Key': self.config['api_key']}
            data = {'mac': self.config['pc_mac'], 'quick': True}
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                Clock.schedule_once(lambda dt: self.show_quick_result(True))
            else:
                Clock.schedule_once(lambda dt: self.show_quick_result(False))
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_quick_error(str(e)))
    
    def show_quick_result(self, success):
        if success:
            self.status.text = "✅ Quick wake sent!"
            self.status.color = (0, 1, 0, 1)
        else:
            self.status.text = "❌ Quick wake failed"
            self.status.color = (1, 0, 0, 1)
    
    def show_quick_error(self, error):
        self.status.text = f"❌ Error: {error[:20]}..."
        self.status.color = (1, 0, 0, 1)
    
    def add_to_history(self, success, message):
        """Добавление в историю"""
        history = self.config.get('history', [])
        
        entry = {
            'time': datetime.now().strftime('%H:%M:%S'),
            'success': success,
            'message': message[:50],
            'pc': self.config.get('pc_name', 'PC')
        }
        
        history.insert(0, entry)
        if len(history) > 5:
            history = history[:5]
        
        self.config['history'] = history
        self.update_history_display()
    
    def update_history_display(self):
        """Обновление отображения истории"""
        history = self.config.get('history', [])
        text = "Recent actions:\n"
        
        for item in history:
            icon = "✅" if item['success'] else "❌"
            text += f"{icon} {item['time']} - {item['message']}\n"
        
        self.history.text = text
    
    def show_message(self, title, message):
        """Показать сообщение"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=message))
        
        btn = Button(text='OK', size_hint=(1, 0.3))
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        
        popup.open()

if __name__ == '__main__':
    XrayWoLApp().run()
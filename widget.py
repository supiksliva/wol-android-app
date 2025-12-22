from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
import requests
import threading
from kivy.clock import Clock

class WolWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 5
        self.padding = 5
        
        self.store = JsonStore('wol_config.json')
        
        # Кнопка быстрого включения
        self.wake_btn = Button(
            text='Wake PC',
            size_hint=(1, 0.7),
            background_color=(0, 0.7, 0, 1)
        )
        self.wake_btn.bind(on_press=self.quick_wake)
        self.add_widget(self.wake_btn)
        
        # Статус
        self.status_label = Label(
            text='Ready',
            size_hint=(1, 0.3),
            font_size=10
        )
        self.add_widget(self.status_label)
        
        # Загружаем конфигурацию
        self.load_config()
    
    def load_config(self):
        """Загрузка последней конфигурации"""
        if self.store.exists('config'):
            config = self.store.get('config')
            self.vps_ip = config.get('vps_ip', '')
            self.vps_port = config.get('vps_port', '5000')
            self.pc_mac = config.get('pc_mac', '')
            self.pc_name = config.get('pc_name', 'PC')
            
            # Обновляем текст кнопки
            self.wake_btn.text = f'Wake {self.pc_name}'
    
    def quick_wake(self, instance):
        """Быстрое включение ПК"""
        if not all([self.vps_ip, self.pc_mac]):
            self.status_label.text = 'Not configured'
            return
        
        self.wake_btn.disabled = True
        self.status_label.text = 'Sending...'
        
        # Отправка в отдельном потоке
        thread = threading.Thread(target=self.send_wake)
        thread.daemon = True
        thread.start()
    
    def send_wake(self):
        """Отправка команды WoL"""
        try:
            url = f"http://{self.vps_ip}:{self.vps_port}/api/wake"
            data = {
                'mac': self.pc_mac,
                'quick': True
            }
            
            response = requests.post(url, json=data, timeout=10)
            
            # Обновляем UI
            Clock.schedule_once(lambda dt: self.update_widget_status(response))
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error(str(e)))
    
    def update_widget_status(self, response):
        """Обновить статус виджета"""
        self.wake_btn.disabled = False
        
        if response.status_code == 200:
            self.status_label.text = 'Sent!'
        else:
            self.status_label.text = 'Error'
    
    def show_error(self, error):
        """Показать ошибку"""
        self.wake_btn.disabled = False
        self.status_label.text = 'Failed'

class WolWidgetApp(App):
    def build(self):
        return WolWidget()

if __name__ == '__main__':
    WolWidgetApp().run()
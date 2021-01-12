from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from time import sleep
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore


# main screen 
class MainScreen(Screen):
    pass

# about screen
class AboutScreen(Screen):
    pass


# setting screen
class SettingScreen(Screen):
    pass


class CustomScreenManager(ScreenManager):
    app_state = JsonStore('application.json')
    default_data_id = 'switches'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.get_app_state(self.default_data_id)


    def get_app_state(self, data_id):
        """ Restore state of the application upon resumption."""
        try: 
            print(self.app_state.get(data_id))
        except:
            print(f'nothing found for {data_id}')


    def update_app_state(self, button, state):
        """ Update the state of the application. """
        if button.text == 'hybrid':
            self.app_state.put('hybrid', state=state)
        elif button.text == 'wind':
            self.app_state.put('wind', state=state)
        elif button.text == 'solar':
            self.app_state.put('solar', state=state)
        else:
            self.app_state.put('battery', state=state)


    def select_tab_item(self, tab_item, text):
        #tab_item.bold = True
        tab_item.color = (0.9, 1, 0.9, 1)
        print(tab_item.text)
        selected_tab = 'main_screen'
        if tab_item.text == 'about':
            selected_tab = 'about_screen'
        elif tab_item.text == 'dashboard':
            selected_tab = 'main_screen'
        elif tab_item.text == 'settings':
            selected_tab = 'settings_screen'
        return selected_tab


    def on_off(self, button, state, dot):
        if state == 'down':
            dot.background_color = (0, 1, 0, 1)
            button.custom_background_color = (0, 1, 0, 0.7)
            button.text = 'OFF'
        else:
            dot.background_color = (1, 0, 0, 1)
            button.custom_background_color = (1, 0, 0, 0.5)
            button.text = 'ON'
        self.update_app_state(button, state)
            

class MyLayout(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flag = False

Builder.load_file('settings.kv')
Builder.load_file('about.kv')
Builder.load_file('tabbedpannel.kv')
kv_layout = Builder.load_file('design.kv')

class HybridPowerSupply(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 0.1)
        return kv_layout


if __name__ == '__main__':
    HybridPowerSupply().run()
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from time import sleep
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from arduino_interface import SerialInterface
from kivy_garden.graph import MeshLinePlot, Graph


# instance SerialInterface
serial_interface = SerialInterface()

# main screen 
class MainScreen(Screen):
    pass

# about screen
class AboutScreen(Screen):
    pass


# setting screen
class SettingScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_enter(self, *args):
        # add available ports to the spinner
        self.ids.spinner.values = serial_interface.get_port_names()

    def get_selected_port(self, port_name):
        serial_port = serial_interface.connect_port(port_name)
        return self.connection_status(serial_port)

    def connection_status(self, serial_port):
        if serial_port:
            self.ids.status.text = 'Connected'
            self.ids.status.color = 'green'
        else:
            self.ids.status.text = 'not connected'
            self.ids.status.color = 'red'

    def refresh_port(self):
        """ Method to refresh spinner for available ports"""
        self.ids.spinner.text = 'available ports'
        self.ids.status.text = 'not connected'
        self.ids.status.color = 'red'


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
        # tab_item.bold = True
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

    def on_off(self, button, state, dot, sent_from):
        if state == 'down':
            dot.background_color = (0, 1, 0, 1)
            button.custom_background_color = (0, 1, 0, 0.7)
            button.text = 'OFF'
            if sent_from == 'hybrid':
                # connect hybrid
                serial_interface.connect_to_plant('h')
                pass
            elif sent_from == 'grid':
                # connect grid plant
                serial_interface.connect_to_plant('g')
            elif sent_from == 'solar':
                # connect solar plant
                serial_interface.connect_to_plant('s')
            elif sent_from == 'battery':
                serial_interface.connect_to_plant('b')
        else:
            dot.background_color = (1, 0, 0, 1)
            button.custom_background_color = (1, 0, 0, 0.5)
            button.text = 'ON'

            if sent_from == 'hybrid':
                # disconnect hybrid
                serial_interface.disconnect_from_plant('h')
                pass
            elif sent_from == 'grid':
                # disconnect grid
                serial_interface.disconnect_from_plant('g')
            elif sent_from == 'solar':
                # disconnect solar
                serial_interface.disconnect_from_plant('s')
            elif sent_from == 'battery':
                # disconnect battery
                serial_interface.disconnect_from_plant('b')
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
        Window.size = (1200, 700)
        return kv_layout


if __name__ == '__main__':
    HybridPowerSupply().run()

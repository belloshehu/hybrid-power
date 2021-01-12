from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from time import sleep
from kivy.uix.screenmanager import ScreenManager, Screen


#kv_layout = Builder.load_file('design.kv')
Builder.load_file('design.kv')

class MyLayout(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flag = False
    
    def select_tab_item(self, tab_item, text):
        tab_item.bold = True
        tab_item.background_color = (0.9, 1, 0.9, 1)


    def on_off(self, button, state, dot):
        if state == 'down':
            dot.background_color = (0, 1, 0, 1)
            button.custom_background_color = (0, 1, 0, 0.7)
            button.text = 'OFF'
        else:
            dot.background_color = (1, 0, 0, 1)
            button.custom_background_color = (1, 0, 0, 0.5)
            button.text = 'ON'
            


class HybridPowerSupply(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 0.1)
        return MyLayout()


if __name__ == '__main__':
    HybridPowerSupply().run()
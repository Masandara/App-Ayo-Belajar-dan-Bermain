from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.screenmanager import SlideTransition, FadeTransition, ScreenManager, Screen

class MenyusunSKScreen(Screen):
     def go_to_mempelajari(self):
        # Navigate back to MempelajariScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = 'mempelajari'

# Load the Alfabet.kv file manually
Builder.load_file('Mempelajari/menyusunsk.kv')
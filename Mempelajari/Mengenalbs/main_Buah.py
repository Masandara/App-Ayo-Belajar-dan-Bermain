from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.screenmanager import SlideTransition, FadeTransition, ScreenManager, Screen

class BuahScreen(Screen):
    def go_to_mengenalbs(self):
        # Navigate back to Mengenalbsscreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = 'mengenalbs'

# Load the Alfabet.kv file manually
Builder.load_file('Mempelajari/Mengenalbs/Buah.kv')
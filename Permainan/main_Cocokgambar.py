from kivy.uix.screenmanager import SlideTransition, FadeTransition, ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.properties import StringProperty, ListProperty
from kivy.animation import Animation
import random

class MencocokkanGambarScreen(Screen):
    def go_to_permainan(self):
        # Navigate back to MempelajariScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = 'permainan'
        
# Load the Alfabet.kv file manually
Builder.load_file('Permainan/cocokgambar.kv')
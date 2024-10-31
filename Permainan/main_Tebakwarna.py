from kivy.uix.screenmanager import (
    SlideTransition,
    FadeTransition,
    ScreenManager,
    Screen,
)
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.properties import StringProperty, ListProperty
from kivy.animation import Animation
import random
from kivy.clock import Clock


class TebakWarnaScreen(Screen):
    current_question = 0

    def on_enter(self):
        # Langsung memuat pertanyaan tanpa delay
        self.load_question()

    def load_question(self):
        # Define the questions and answers
        questions = [
            {
                "question": "MERAH",
                "answers": [
                    ("Merah", [1, 0, 0, 1]),
                    ("Hijau", [0, 1, 0, 1]),
                    ("Biru", [0, 0, 1, 1]),
                ],
            },
            {
                "question": "BIRU",
                "answers": [
                    ("Biru", [0, 0, 1, 1]),
                    ("Merah", [1, 0, 0, 1]),
                    ("Kuning", [1, 1, 0, 1]),
                ],
            },
            {
                "question": "HIJAU",
                "answers": [
                    ("Hijau", [0, 1, 0, 1]),
                    ("Hitam", [0, 0, 0, 1]),
                    ("Putih", [1, 1, 1, 1]),
                ],
            },
            {
                "question": "ORANGE",
                "answers": [
                    ("Orange", [1, 0.5, 0, 1]),
                    ("Ungu", [0.5, 0, 0.5, 1]),
                    ("Biru", [0, 0, 1, 1]),
                ],
            },
            {
                "question": "PUTIH",
                "answers": [
                    ("Putih", [1, 1, 1, 1]),
                    ("Merah", [1, 0, 0, 1]),
                    ("Hijau", [0, 1, 0, 1]),
                ],
            },
            {
                "question": "HITAM",
                "answers": [
                    ("Hitam", [0, 0, 0, 1]),
                    ("Kuning", [1, 1, 0, 1]),
                    ("Ungu", [0.5, 0, 0.5, 1]),
                ],
            },
            {
                "question": "KUNING",
                "answers": [
                    ("Kuning", [1, 1, 0, 1]),
                    ("Orange", [1, 0.5, 0, 1]),
                    ("Hijau", [0, 1, 0, 1]),
                ],
            },
            {
                "question": "UNGU",
                "answers": [
                    ("Ungu", [0.5, 0, 0.5, 1]),
                    ("Putih", [1, 1, 1, 1]),
                    ("Merah", [1, 0, 0, 1]),
                ],
            },
        ]

        # Pick a random question for the current session
        question_data = random.choice(questions)
        self.ids.question_label.text = question_data["question"]

        # Update button text and color for answers
        for i, answer_data in enumerate(question_data["answers"]):
            button = self.ids[f"answer_button_{i+1}"]
            button.text = answer_data[0]
            button.background_color = answer_data[1]

    def check_answer(self, selected_answer):
        # Define correct answer for each color
        correct_answers = {
            "MERAH": "Merah",
            "BIRU": "Biru",
            "HIJAU": "Hijau",
            "ORANGE": "Orange",
            "PUTIH": "Putih",
            "HITAM": "Hitam",
            "KUNING": "Kuning",
            "UNGU": "Ungu",
        }

        # Check if the selected answer is correct
        correct_answer = correct_answers.get(self.ids.question_label.text, "")
        if selected_answer == correct_answer:
            self.show_popup("Jawaban Benar!")
        else:
            self.show_popup("Jawaban Salah!")

    def show_popup(self, message):
        # Display popup message
        popup_content = BoxLayout(orientation="vertical")
        popup_content.add_widget(Label(text=message, font_size="30sp"))

        popup = Popup(
            title="", content=popup_content, size_hint=(0.6, 0.4), auto_dismiss=False
        )
        popup.open()

        # Set random delay for popup close and move to the next question
        random_popup_delay = random.uniform(
            2, 4
        )  # Random delay between 2 and 4 seconds
        Clock.schedule_once(lambda dt: self.next_question(popup), random_popup_delay)

    def next_question(self, popup):
        # Dismiss popup
        popup.dismiss()

        # Load a new question
        self.load_question()

    def go_to_permainan(self):
        # Navigate back to MempelajariScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = "permainan"


# Load the Alfabet.kv file manually
Builder.load_file("Permainan/tebakwarna.kv")

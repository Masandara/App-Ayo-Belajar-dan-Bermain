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
    questions = []  # Memuat semua pertanyaan warna tanpa duplikat
    previous_question = None  # Menyimpan soal sebelumnya untuk menghindari duplikasi

    def on_enter(self):
        self.generate_questions()  # Mengacak pertanyaan setiap kali halaman dimulai
        self.load_question()

    def generate_questions(self):
        # Define all questions with 10 unique colors
        all_questions = [
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
            {
                "question": "COKLAT",
                "answers": [
                    ("Coklat", [0.6, 0.3, 0, 1]),
                    ("Hijau", [0, 1, 0, 1]),
                    ("Biru", [0, 0, 1, 1]),
                ],
            },
            {
                "question": "ABU-ABU",
                "answers": [
                    ("Abu-abu", [0.5, 0.5, 0.5, 1]),
                    ("Merah", [1, 0, 0, 1]),
                    ("Kuning", [1, 1, 0, 1]),
                ],
            },
        ]
        # Randomize the questions order
        self.questions = random.sample(all_questions, len(all_questions))

    def load_question(self):
        while True:
            question_data = random.choice(self.questions)
            if question_data["question"] != self.previous_question:
                self.previous_question = question_data["question"]
                break

        self.ids.question_label.text = question_data["question"]
        answers = question_data["answers"]
        random.shuffle(answers)  # Shuffle answers for randomized positions

        # Update answer buttons
        for i, answer_data in enumerate(answers):
            button = self.ids[f"answer_button_{i+1}"]
            button.text = answer_data[0]
            button.background_color = answer_data[1]

    def check_answer(self, selected_answer):
        # Dictionary to check the correct answer
        correct_answers = {
            "MERAH": "Merah",
            "BIRU": "Biru",
            "HIJAU": "Hijau",
            "ORANGE": "Orange",
            "PUTIH": "Putih",
            "HITAM": "Hitam",
            "KUNING": "Kuning",
            "UNGU": "Ungu",
            "COKLAT": "Coklat",
            "ABU-ABU": "Abu-abu",
        }

        # Check the answer
        correct_answer = correct_answers.get(self.ids.question_label.text, "")
        if selected_answer == correct_answer:
            self.show_popup("Selamat, jawaban benar!", correct=True)
        else:
            self.show_popup("Jawaban salah, coba lagi!", correct=False)

    def show_popup(self, message, correct):
        # Display customized popup for correct/incorrect answer
        popup_content = BoxLayout(orientation="vertical")

        # Tampilkan pesan tanpa "icon jempol"
        popup_content.add_widget(Label(text=message, font_size="15sp"))

        popup = Popup(
            title="", content=popup_content, size_hint=(0.3, 0.25), auto_dismiss=False
        )
        popup.open()

        # Set delay before closing popup and moving to the next question
        delay = 1.5 if correct else 1.5  # Tambahkan durasi untuk jawaban salah
        Clock.schedule_once(lambda dt: self.next_question(popup, correct), delay)

    def next_question(self, popup, correct):
        popup.dismiss()
        if correct:
            self.load_question()  # Load a new question only if the answer was correct

    def go_to_permainan(self):
        # Navigate back to MempelajariScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = "permainan"


# Load the Alfabet.kv file manually
Builder.load_file("Permainan/tebakwarna.kv")

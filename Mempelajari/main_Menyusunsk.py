import random
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import (
    SlideTransition,
    FadeTransition,
    ScreenManager,
    Screen,
)
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.popup import Popup


class MenyusunSKScreen(Screen):
    current_question_index = 0
    questions = [
        {
            "image": "Image/Susun-kata/Sepeda.png",
            "choices": ["SE", "DE", "DA", "PE"],
            "correct_answer": ["SE", "PE", "DA"],
        },
        {
            "image": "Image/Susun-kata/Kereta.png",
            "choices": ["RE", "KA", "TA", "KE"],
            "correct_answer": ["KE", "RE", "TA"],
        },
        {
            "image": "Image/Susun-kata/Pepaya.png",
            "choices": ["PA", "PE", "YA", "AP"],
            "correct_answer": ["PE", "PA", "YA"],
        },
        {
            "image": "Image/Susun-kata/Brokoli.png",
            "choices": ["LI", "BRO", "BO", "KO"],
            "correct_answer": ["BRO", "KO", "LI"],
        },
        {
            "image": "Image/Susun-kata/Paprika.png",
            "choices": ["PA", "RI", "KA", "PRI"],
            "correct_answer": ["PA", "PRI", "KA"],
        },
        {
            "image": "Image/Susun-kata/Gurita.png",
            "choices": ["GU", "TA", "RI", "RA"],
            "correct_answer": ["GU", "RI", "TA"],
        },
        {
            "image": "Image/Susun-kata/Kelapa.png",
            "choices": ["LA", "KE", "PA", "KA"],
            "correct_answer": ["KE", "LA", "PA"],
        },
        {
            "image": "Image/Susun-kata/Durian.png",
            "choices": ["DU", "DA", "AN", "RI"],
            "correct_answer": ["DU", "RI", "AN"],
        },
        {
            "image": "Image/Susun-kata/Selada.png",
            "choices": ["LA", "SE", "DA", "LE"],
            "correct_answer": ["SE", "LA", "DA"],
        },
        {
            "image": "Image/Susun-kata/Jerapah.png",
            "choices": ["RA", "JE", "PH", "PAH"],
            "correct_answer": ["JE", "RA", "PAH"],
        },
        {
            "image": "Image/Susun-kata/Perahu.png",
            "choices": ["RA", "AH", "PE", "HU"],
            "correct_answer": ["PE", "RA", "HU"],
        },
    ]
    current_answer_index = 0  # Index jawaban saat ini

    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        self.load_question()

    def load_question(self):
        try:
            question = self.questions[self.current_question_index]
            self.ids.image_display.source = question["image"]
            shuffled_choices = question["choices"][:]
            random.shuffle(shuffled_choices)  # Mengacak pilihan jawaban
            for i, choice in enumerate(shuffled_choices):
                button = self.ids[f"choice_{i+1}"]
                button.text = choice
                button.disabled = False

            # Reset kolom jawaban dan index jawaban saat ini
            for i in range(3):
                self.ids[f"answer_{i+1}"].text = "---"
            self.current_answer_index = 0

        except Exception as e:
            print(f"Error in load_question: {e}")

    def check_answer(self, button, index):
        try:
            question = self.questions[self.current_question_index]
            correct_answer = question["correct_answer"]

            # Periksa apakah pilihan sesuai dengan urutan jawaban saat ini
            if button.text == correct_answer[self.current_answer_index]:
                self.ids[f"answer_{self.current_answer_index + 1}"].text = button.text
                button.disabled = True
                self.current_answer_index += 1  # Pindah ke index jawaban berikutnya

                # Periksa apakah semua jawaban sudah benar
                if self.current_answer_index == len(correct_answer):
                    self.show_popup()
            else:
                # Jika salah, pilihan tidak akan mengisi kolom jawaban
                print("Pilihan salah, silakan coba lagi.")

        except Exception as e:
            print(f"Error in check_answer: {e}")

    def show_popup(self):
        self.popup = Popup(
            title="Selamat!",
            content=Label(text="Jawaban Anda benar!"),
            size_hint=(None, None),
            size=(400, 200),
        )
        self.popup.open()

        # Tutup pop-up setelah 2 detik dan lanjut ke soal berikutnya
        Clock.schedule_once(self.close_popup_and_next_question, 2)

    def close_popup_and_next_question(self, dt):
        self.popup.dismiss()  # Tutup pop-up
        self.next_question()  # Panggil fungsi untuk soal berikutnya

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index >= len(self.questions):
            self.current_question_index = 0
        self.load_question()

    def go_to_mempelajari(self):
        # Navigate back to MempelajariScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = "mempelajari"


# Load the Alfabet.kv file manually
Builder.load_file("Mempelajari/menyusunsk.kv")

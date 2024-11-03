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


class MencocokkanGambarScreen(Screen):
    main_image_source = StringProperty("Image/Cocok-gambar/Soal/Soal1.png")
    correct_answer = "Image/Cocok-gambar/jawab12.png"

    # Daftar soal, termasuk main_image, correct_answer, dan pilihan jawabannya
    questions = [
        {
            "main_image": "Image/Cocok-gambar/Soal/Soal1.png",
            "correct_answer": "Image/Cocok-gambar/Jawab12.png",
            "answers": [
                "Image/Cocok-gambar/Jawab11.png",
                "Image/Cocok-gambar/Jawab12.png",
                "Image/Cocok-gambar/Jawab13.png",
            ],
        },
        {
            "main_image": "Image/Cocok-gambar/Soal/Soal2.png",
            "correct_answer": "Image/Cocok-gambar/Jawab23.png",
            "answers": [
                "Image/Cocok-gambar/Jawab23.png",
                "Image/Cocok-gambar/Jawab22.png",
                "Image/Cocok-gambar/Jawab21.png",
            ],
        },
        {
            "main_image": "Image/Cocok-gambar/Soal/Soal3.png",
            "correct_answer": "Image/Cocok-gambar/Jawab32.png",
            "answers": [
                "Image/Cocok-gambar/Jawab31.png",
                "Image/Cocok-gambar/Jawab32.png",
                "Image/Cocok-gambar/Jawab33.png",
            ],
        },
        {
            "main_image": "Image/Cocok-gambar/Soal/Soal4.png",
            "correct_answer": "Image/Cocok-gambar/Jawab43.png",
            "answers": [
                "Image/Cocok-gambar/Jawab41.png",
                "Image/Cocok-gambar/Jawab42.png",
                "Image/Cocok-gambar/Jawab43.png",
            ],
        },
        {
            "main_image": "Image/Cocok-gambar/Soal/Soal5.png",
            "correct_answer": "Image/Cocok-gambar/Jawab51.png",
            "answers": [
                "Image/Cocok-gambar/Jawab51.png",
                "Image/Cocok-gambar/Jawab52.png",
                "Image/Cocok-gambar/Jawab53.png",
            ],
        },
        {
            "main_image": "Image/Cocok-gambar/Soal/Soal6.png",
            "correct_answer": "Image/Cocok-gambar/Jawab62.png",
            "answers": [
                "Image/Cocok-gambar/Jawab61.png",
                "Image/Cocok-gambar/Jawab62.png",
                "Image/Cocok-gambar/Jawab63.png",
            ],
        },
    ]
    question_index = 0

    def on_pre_enter(self):
        self.load_next_question()

    def check_answer(self, selected_image_source):
        if selected_image_source == self.correct_answer:
            self.main_image_source = self.correct_answer
            self.ids.main_image.source = self.main_image_source
            self.show_popup(is_correct=True)
        else:
            self.show_popup(is_correct=False)

    def show_popup(self, is_correct):
        popup_content = BoxLayout(orientation="vertical")
        if is_correct:
            popup_content.add_widget(Label(text="Jawaban benar!", font_size="20sp"))
        else:
            popup_content.add_widget(Label(text="Jawaban salah!", font_size="20sp"))

        popup = Popup(
            title="Hasil",
            content=popup_content,
            size_hint=(0.4, 0.2),
            auto_dismiss=True,
        )
        popup.open()

        Clock.schedule_once(lambda dt: self.close_popup_and_next_question(popup), 2)

    def close_popup_and_next_question(self, popup):
        popup.dismiss()
        self.next_question()

    def next_question(self):
        self.question_index += 1
        if self.question_index < len(self.questions):
            self.load_next_question()
        else:
            print("Permainan selesai! Semua soal telah dijawab.")
            self.question_index = 0  # Reset index agar bisa mengulang soal

    def load_next_question(self):
        current_question = self.questions[self.question_index]
        self.main_image_source = current_question["main_image"]
        self.correct_answer = current_question["correct_answer"]
        self.ids.main_image.source = self.main_image_source
        # Memperbarui sumber gambar untuk pilihan jawaban
        self.ids.answer_1_img.source = current_question["answers"][0]
        self.ids.answer_2_img.source = current_question["answers"][1]
        self.ids.answer_3_img.source = current_question["answers"][2]

    def go_to_permainan(self):
        # Navigate back to MempelajariScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = "permainan"


# Load the Alfabet.kv file manually
Builder.load_file("Permainan/cocokgambar.kv")

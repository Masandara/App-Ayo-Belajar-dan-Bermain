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
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.animation import Animation
import random
from kivy.clock import Clock


class MencocokkanGambarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.question_index = 0
        self.total_questions = 10  # Atur jumlah total soal

    main_image_source = StringProperty("Image/Cocok-gambar/Soal/Soal1.png")
    correct_answer = "Image/Cocok-gambar/jawab12.png"
    current_question_label = StringProperty("")
    show_label = BooleanProperty(False)

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
            "label": "Bus Pariwisata",
        },
        {
            "main_image": "Image/Cocok-gambar/Soal/Soal2.png",
            "correct_answer": "Image/Cocok-gambar/Jawab23.png",
            "answers": [
                "Image/Cocok-gambar/Jawab22.png",
                "Image/Cocok-gambar/Jawab21.png",
                "Image/Cocok-gambar/Jawab23.png",
            ],
            "label": "Mobil Taxi",
        },
        {
            "main_image": "Image/Cocok-gambar/Soal/Soal3.png",
            "correct_answer": "Image/Cocok-gambar/Jawab32.png",
            "answers": [
                "Image/Cocok-gambar/Jawab31.png",
                "Image/Cocok-gambar/Jawab32.png",
                "Image/Cocok-gambar/Jawab33.png",
            ],
            "label": "Motor Sport",
        },
        {
            "main_image": "Image/Cocok-gambar/Soal/Soal4.png",
            "correct_answer": "Image/Cocok-gambar/Jawab43.png",
            "answers": [
                "Image/Cocok-gambar/Jawab41.png",
                "Image/Cocok-gambar/Jawab42.png",
                "Image/Cocok-gambar/Jawab43.png",
            ],
            "label": "Sepeda Balap",
        },
        {
            "main_image": "Image/Cocok-gambar/Soal/Soal5.png",
            "correct_answer": "Image/Cocok-gambar/Jawab51.png",
            "answers": [
                "Image/Cocok-gambar/Jawab51.png",
                "Image/Cocok-gambar/Jawab52.png",
                "Image/Cocok-gambar/Jawab53.png",
            ],
            "label": "Kapal Pesiar",
        },
        {
            "main_image": "Image/Cocok-gambar/Soal/Soal6.png",
            "correct_answer": "Image/Cocok-gambar/Jawab62.png",
            "answers": [
                "Image/Cocok-gambar/Jawab61.png",
                "Image/Cocok-gambar/Jawab63.png",
                "Image/Cocok-gambar/Jawab62.png",
            ],
            "label": "Pesawat terbang",
        },
        {
            "main_image": "Image/Cocok-gambar/Soal/Soal7.png",
            "correct_answer": "Image/Cocok-gambar/Jawab71.png",
            "answers": [
                "Image/Cocok-gambar/Jawab71.png",
                "Image/Cocok-gambar/Jawab72.png",
                "Image/Cocok-gambar/Jawab53.png",
            ],
            "label": "Ambulans",
        },
        {
            "main_image": "Image/Cocok-gambar/Soal/Soal8.png",
            "correct_answer": "Image/Cocok-gambar/Jawab81.png",
            "answers": [
                "Image/Cocok-gambar/Jawab62.png",
                "Image/Cocok-gambar/Jawab81.png",
                "Image/Cocok-gambar/Jawab83.png",
            ],
            "label": "Bus Sekolah",
        },
        {
            "main_image": "Image/Cocok-gambar/Soal/Soal9.png",
            "correct_answer": "Image/Cocok-gambar/Jawab91.png",
            "answers": [
                "Image/Cocok-gambar/Jawab63.png",
                "Image/Cocok-gambar/Jawab22.png",
                "Image/Cocok-gambar/Jawab91.png",
            ],
            "label": "Kucing",
        },
        {
            "main_image": "Image/Cocok-gambar/Soal/Soal10.png",
            "correct_answer": "Image/Cocok-gambar/Jawab101.png",
            "answers": [
                "Image/Cocok-gambar/Jawab101.png",
                "Image/Cocok-gambar/Jawab11.png",
                "Image/Cocok-gambar/Jawab42.png",
            ],
            "label": "Pisang",
        },
    ]
    question_index = 0

    def on_pre_enter(self):
        # Reset ke soal pertama setiap kali layar ini dimasuki
        self.question_index = 0
        self.load_next_question()

    def check_answer(self, selected_image_source):
        if selected_image_source == self.correct_answer:
            self.score += 10  # Tambahkan 10 poin untuk jawaban benar
            self.main_image_source = self.correct_answer
            self.ids.main_image.source = self.main_image_source
            self.show_label = True  # Tampilkan label jika jawaban benar
            self.current_question_label = self.questions[self.question_index]["label"]
            self.show_popup(is_correct=True)
        else:
            self.score += 0  # Tambahkan 0 poin untuk jawaban salah
            self.show_popup(is_correct=False)

    def show_popup(self, is_correct):
        popup_content = BoxLayout(orientation="vertical")
        if is_correct:
            popup_content.add_widget(
                Label(text="Selamat, jawaban benar!", font_size="15sp")
            )
        else:
            popup_content.add_widget(Label(text="Jawaban salah!", font_size="15sp"))

        popup = Popup(
            title="Hasil",
            content=popup_content,
            size_hint=(0.3, 0.25),
            auto_dismiss=True,
        )
        popup.open()

        Clock.schedule_once(lambda dt: self.close_popup_and_next_question(popup), 1.5)

    def close_popup_and_next_question(self, popup):
        popup.dismiss()
        self.show_label = False  # Sembunyikan label saat beralih ke soal berikutnya
        self.next_question()

    def next_question(self):
        # Periksa jika pertanyaan sudah mencapai total pertanyaan yang diinginkan
        self.question_index += 1
        if self.question_index < self.total_questions:
            self.load_next_question()
        else:
            # Tampilkan layar skor di akhir permainan
            self.show_score_screen()

    def load_next_question(self):
        # Muat soal berikutnya berdasarkan indeks saat ini
        current_question = self.questions[self.question_index]
        self.main_image_source = current_question["main_image"]
        self.correct_answer = current_question["correct_answer"]
        self.current_question_label = current_question.get("label", "")

        # Atur gambar dan reset tampilan
        self.ids.main_image.source = self.main_image_source
        self.ids.answer_1_img.source = current_question["answers"][0]
        self.ids.answer_2_img.source = current_question["answers"][1]
        self.ids.answer_3_img.source = current_question["answers"][2]

        # Sembunyikan label saat soal baru dimuat
        self.show_label = False

    def show_score_screen(self):
        # Set nilai skor ke final_score di ScoreScreen
        score_screen = self.manager.get_screen("score_screen")
        score_screen.final_score = str(self.score)  # Set nilai skor akhir

        # Pindah ke screen skor untuk menampilkan hasil
        self.manager.current = "score_screen"

    def go_to_permainan(self):
        # Navigate back to MempelajariScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = "permainan"


class ScoreScreen(Screen):
    final_score = StringProperty("")

    def on_enter(self):
        # Menampilkan skor akhir pada Label saat layar ini ditampilkan
        self.ids.score_label.text = f"{self.final_score}"

    def go_to_permainan(self):
        # Navigate back to MempelajariScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = "permainan"

    def go_to_layar(self):
        # Navigate to LayarScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = "layar"


# Load the Alfabet.kv file manually
Builder.load_file("Permainan/cocokgambar.kv")

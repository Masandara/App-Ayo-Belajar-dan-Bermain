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
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.animation import Animation
import random
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line


class CustomPopup(Popup):
    def __init__(self, title, message, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (None, None)
        self.size = (300, 150)

        # Bagian ini dihapus untuk menghilangkan garis tepi (outline)
        # with self.canvas.before:
        #     Color(0, 0, 0, 1)  # Hitam untuk garis tepi
        #     self.line = Line(
        #         rectangle=(self.x, self.y, self.width, self.height), width=1.5
        #     )
        #
        # self.bind(size=self._update_rect, pos=self._update_rect)

        self.content = BoxLayout(orientation="vertical", padding=10, spacing=10)

        message_label = Label(
            text=message, size_hint_y=None, height=40, color=(1, 1, 1, 1)
        )
        self.content.add_widget(message_label)

        Clock.schedule_once(lambda dt: self.dismiss(), 2)

    # Bagian ini dihapus karena sudah tidak perlu update outline
    # def _update_rect(self, *args):
    #     self.line.rectangle = (self.x, self.y, self.width, self.height)


class PenjumlahanScreen(Screen):
    angka1 = NumericProperty(0)
    angka2 = NumericProperty(0)
    soal = StringProperty("")
    buah_terpilih = StringProperty("")
    gambar_list = [
        "Image/Buah/Apel.png",
        "Image/Buah/Ceri.png",
        "Image/Buah/Lemon.png",
        "Image/Buah/Naga.png",
        "Image/Buah/Pisang.png",
        "Image/Buah/Mangga.png",
        # Tambahkan lebih banyak gambar sesuai kebutuhan
    ]

    def on_enter(self):
        Clock.schedule_once(lambda dt: self.generate_question())

    def generate_question(self):
        self.angka1 = random.randint(1, 10)
        self.angka2 = random.randint(1, 10)
        self.buah_terpilih = random.choice(self.gambar_list)

        self.ids.soal_label.text = f" {self.angka1}   +   {self.angka2}   =   ?"
        self.generate_answers()
        self.update_buah_images()

    def update_buah_images(self):
        # Kosongkan kotak kiri dan kanan sebelum menambahkan gambar baru
        self.ids.kotak_buah_a.clear_widgets()  # Menghapus semua gambar apel di kotak kiri
        self.ids.kotak_buah_b.clear_widgets()  # Menghapus semua gambar apel di kotak kanan

        # Menambahkan gambar apel sesuai angka1
        for _ in range(self.angka1):
            fruit_image = Image(
                source=self.buah_terpilih, size_hint=(None, None), size=(50, 50)
            )
            self.ids.kotak_buah_a.add_widget(fruit_image)

        # Menambahkan gambar sesuai angka2
        for _ in range(self.angka2):
            fruit_image = Image(
                source=self.buah_terpilih, size_hint=(None, None), size=(50, 50)
            )
            self.ids.kotak_buah_b.add_widget(fruit_image)

    def generate_answers(self):
        correct_answer = self.angka1 + self.angka2
        answers = [correct_answer]

        while len(answers) < 3:
            wrong_answer = random.randint(2, 20)
            if wrong_answer not in answers:
                answers.append(wrong_answer)

        random.shuffle(answers)

        # Assign answers to buttons
        self.ids.btn_jawaban_1.text = str(answers[0])
        self.ids.btn_jawaban_2.text = str(answers[1])
        self.ids.btn_jawaban_3.text = str(answers[2])

    def check_jawaban(self, jawaban):
        if jawaban == (self.angka1 + self.angka2):
            # Ganti tanda tanya dengan jawaban yang benar
            self.ids.soal_label.text = (
                f" {self.angka1}   +   {self.angka2}   =   {jawaban}"
            )
            self.show_popup("Hasil", "Selamat, jawaban benar!")
            Clock.schedule_once(lambda dt: self.generate_question(), 1.5)
        else:
            self.show_popup("Hasil", "Jawaban salah, coba lagi!")

    def show_popup(self, title, message):
        popup = CustomPopup(title=title, message=message)
        popup.open()

    def go_to_permainan(self):
        # Navigate back to MempelajariScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = "permainan"


# Load the Alfabet.kv file manually
Builder.load_file("Permainan/penjumlahan.kv")

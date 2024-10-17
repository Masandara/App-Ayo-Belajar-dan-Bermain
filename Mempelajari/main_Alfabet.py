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

class AlfabetScreen(Screen):
    def go_to_mempelajari(self):
        # Navigate back to MempelajariScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = 'mempelajari'

    huruf_saat_ini = StringProperty("")  # Menyimpan huruf soal saat ini
    opsi_jawaban = ListProperty(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                                 "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"])  # Menyimpan opsi jawaban

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.jumlah_benar = 0  # Menyimpan jumlah jawaban benar
        self.perbarui_opsi_jawaban()

    def periksa_jawaban(self, jawaban):
        if jawaban.lower() == self.huruf_saat_ini.lower():
            self.jumlah_benar += 1
            self.perbarui_opsi_jawaban()  # Perbarui opsi dan huruf soal setelah jawaban benar
            if self.jumlah_benar % 5 == 0:
                self.tampilkan_pop_up_good_job()

            # Animasi elegan untuk transisi huruf
            self.animate_transition()

    def perbarui_opsi_jawaban(self):
        # Ubah huruf soal saat ini
        huruf_alphabet = [chr(i) for i in range(65, 91)]  # Daftar huruf A-Z
        self.huruf_saat_ini = random.choice(huruf_alphabet)  # Pilih huruf secara acak
        
        # Ubah opsi jawaban dan pastikan satu jawaban yang benar ada di dalamnya
        benar = self.huruf_saat_ini  # Ambil huruf sebagai jawaban yang benar
        jawaban_lain = random.sample([chr(i) for i in range(65, 91) if chr(i) != benar], 4)  # Pilih 4 jawaban lain yang berbeda
        opsi = [benar] + jawaban_lain  # Gabungkan jawaban benar dengan jawaban lain
        random.shuffle(opsi)  # Acak opsi jawaban
        self.opsi_jawaban = opsi  # Set opsi jawaban baru

    def tampilkan_pop_up_good_job(self):
        konten = BoxLayout(orientation='vertical', padding=10)
        label_good_job = Label(text="Good Job", font_size='20sp')
        icon_jempol = Image(source='Icon/goodjob.png')  # Masukkan path untuk ikon jempol
        konten.add_widget(icon_jempol)
        konten.add_widget(label_good_job)

        pop_up = Popup(title="Good Job!",
                       content=konten,
                       size_hint=(0.5, 0.5))
        tutup_button = Button(text="Tutup", size_hint=(1, 0.2))
        tutup_button.bind(on_press=pop_up.dismiss)
        konten.add_widget(tutup_button)

        pop_up.open()

    def animate_transition(self):
        # Animasi untuk transisi huruf
        anim = Animation(opacity=0, duration=0.5) + Animation(opacity=1, duration=0.5)
        anim.start(self)

# Load the Alfabet.kv file manually
Builder.load_file('Mempelajari/Alfabet.kv')

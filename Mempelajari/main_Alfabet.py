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
from kivy.clock import Clock

huruf = [chr(i) for i in range(65, 91)]  # List huruf A sampai Z

class AlfabetScreen(Screen):
    def go_to_mempelajari(self):
        # Navigate back to MempelajariScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = 'mempelajari'

    huruf_saat_ini = StringProperty("")  # Menyimpan huruf soal saat ini
    opsi_jawaban = ListProperty(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"])  # Menyimpan opsi jawaban

    def __init__(self, **kwargs):
        super(AlfabetScreen, self).__init__(**kwargs)
        self.index_huruf = 0
        self.huruf_saat_ini = huruf[self.index_huruf]
        self.opsi_jawaban = self.acak_jawaban()

    def periksa_jawaban(self, jawaban):
        if jawaban == self.huruf_saat_ini:
            # Cek apakah sudah sampai ke huruf Z
            if self.index_huruf < len(huruf) - 1:
                self.index_huruf += 1
                self.huruf_saat_ini = huruf[self.index_huruf]
                self.opsi_jawaban = self.acak_jawaban()
                self.animasi_soal_dan_jawaban()
            else:
                # Jika sudah sampai Z, tampilkan pop-up dengan tombol tutup
                self.tampilkan_pop_up(True)
        else:
            self.tampilkan_pop_up(False)

    def acak_jawaban(self):
        # Ambil 5 huruf berikutnya tanpa double
        opsi = huruf[self.index_huruf:self.index_huruf+5]
        random.shuffle(opsi)
        return opsi

    def tampilkan_pop_up(self, huruf_terakhir):
        if huruf_terakhir:
            content = Button(text="Huruf terakhir! Tutup", size_hint=(0.8, 0.2))
            popup = Popup(title="Selesai", content=content, size_hint=(0.6, 0.6))
            content.bind(on_press=popup.dismiss)
            popup.open()
        else:
            # Wadah untuk ikon dan teks
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            
            # Menambahkan ikon "Good Job"
            icon = Image(source='Icon/goodjob.png', size_hint=(0.5, 0.5))  # Ganti dengan path gambar
            
            # Label "Good Job!"
            label = Label(text="Good Job!", size_hint=(0.8, 0.2))
            
            # Menambahkan ikon dan label ke dalam layout
            layout.add_widget(icon)
            layout.add_widget(label)
            
            # Membuat pop-up
            popup = Popup(title="Selamat", content=layout, size_hint=(0.6, 0.6))
            popup.open()
            
            # Tutup pop-up setelah 2 detik
            Clock.schedule_once(lambda dt: popup.dismiss(), 2)

    def animasi_soal_dan_jawaban(self):
        # Animasi pada soal dan jawaban
        animasi_soal = Animation(opacity=0, duration=0.5) + Animation(opacity=1, duration=0.5)
        animasi_jawaban = Animation(opacity=0, duration=0.5) + Animation(opacity=1, duration=0.5)

        # Terapkan animasi hanya pada label soal dan grid jawaban
        animasi_soal.start(self.ids.soal_label)  # Label soal
        animasi_jawaban.start(self.ids.grid_jawaban)  # Grid jawaban

# Load the Alfabet.kv file manually
Builder.load_file('Mempelajari/Alfabet.kv')

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
        self.jawaban_benar_counter = 0  # Tambahkan penghitung jawaban benar
        self.huruf_saat_ini = self.get_huruf_saat_ini()  # Panggil metode untuk mendapatkan huruf
        self.opsi_jawaban = self.acak_jawaban()
        
    def get_huruf_saat_ini(self):
        # Mengembalikan huruf besar dan kecil
        return f"{huruf[self.index_huruf]}{huruf[self.index_huruf].lower()}"

    # Fungsi untuk memeriksa jawaban
    def periksa_jawaban(self, jawaban):
        if jawaban == huruf[self.index_huruf]:  # Periksa jawaban dengan huruf besar saja
            self.jawaban_benar_counter += 1

            if self.jawaban_benar_counter % 5 == 0:
                self.tampilkan_pop_up(False)

            if self.index_huruf < len(huruf) - 1:
                self.index_huruf += 1
                self.huruf_saat_ini = self.get_huruf_saat_ini()  # Update menggunakan metode

                self.opsi_jawaban = self.acak_jawaban()

                if self.index_huruf >= len(huruf) - 4:
                    sisa_huruf = len(huruf) - self.index_huruf
                    self.sesuaikan_grid_layout(sisa_huruf)

                self.animasi_soal_dan_jawaban()
            else:
                self.tampilkan_pop_up(True)
        else:
            # Tidak ada pop-up jika jawaban salah, hanya abaikan
            pass

    def acak_jawaban(self):
        # Ambil 5 huruf berikutnya tanpa double
        if self.index_huruf >= len(huruf) - 4:
            opsi = huruf[self.index_huruf:]
        else:
            opsi = huruf[self.index_huruf:self.index_huruf+5]
        random.shuffle(opsi)
        return opsi

    def tampilkan_pop_up(self, huruf_terakhir):
        if huruf_terakhir:
            content = Button(text="Huruf terakhir! Tutup", size_hint=(0.8, 0.2))
            popup = Popup(
                title=" ",
                separator_height=0,
                content=content, 
                size_hint=(0.6, 0.6),
                background_color=(1, 1, 1, 1)  # Warna putih untuk latar belakang
            )
            content.bind(on_press=popup.dismiss)
            popup.open()
        else:
            # Wadah untuk ikon dan teks
            layout = BoxLayout(
                orientation='vertical', 
                padding=70, 
                spacing=50, 
                size_hint=(1, 1)
            )
            
            # Menambahkan ikon "Good Job" yang diratakan di tengah
            icon = Image(
                source='Icon/goodjob.png', 
                size_hint=(None, None), 
                size=(150, 150),
                pos_hint={'center_x': 0.5, 'top': 0.5}
            )
            icon.bind(size=lambda instance, size: icon.center_x)

            # Label "Good Job!" dengan teks di rata tengah
            label = Label(
                text="Good Job!",
                font_name='Font/PoetsenOne-Regular.ttf',
                size_hint=(1, 0.2), 
                halign='center', 
                valign='middle', 
                font_size='24sp',
                color=(1, 1, 1, 1)  # Teks hitam
            )
            label.bind(size=label.setter('text_size'))  # Untuk memastikan teks di tengah

            # Menambahkan ikon dan label ke dalam layout
            layout.add_widget(icon)
            layout.add_widget(label)

            # Membuat pop-up dengan warna latar belakang putih
            popup = Popup(
                title=" ",
                separator_height=0,  # Menghilangkan garis separator
                content=layout,
                size_hint=(0.6, 0.6),
                background_color=(1, 1, 1, 1),  # Warna latar belakang putih (RGBA)
            )
            popup.open()

            # Tutup pop-up setelah 1.5 detik
            Clock.schedule_once(lambda dt: popup.dismiss(), 1.8)


    def animasi_soal_dan_jawaban(self):
        # Animasi pada soal dan jawaban
        animasi_soal = Animation(opacity=0, duration=0.5) + Animation(opacity=1, duration=0.5)
        animasi_jawaban = Animation(opacity=0, duration=0.5) + Animation(opacity=1, duration=0.5)

        # Terapkan animasi hanya pada label soal dan grid jawaban
        animasi_soal.start(self.ids.soal_label)  # Label soal
        animasi_jawaban.start(self.ids.grid_jawaban1)  # Grid jawaban
        animasi_jawaban.start(self.ids.grid_jawaban2)  # Grid jawaban
    
    def sesuaikan_grid_layout(self, sisa_huruf):
        """
        Fungsi untuk menyesuaikan GridLayout ketika mendekati huruf terakhir (W-Z).
        Akan menampilkan jumlah opsi yang sesuai dengan huruf yang tersisa.
        """
        if sisa_huruf == 1:
            # Hanya satu huruf tersisa
            self.ids.grid_jawaban1.clear_widgets()
            self.ids.grid_jawaban2.clear_widgets()
            
            # Buat satu tombol di grid_jawaban1
            self.ids.grid_jawaban1.add_widget(self.buat_button(self.opsi_jawaban[0]))

        elif sisa_huruf == 2:
            # Dua huruf tersisa
            self.ids.grid_jawaban1.clear_widgets()
            self.ids.grid_jawaban2.clear_widgets()

            # Buat dua tombol di grid_jawaban1
            self.ids.grid_jawaban1.add_widget(self.buat_button(self.opsi_jawaban[0]))
            self.ids.grid_jawaban1.add_widget(self.buat_button(self.opsi_jawaban[1]))

        elif sisa_huruf == 3:
            # Tiga huruf tersisa
            self.ids.grid_jawaban1.clear_widgets()
            self.ids.grid_jawaban2.clear_widgets()

            # Buat tiga tombol di grid_jawaban1
            self.ids.grid_jawaban1.add_widget(self.buat_button(self.opsi_jawaban[0]))
            self.ids.grid_jawaban1.add_widget(self.buat_button(self.opsi_jawaban[1]))
            self.ids.grid_jawaban1.add_widget(self.buat_button(self.opsi_jawaban[2]))

        elif sisa_huruf == 4:
            # Empat huruf tersisa
            self.ids.grid_jawaban1.clear_widgets()
            self.ids.grid_jawaban2.clear_widgets()

            # Buat tiga tombol di grid_jawaban1 dan satu di grid_jawaban2
            self.ids.grid_jawaban1.add_widget(self.buat_button(self.opsi_jawaban[0]))
            self.ids.grid_jawaban1.add_widget(self.buat_button(self.opsi_jawaban[1]))
            self.ids.grid_jawaban1.add_widget(self.buat_button(self.opsi_jawaban[2]))
            self.ids.grid_jawaban2.add_widget(self.buat_button(self.opsi_jawaban[3]))

        else:
            # Jika lebih dari 4 huruf tersisa, tampilkan normal seperti biasa
            self.ids.grid_jawaban1.clear_widgets()
            self.ids.grid_jawaban2.clear_widgets()

            for i in range(3):
                self.ids.grid_jawaban1.add_widget(self.buat_button(self.opsi_jawaban[i]))

            for i in range(3, len(self.opsi_jawaban)):
                self.ids.grid_jawaban2.add_widget(self.buat_button(self.opsi_jawaban[i]))


# Load the Alfabet.kv file manually
Builder.load_file('Mempelajari/Alfabet.kv')

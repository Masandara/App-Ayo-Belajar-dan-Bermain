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


class MenyusunSKScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.jawaban_benar = ""
        self.jawaban_terpilih = []
        self.soal_list = [
            {"gambar": "Image/Susun-kata/Mobil.png", "jawaban": ["MO", "BIL"]},
            {"gambar": "Image/Susun-kata/Sepeda.png", "jawaban": ["SE", "PE", "DA"]},
            {"gambar": "Image/Susun-kata/Motor.png", "jawaban": ["MO", "TOR"]},
            {"gambar": "Image/Susun-kata/Perahu.png", "jawaban": ["PE", "RA", "HU"]},
            {"gambar": "Image/Susun-kata/Becak.png", "jawaban": ["BE", "CAK"]},
            {
                "gambar": "Image/Susun-kata/Helikopter.png",
                "jawaban": ["HELI", "KOP", "TER"],
            },
            # Tambahkan soal lainnya sesuai kebutuhan
        ]
        self.load_random_soal()

    def on_enter(self):
        # Randomisasi soal setiap kali layar diakses
        self.load_random_soal()

    def load_random_soal(self):
        # Mengambil soal secara acak
        soal = random.choice(self.soal_list)
        self.ids.gambar_utama.source = soal["gambar"]
        self.jawaban_benar = soal["jawaban"]
        self.jawaban_terpilih = []

        # Mengacak letak jawaban
        jawaban_acak = random.sample(soal["jawaban"], len(soal["jawaban"]))

        # Menampilkan opsi jawaban secara acak
        for i, box in enumerate(self.ids.opsi_jawaban.children):
            if i < len(jawaban_acak):
                box.children[0].text = jawaban_acak[i]
            else:
                box.children[0].text = ""

    def pilih_jawaban(self, teks):
        # Memasukkan jawaban ke dalam jawaban yang dipilih jika belum lengkap
        if len(self.jawaban_terpilih) < len(self.jawaban_benar):
            self.jawaban_terpilih.append(teks)

            # Memperbarui label jawaban di bawah gambar
            jawaban_label = "     ".join(self.jawaban_terpilih)
            self.ids.label_jawaban.text = jawaban_label

            # Animasi saat jawaban benar
            selected_label = Label(text=teks, font_size="30sp", color=(0, 0, 0, 1))
            self.ids.float_layout.add_widget(
                selected_label
            )  # Tambahkan widget label sementara

            anim = Animation(
                center_y=self.ids.label_jawaban.center_y, d=0.5, t="out_bounce"
            )
            anim.start(selected_label)

            # Cek apakah jawaban sudah lengkap dan benar
            if len(self.jawaban_terpilih) == len(self.jawaban_benar):
                if self.jawaban_terpilih == self.jawaban_benar:
                    # Tunggu sebentar sebelum lanjut ke soal berikutnya
                    anim.bind(on_complete=lambda *args: self.load_random_soal())
                else:
                    # Reset jawaban jika salah
                    self.jawaban_terpilih = []
                    self.ids.label_jawaban.text = "----     ----     ----"

    def go_to_mempelajari(self):
        # Navigate back to MempelajariScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = "mempelajari"


# Load the Alfabet.kv file manually
Builder.load_file("Mempelajari/menyusunsk.kv")

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.screenmanager import (
    SlideTransition,
    FadeTransition,
    ScreenManager,
    Screen,
)
from kivy.animation import Animation
from kivy.core.audio import SoundLoader


class SayurScreen(Screen):
    sayur_list = [
        "tomat",
        "wortel",
        "kentang",
        "kubis",
        "terong",
        "jagung",
        "bawang putih",
    ]
    sound_files = {
        "tomat": "sSounds/Tomat.MP3",
        "wortel": "sSounds/Wortel.MP3",
        "kentang": "sSounds/Kentang.MP3",
        "kubis": "sSounds/Kubis.MP3",
        "terong": "sSounds/Terong.MP3",
        "jagung": "sSounds/Jagung.MP3",
        "bawang putih": "sSounds/Bawangputih.MP3",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_index = 0
        self.outline_widget = None
        self.sound = None

    def on_enter(self):
        # Reset ke tampilan awal (soal pertama) setiap kali masuk ke layar ini
        self.current_index = 0
        self.outline_widget = self.ids.outline
        self.update_outline_position()
        self.update_question()
        self.play_backsound()

    def update_outline_position(self):
        if not self.outline_widget:
            self.outline_widget = self.ids.outline

        # Ambil widget jawaban sesuai dengan buah saat ini
        current_sayur = self.sayur_list[self.current_index]
        target_widget = self.ids[f"jawaban_{current_sayur}"]

        # Atur ukuran outline sedikit lebih besar dari target_widget (misalnya, gambar sayur)
        buffer_size = 29.9  # Tambahkan 20 piksel ke ukuran outline
        self.outline_widget.size = (
            target_widget.width + buffer_size,
            target_widget.height + buffer_size,
        )

        # Atur posisi outline untuk sedikit memperbesar posisi outline sekitar target_widget
        outline_x = target_widget.x - buffer_size / 1.89
        outline_y = target_widget.y - buffer_size / 1.8
        self.outline_widget.pos = (outline_x, outline_y)

        # Buat animasi untuk outline menuju ke posisi buah saat ini
        anim = Animation(pos=(outline_x, outline_y), duration=0.1, t="out_expo")
        anim.start(self.outline_widget)

        # Update visibilitas panah
        self.ids.arrow_left.opacity = 1 if self.current_index > 0 else 0
        self.ids.arrow_right.opacity = (
            1 if self.current_index < len(self.sayur_list) - 1 else 0
        )

    def update_question(self):
        # Update label, soal, dan jawaban sesuai buah saat ini
        current_sayur = self.sayur_list[self.current_index]
        self.ids.label_nama_sayur.text = (
            current_sayur.upper()
        )  # Update nama buah di label
        self.ids.soal_image.source = (
            f"Image/Sayur/Soal_{current_sayur}.png"  # Update soal image
        )

    def next_sayur(self):
        # Navigasi ke buah berikutnya
        if self.current_index < len(self.sayur_list) - 1:
            self.current_index += 1
            self.update_outline_position()
            self.update_question()
            self.play_backsound()

    def prev_sayur(self):
        # Navigasi ke buah sebelumnya
        if self.current_index > 0:
            self.current_index -= 1
            self.update_outline_position()
            self.update_question()
            self.play_backsound()

    def play_backsound(self):
        # Stop suara sebelumnya jika ada
        if self.sound:
            self.sound.stop()

        # Load dan mainkan suara sesuai buah saat ini
        current_sayur = self.sayur_list[self.current_index]
        sound_file = self.sound_files[current_sayur]
        self.sound = SoundLoader.load(sound_file)
        if self.sound:
            self.sound.play()

    def go_to_mengenalbs(self):
        # Navigate back to Mengenalbsscreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = "mengenalbs"


# Load the Alfabet.kv file manually
Builder.load_file("Mempelajari/Mengenalbs/Sayur.kv")

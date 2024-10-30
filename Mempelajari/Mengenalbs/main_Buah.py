from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.screenmanager import SlideTransition, FadeTransition, ScreenManager, Screen
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

class BuahScreen(Screen):
    buah_list = ["apel", "ceri", "durian", "mangga", "lemon", "pisang", "naga"]
    sound_files = {
        "apel": "Sounds/Apel.MP3",
        "ceri": "Sounds/Ceri.MP3",
        "durian": "Sounds/Durian.MP3",
        "mangga": "Sounds/Mangga.MP3",
        "lemon": "Sounds/Lemon.MP3",
        "pisang": "Sounds/Pisang.MP3",
        "naga": "Sounds/Naga.MP3",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_index = 0
        self.outline_widget = None
        self.sound = None

    def on_enter(self):
        # Reset ke tampilan awal (soal pertama) setiap kali masuk ke layar ini
        self.current_index = 0
        self.update_outline_position()
        self.update_question()
        self.play_backsound()

    def update_outline_position(self):
        if not self.outline_widget:
            self.outline_widget = self.ids.outline

        # Ambil widget jawaban sesuai dengan buah saat ini
        current_buah = self.buah_list[self.current_index]
        target_widget = self.ids[f"jawaban_{current_buah}"]

        # Set ukuran outline agar sama dengan target_widget (misalnya, gambar buah)
        self.outline_widget.size = target_widget.size

        # Set posisi outline agar tepat di sekitar target_widget
        self.outline_widget.pos = target_widget.pos

        # Buat animasi untuk outline menuju ke posisi buah saat ini
        anim = Animation(pos=target_widget.pos, duration=0.1, t='out_expo')
        anim.start(self.outline_widget)

        # Update visibilitas panah
        self.ids.arrow_left.opacity = 1 if self.current_index > 0 else 0
        self.ids.arrow_right.opacity = 1 if self.current_index < len(self.buah_list) - 1 else 0

    def update_question(self):
        # Update label, soal, dan jawaban sesuai buah saat ini
        current_buah = self.buah_list[self.current_index]
        self.ids.label_nama_buah.text = current_buah.upper()  # Update nama buah di label
        self.ids.soal_image.source = f"Image/Buah/Soal_{current_buah}.png"  # Update soal image

    def next_buah(self):
        # Navigasi ke buah berikutnya
        if self.current_index < len(self.buah_list) - 1:
            self.current_index += 1
            self.update_outline_position()
            self.update_question()
            self.play_backsound()

    def prev_buah(self):
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
        current_buah = self.buah_list[self.current_index]
        sound_file = self.sound_files[current_buah]
        self.sound = SoundLoader.load(sound_file)
        if self.sound:
            self.sound.play()

    def go_to_mengenalbs(self):
        # Fungsi untuk navigasi kembali dengan transisi slide
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = 'mengenalbs'

# Load the Alfabet.kv file manually
Builder.load_file('Mempelajari/Mengenalbs/Buah.kv')
from kivy.app import App
from kivy.uix.screenmanager import (
    SlideTransition,
    FadeTransition,
    ScreenManager,
    Screen,
)
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import re  # Untuk melakukan validasi menggunakan regular expression
from kivy.lang import Builder
import os
from Mempelajari.main_Alfabet import AlfabetScreen
from Mempelajari.main_Menyusunsk import MenyusunSKScreen
from Mempelajari.Mengenalbs.main_Buah import BuahScreen
from Mempelajari.Mengenalbs.main_Sayur import SayurScreen
from Permainan.main_Tebakwarna import TebakWarnaScreen
from Permainan.main_Cocokgambar import MencocokkanGambarScreen
from Permainan.main_Penjumlahan import PenjumlahanScreen
import pyrebase
from profil import ProfilScreen

# == Aplikasi Ayo Belajar ==
# Mengatur ukuran window (lebar, tinggi)
Window.size = (900, 500)
Window.clearcolor = (0.65, 0.65, 0.65, 0.7)

Builder.load_file("login.kv")
Builder.load_file("register.kv")
firebase_config = {
    "apiKey": "AIzaSyColUuRwpOiRmYWkp1i9VREVySdfOL955g",
    "authDomain": "profil-6c411.firebaseapp.com",
    "databaseURL": "https://profil-6c411-default-rtdb.firebaseio.com/",
    "projectId": "profil-6c411",
    "storageBucket": "profil-6c411.firebasestorage.app",
    "messagingSenderId": "644018498360",
    "appId": "1:644018498360:web:748c74657b7b74ae0a2fcd",
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()


class LoginScreen(Screen):
    def login_user(self):
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        try:
            # Melakukan proses login dengan Firebase
            user = auth.sign_in_with_email_and_password(email, password)
            self.user_id = user[
                "localId"
            ]  # Menyimpan user_id untuk digunakan di layar berikutnya

            # Mengambil data pengguna dari Firebase menggunakan user_id
            user_data = db.child("users").child(self.user_id).get().val()

            if user_data:
                # Meneruskan user_id ke ProfilScreen
                profil_screen = self.manager.get_screen("profil")
                profil_screen.user_id = self.user_id  # Kirim user_id ke ProfilScreen

                # Menyimpan nama pengguna di layar LayarScreen
                layar_screen = self.manager.get_screen("layar")
                layar_screen.ids.welcome_label.text = (
                    f"Hai, {user_data['name']}!\nYuk, mulai petualangan belajar kamu!"
                )

                # Transisi ke LayarScreen
                self.manager.transition = FadeTransition(duration=0.3)
                self.manager.current = "layar"
            else:
                self.show_error_popup("Data pengguna tidak ditemukan.")
        except Exception as e:
            print(f"Error during login: {e}")
            self.show_error_popup("Login Gagal! Periksa email dan password.")

    def show_error_popup(self, message):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_label = Label(text=message)
        close_button = Button(text="Tutup", size_hint=(None, None), size=(100, 40))
        layout.add_widget(popup_label)
        layout.add_widget(close_button)
        popup = Popup(
            title="Error", content=layout, size_hint=(None, None), size=(300, 200)
        )
        close_button.bind(on_press=popup.dismiss)
        popup.open()


class RegisterScreen(Screen):
    def register_user(self):
        email = self.ids.email_input.text
        password = self.ids.password_input.text
        name = self.ids.name_input.text

        if re.match(r"^[A-Za-z]", name):
            try:
                user = auth.create_user_with_email_and_password(email, password)
                db.child("users").child(user["localId"]).set(
                    {
                        "name": name,
                        "email": email,  # Hanya nama dan email yang disimpan saat registrasi
                    }
                )

                # Tampilkan popup setelah akun berhasil dibuat
                self.show_success_popup("Selamat akun berhasil dibuat!")

                # Pindah ke layar login setelah berhasil mendaftar
                self.manager.current = "login"
            except Exception as e:
                print(f"Error during registration: {e}")
                self.show_error_popup(
                    "Pendaftaran Gagal! Periksa kembali email atau password."
                )
        else:
            self.show_error_popup("Nama tidak valid!")

    def show_success_popup(self, message):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_label = Label(text=message)
        close_button = Button(text="Tutup", size_hint=(None, None), size=(100, 40))
        layout.add_widget(popup_label)
        layout.add_widget(close_button)
        popup = Popup(
            title="Berhasil", content=layout, size_hint=(None, None), size=(300, 200)
        )
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def show_error_popup(self, message):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_label = Label(text=message)
        close_button = Button(text="Tutup", size_hint=(None, None), size=(100, 40))
        layout.add_widget(popup_label)
        layout.add_widget(close_button)
        popup = Popup(
            title="Error", content=layout, size_hint=(None, None), size=(300, 200)
        )
        close_button.bind(on_press=popup.dismiss)
        popup.open()


class LayarScreen(Screen):
    def show_logout_popup(self):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_label = Label(text="Apakah Kamu Ingin Selesai?", font_size="15sp")

        button_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.3), spacing=50
        )
        yes_button = Button(text="Ya", size_hint=(None, None), size=(100, 40))
        no_button = Button(text="Tidak", size_hint=(None, None), size=(100, 40))

        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)

        layout.add_widget(popup_label)
        layout.add_widget(button_layout)

        popup = Popup(
            title="Konfirmasi Pesan",
            content=layout,
            size_hint=(None, None),
            size=(300, 200),
        )

        yes_button.bind(on_press=lambda *args: self.logout(popup))
        no_button.bind(on_press=popup.dismiss)

        popup.open()

    def logout(self, popup):
        popup.dismiss()
        # Mengosongkan inputan email dan password pada layar login
        login_screen = self.manager.get_screen("login")
        login_screen.ids.email_input.text = ""
        login_screen.ids.password_input.text = ""

        # Transisi ke layar login
        self.manager.transition = FadeTransition(duration=0.3)
        self.manager.current = "login"

    def on_touch_down(self, touch):
        # Cek jika ikon Exit diklik
        if self.ids.exit_icon.collide_point(*touch.pos):
            self.show_logout_popup()
            return True
        # Cek jika ikon Gear diklik
        elif self.ids.gear_icon.collide_point(*touch.pos):
            self.open_settings_widget()
            return True
        elif self.ids.profil_icon.collide_point(*touch.pos):
            self.go_to_profil()
            return True
        elif self.ids.mempelajari_image.collide_point(*touch.pos):
            self.go_to_mempelajari()
            return True
        elif self.ids.permainan_image.collide_point(*touch.pos):
            self.go_to_permainan()
            return True
        return super().on_touch_down(touch)

    def open_settings_widget(self):
        self.ids.settings_widget.opacity = 1  # Menampilkan widget pengaturan

    def close_settings_widget(self):
        self.ids.settings_widget.opacity = 0  # Menyembunyikan widget pengaturan

    def update_volume_label(self, slider_type, value):
        if slider_type == "music":
            self.ids.music_volume_label.text = f"{int(value)}%"
        elif slider_type == "speaker":
            self.ids.speaker_volume_label.text = f"{int(value)}%"

    def go_to_profil(self):
        # Arahkan ke ProfilScreen dengan transisi fade
        self.manager.transition = FadeTransition(duration=0.3)
        self.manager.current = "profil"

    def go_to_mempelajari(self):
        # Navigate to MempelajariScreen with a fade transition
        self.manager.transition = FadeTransition(duration=0.3)
        self.manager.current = "mempelajari"

    def go_to_permainan(self):
        # Navigate to PermainanScreen with a fade transition
        self.manager.transition = FadeTransition(duration=0.3)
        self.manager.current = "permainan"


class MempelajariScreen(Screen):
    def go_to_layar(self):
        # Navigate to LayarScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = "layar"

    def on_touch_down(self, touch):
        if self.ids.alfabet_image.collide_point(*touch.pos):
            self.go_to_alfabet()
            return True
        elif self.ids.mengenalbuahsayur_image.collide_point(*touch.pos):
            self.go_to_mengenalbs()
            return True
        elif self.ids.menyusunsukukata_image.collide_point(*touch.pos):
            self.go_to_menyusunsk()
            return True
        return super().on_touch_down(touch)

    def go_to_alfabet(self):
        # Navigate to AlfabetScreen with a fade transition
        self.manager.transition = FadeTransition(duration=0.2)
        self.manager.current = "alfabet"

    def go_to_mengenalbs(self):
        # Navigate to MengenalbsScreen with a fade transition
        self.manager.transition = FadeTransition(duration=0.2)
        self.manager.current = "mengenalbs"

    def go_to_menyusunsk(self):
        # Navigate to MenyusunSKScreen with a fade transition
        self.manager.transition = FadeTransition(duration=0.2)
        self.manager.current = "menyusunsk"


class MengenalBSScreen(Screen):
    def go_to_mempelajari(self):
        # Navigate back to MempelajariScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = "mempelajari"

    def on_touch_down(self, touch):
        if self.ids.buah_image.collide_point(*touch.pos):
            self.go_to_buah()
            return True
        elif self.ids.sayur_image.collide_point(*touch.pos):
            self.go_to_sayur()
            return True
        return super().on_touch_down(touch)

    def go_to_buah(self):
        # Navigate to BuahScreen with a fade transition
        self.manager.transition = FadeTransition(duration=0.2)
        self.manager.current = "buah"

    def go_to_sayur(self):
        # Navigate to SayurScreen with a fade transition
        self.manager.transition = FadeTransition(duration=0.2)
        self.manager.current = "sayur"


class PermainanScreen(Screen):  # Menambahkan PermainanScreen
    def go_to_layar(self):
        # Navigate to LayarScreen with a fade transition
        self.manager.transition = SlideTransition(direction="left", duration=0.2)
        self.manager.current = "layar"

    def on_touch_down(self, touch):
        if self.ids.tebakwarna_image.collide_point(*touch.pos):
            self.go_to_tebakwarna()
            return True
        elif self.ids.mencocokkangambar_image.collide_point(*touch.pos):
            self.go_to_mencocokkangambar()
            return True
        elif self.ids.penjumlahan_image.collide_point(*touch.pos):
            self.go_to_penjumlahan()
            return True
        return super().on_touch_down(touch)

    def go_to_tebakwarna(self):
        # Navigate to TebakWarnaScreen with a fade transition
        self.manager.transition = FadeTransition(duration=0.2)
        self.manager.current = "tebakwarna"

    def go_to_mencocokkangambar(self):
        # Navigate to MencocokkanGambarScreen with a fade transition
        self.manager.transition = FadeTransition(duration=0.2)
        self.manager.current = "mencocokkangambar"

    def go_to_penjumlahan(self):
        # Navigate to PenjumlahanScreen with a fade transition
        self.manager.transition = FadeTransition(duration=0.2)
        self.manager.current = "penjumlahan"


class AyoBelajarApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(BuahScreen(name="buah"))

        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(ProfilScreen(name="profil"))

        sm.add_widget(LayarScreen(name="layar"))
        sm.add_widget(MempelajariScreen(name="mempelajari"))
        sm.add_widget(PermainanScreen(name="permainan"))
        sm.add_widget(AlfabetScreen(name="alfabet"))
        sm.add_widget(MengenalBSScreen(name="mengenalbs"))
        sm.add_widget(SayurScreen(name="sayur"))
        sm.add_widget(MenyusunSKScreen(name="menyusunsk"))
        sm.add_widget(TebakWarnaScreen(name="tebakwarna"))
        sm.add_widget(MencocokkanGambarScreen(name="mencocokkangambar"))
        sm.add_widget(PenjumlahanScreen(name="penjumlahan"))

        return sm


if __name__ == "__main__":
    AyoBelajarApp().run()

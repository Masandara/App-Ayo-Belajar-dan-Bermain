from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
import pyrebase
from kivy.lang import Builder

Builder.load_file("profile.kv")
# Menginisialisasi Firebase Admin SDK dengan kredensial JSON Anda
import pyrebase

# Konfigurasi Firebase
firebaseConfig = {
    "apiKey": "AIzaSyColUuRwpOiRmYWkp1i9VREVySdfOL955g",
    "authDomain": "profil-6c411.firebaseapp.com",
    "databaseURL": "https://profil-6c411-default-rtdb.firebaseio.com/",
    "projectId": "profil-6c411",
    "storageBucket": "profil-6c411.firebasestorage.app",
    "messagingSenderId": "644018498360",
    "appId": "1:644018498360:web:748c74657b7b74ae0a2fcd",
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


class ProfilScreen(Screen):
    def on_pre_enter(self):
        # Ambil user_id dari login screen
        try:
            # Mendapatkan data pengguna dari Firebase
            user_data = db.child("users").child(self.user_id).get().val()
            if user_data:
                # Menampilkan info pengguna
                self.ids.email_label.text = f"Email: {user_data['email']}"
                self.ids.name_label.text = f"Nama: {user_data['name']}"

                # Cek jika umur dan hobi sudah diatur, jika belum tampilkan tombol Tambah
                if "age" in user_data:
                    self.ids.age_button.text = "Edit Umur"
                    self.ids.age_label.text = f"Umur: {user_data['age']}"
                else:
                    self.ids.age_button.text = "Tambahkan Umur"
                    self.ids.age_label.text = "Umur: -"

                if "hobby" in user_data:
                    self.ids.hobby_button.text = "Edit Hobi"
                    self.ids.hobby_label.text = f"Hobi: {user_data['hobby']}"
                else:
                    self.ids.hobby_button.text = "Tambahkan Hobi"
                    self.ids.hobby_label.text = "Hobi: -"
            else:
                print("Data pengguna tidak ditemukan.")
        except Exception as e:
            print(f"Error fetching user data: {e}")

    def add_or_edit_age(self):
        self.show_input_popup("Ubah Umur", "Masukkan umur baru:", "age")

    def add_or_edit_hobby(self):
        self.show_input_popup("Ubah Hobi", "Masukkan hobi baru:", "hobby")

    def edit_name(self):
        self.show_input_popup("Ubah Nama", "Masukkan nama baru:", "name")

    def edit_password(self):
        self.show_input_popup(
            "Ubah Password", "Masukkan password baru:", "password", is_password=True
        )

    def show_input_popup(self, title, message, field, is_password=False):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        label = Label(text=message)
        input_field = TextInput(password=is_password, multiline=False)
        save_button = Button(text="Simpan", size_hint=(None, None), size=(100, 40))
        layout.add_widget(label)
        layout.add_widget(input_field)
        layout.add_widget(save_button)

        popup = Popup(
            title=title, content=layout, size_hint=(None, None), size=(300, 200)
        )
        save_button.bind(
            on_press=lambda instance: self.save_user_data(
                field, input_field.text, popup
            )
        )
        popup.open()

    def save_user_data(self, field, value, popup):
        if value:
            try:
                # Perbarui data di Firebase
                db.child("users").child(self.user_id).update({field: value})
                popup.dismiss()

                # Refresh tampilan profil setelah penyimpanan
                self.on_pre_enter()
            except Exception as e:
                print(f"Error saving {field}: {e}")
        else:
            print("Nilai tidak valid.")

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
        try:
            user_data = db.child("users").child(self.user_id).get().val()
            if user_data:
                self.ids.email_label.text = f"Email: {user_data['email']}"
                self.ids.name_label.text = f"Nama: {user_data['name']}"

                # Atur umur
                if "age" in user_data:
                    self.ids.age_button.text = "Edit Umur"
                    self.ids.age_label.text = f"Umur: {user_data['age']}"
                    self.ids.delete_age_button.opacity = 1
                    self.ids.delete_age_button.disabled = False
                else:
                    self.ids.age_button.text = "Tambahkan Umur"
                    self.ids.age_label.text = "Umur: -"
                    self.ids.delete_age_button.opacity = 0
                    self.ids.delete_age_button.disabled = True

                # Atur hobi
                if "hobby" in user_data:
                    self.ids.hobby_button.text = "Edit Hobi"
                    self.ids.hobby_label.text = f"Hobi: {user_data['hobby']}"
                    self.ids.delete_hobby_button.opacity = 1
                    self.ids.delete_hobby_button.disabled = False
                else:
                    self.ids.hobby_button.text = "Tambahkan Hobi"
                    self.ids.hobby_label.text = "Hobi: -"
                    self.ids.delete_hobby_button.opacity = 0
                    self.ids.delete_hobby_button.disabled = True
            else:
                print("Data pengguna tidak ditemukan.")
        except Exception as e:
            print(f"Error fetching user data: {e}")

    def add_or_edit_age(self):
        self.show_input_popup("Ubah Umur", "Masukkan umur baru", "age")

    def add_or_edit_hobby(self):
        self.show_input_popup("Ubah Hobi", "Masukkan hobi baru", "hobby")

    def edit_name(self):
        self.show_input_popup("Ubah Nama", "Masukkan nama baru", "name")

    def edit_password(self):
        self.show_input_popup(
            "Ubah Password", "Masukkan password baru", "password", is_password=True
        )

    def delete_age(self):
        self.show_delete_confirmation("age", "Apakah Anda yakin ingin menghapus umur?")

    def delete_hobby(self):
        self.show_delete_confirmation(
            "hobby", "Apakah Anda yakin ingin menghapus hobi?"
        )

    def show_delete_confirmation(self, field, message):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        label = Label(text=message)
        button_yes = Button(text="Iya", size_hint=(None, None), size=(100, 40))
        button_no = Button(text="Tidak", size_hint=(None, None), size=(100, 40))

        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        button_layout.add_widget(button_yes)
        button_layout.add_widget(button_no)

        layout.add_widget(label)
        layout.add_widget(button_layout)

        popup = Popup(
            title="Konfirmasi Hapus",
            content=layout,
            size_hint=(None, None),
            size=(300, 200),
        )

        button_yes.bind(on_press=lambda instance: self.confirm_delete(field, popup))
        button_no.bind(on_press=popup.dismiss)

        popup.open()

    def confirm_delete(self, field, popup):
        try:
            # Menghapus data di Firebase
            db.child("users").child(self.user_id).child(field).remove()
            popup.dismiss()
            # Refresh tampilan profil setelah penghapusan
            self.on_pre_enter()
            print(f"{field} berhasil dihapus.")
        except Exception as e:
            print(f"Error deleting {field}: {e}")

    def show_input_popup(self, title, message, field, is_password=False):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        label = Label(text=message)
        input_field = TextInput(password=is_password, multiline=False)
        save_button = Button(text="Simpan", size_hint=(None, None), size=(100, 40))
        layout.add_widget(label)
        layout.add_widget(input_field)
        layout.add_widget(save_button)

        popup = Popup(
            title=title, content=layout, size_hint=(None, None), size=(350, 250)
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

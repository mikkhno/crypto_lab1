import os
import tkinter as tk
from tkinter import filedialog, messagebox


# --- Caesar Cipher Class ---
class CaesarCipher:
    def __init__(self):
        self.uk_alphabet = "абвгґдежзийіклмнопрстуфхцчшщьюя"
        self.en_alphabet = "abcdefghijklmnopqrstuvwxyz"

    # Валідація ключа
    def validate_key(self, key):
        if not isinstance(key, int):
            raise ValueError("Key must be an integer.")

    def shift_alphabet(self, alphabet, key):
        return alphabet[key:] + alphabet[:key]

    def encrypt(self, text, key, language="en"):
        self.validate_key(key)
        alphabet = self.en_alphabet if language == "en" else self.uk_alphabet
        shifted_alphabet = self.shift_alphabet(alphabet, key)
        table = str.maketrans(alphabet + alphabet.upper(),
                              shifted_alphabet + shifted_alphabet.upper())
        return text.translate(table)

    def decrypt(self, text, key, language="en"):
        return self.encrypt(text, -key, language)


# --- File Manager Class ---
class FileManager:
    @staticmethod
    def read_file(filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} does not exist.")
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def save_file(filename, content):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)


# --- GUI Application ---
class CipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Caesar Cipher Application")

        self.cipher = CaesarCipher()
        self.file_manager = FileManager()

        self.text = tk.StringVar()
        self.key = tk.IntVar()
        self.language = tk.StringVar(value="en")

        # --- GUI Components ---
        self.create_widgets()

    def create_widgets(self):
        # Text Input
        tk.Label(self.root, text="Enter Text:").pack(pady=5)
        self.text_entry = tk.Entry(self.root, textvariable=self.text, width=50)
        self.text_entry.pack(pady=5)

        # Key Input
        tk.Label(self.root, text="Enter Key:").pack(pady=5)
        self.key_entry = tk.Entry(self.root, textvariable=self.key, width=10)
        self.key_entry.pack(pady=5)

        # Language Selection
        tk.Label(self.root, text="Select Language:").pack(pady=5)
        tk.Radiobutton(self.root, text="English", variable=self.language, value="en").pack()
        tk.Radiobutton(self.root, text="Ukrainian", variable=self.language, value="uk").pack()

        # Buttons
        tk.Button(self.root, text="Encrypt", command=self.encrypt_text).pack(pady=5)
        tk.Button(self.root, text="Decrypt", command=self.decrypt_text).pack(pady=5)
        tk.Button(self.root, text="Open File", command=self.open_file).pack(pady=5)
        tk.Button(self.root, text="Save File", command=self.save_file).pack(pady=5)
        tk.Button(self.root, text="About", command=self.show_about).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)

    def encrypt_text(self):
        try:
            key = self.key.get()
            text = self.text.get()
            language = self.language.get()
            result = self.cipher.encrypt(text, key, language)
            self.text.set(result)
            messagebox.showinfo("Success", "Text encrypted successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def decrypt_text(self):
        try:
            key = self.key.get()
            text = self.text.get()
            language = self.language.get()
            result = self.cipher.decrypt(text, key, language)
            self.text.set(result)
            messagebox.showinfo("Success", "Text decrypted successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                content = self.file_manager.read_file(file_path)
                self.text.set(content)
                messagebox.showinfo("Success", "File opened successfully!")
            except FileNotFoundError as e:
                messagebox.showerror("Error", str(e))

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            content = self.text.get()
            self.file_manager.save_file(file_path, content)
            messagebox.showinfo("Success", "File saved successfully!")

    def show_about(self):
        messagebox.showinfo("About", "Caesar Cipher Application\nDeveloper: Dmytro Mikhno TV-12, v1.0")


# --- Main Loop ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CipherApp(root)
    root.mainloop()

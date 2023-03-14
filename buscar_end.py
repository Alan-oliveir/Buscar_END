import tkinter as tk
import customtkinter as ctk

from PIL import Image, ImageTk

import os

import requests

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

PATH = os.path.dirname(os.path.realpath(__file__))

class App(ctk.CTk):

    APP_NAME = "Buscar Endereço"
    WIDTH = 500
    HEIGHT = 650

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.minsize(App.WIDTH, App.HEIGHT)
        self.maxsize(App.WIDTH, App.HEIGHT)
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # load image with PIL and convert to PhotoImage
        image = Image.open(PATH + "/test_images/bg_gradient.jpg").resize((self.WIDTH, self.HEIGHT))
        self.bg_image = ImageTk.PhotoImage(image)

        self.image_label = tk.Label(master=self, image=self.bg_image)
        self.image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.frame = ctk.CTkFrame(master=self, width=300, height=App.HEIGHT, corner_radius=0)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.label = ctk.CTkLabel(master=self.frame, width=200, height=60, corner_radius=6, fg_color=("gray70", "gray25"), text="BUSCA DE ENDEREÇO")
        self.label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.entry_cep = ctk.CTkEntry(master=self.frame, corner_radius=6, width=200, placeholder_text="CEP")
        self.entry_cep.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

        self.button_submit = ctk.CTkButton(master=self.frame, text="Enviar", corner_radius=6, command=self.button_event_submit, width=200)
        self.button_submit.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

        self.button_clean = ctk.CTkButton(master=self.frame, text="Clean", corner_radius=6, command=self.button_event_clean, width=200)
        self.button_clean.place(relx=0.5, rely=0.42, anchor=tk.CENTER)

        self.textbox = ctk.CTkTextbox(master=self.frame, width=250, height=260, corner_radius=6)
        self.textbox.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def button_event_submit(self):
                     
        text = self.entry_cep.get()

        text = text.replace("-", "").replace(".", "").replace(" ", "")
    
        link = requests.get(f'https://viacep.com.br/ws/{text}/json/')

        # Verifica erro na requisição do CEP
        if link.status_code != 200:
            self.message_window = ctk.CTkToplevel(self)
            self.message_window.title('Erro de Requisição')
            self.message_window.after(10000, self.message_window.destroy)

            # create label on CTkToplevel window
            label = ctk.CTkLabel(self.message_window, text=f"Ocorreu um erro na requisição do CEP: {text}.\nVerifique o CEP e tente novamente.")
            label.pack(side="top", fill="both", expand=True, padx=40, pady=40)

        # Retorna o endereço do CEP em formato json/chaves/dicionário.
        dic_endereco = link.json()

        uf = dic_endereco['uf']
        cidade = dic_endereco['localidade']
        bairro = dic_endereco['bairro']
        logradouro = dic_endereco['logradouro']

        # Exibe o endereço na caixa de texto
        self.textbox.insert("0.0", f" UF: {uf}\n Cidade: {cidade}\n Bairro: {bairro}\n Logradouro: {logradouro}")   

    def button_event_clean(self):

        self.entry_cep.delete(0, 'end')
        self.textbox.delete("0.0", 'end')

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
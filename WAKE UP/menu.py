import customtkinter as ctk
import subprocess
import os
import sys
import opcoes
import math

def abrir_wake_up():

    script_path = os.path.join(os.path.dirname(__file__), "wake_up_main.py")

    try:
        subprocess.Popen([sys.executable, script_path])
        app.destroy()

    except Exception as e:
        print(f"Erro ao abrir o sistema: {e}")

def abrir_opcoes():

    try:
        opcoes.abrir_opcoes(main_view, mostrar_menu)

    except Exception as e:
        print(f"Erro ao abrir opções: {e}")

def mostrar_menu():

    for widget in main_view.winfo_children():
        widget.destroy()

    # CONTAINER CENTRAL
    center = ctk.CTkFrame(main_view, fg_color="transparent")
    center.place(relx=0.5, rely=0.5, anchor="center")

    # TITULO
    label = ctk.CTkLabel(
        center,
        text="WAKE UP",
        font=("Inter", 42, "bold"),
        text_color="#FFFFFF"
    )

    label.pack(pady=(0,10))

    # SUBTITULO
    sub = ctk.CTkLabel(
        center,
        text="Controle sua produtividade",
        font=("Inter", 16),
        text_color="#9ca3af"
    )

    sub.pack(pady=(0,40))

    # BOTÃO INICIAR
    btn_ligar = ctk.CTkButton(
        center,
        text="INICIAR",
        command=abrir_wake_up,
        fg_color="transparent",
        hover_color="#064e3b",
        border_width=3,
        border_color="#10b981",
        corner_radius=12,
        text_color="#10b981",
        height=50,
        width=280,
        font=("Segoe UI", 16, "bold")
    )

    btn_ligar.pack(pady=8)

    # BOTÃO OPÇÕES
    btn_opcoes = ctk.CTkButton(
        center,
        text="OPÇÕES",
        command=abrir_opcoes,
        fg_color="transparent",
        hover_color="#1e3a8a",
        border_width=3,
        border_color="#60a5fa",
        corner_radius=12,
        text_color="#60a5fa",
        height=50,
        width=280,
        font=("Segoe UI", 16, "bold")
    )

    btn_opcoes.pack(pady=8)

    # BOTÃO SAIR
    btn_sair = ctk.CTkButton(
        center,
        text="SAIR",
        command=app.quit,
        fg_color="transparent",
        hover_color="#7f1d1d",
        border_width=3,
        border_color="#f87171",
        corner_radius=12,
        text_color="#f87171",
        height=50,
        width=280,
        font=("Segoe UI", 16, "bold")
    )

    btn_sair.pack(pady=8)

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Controle WAKE UP")

# FADE
app.attributes("-alpha", 0)

def fade_in():
    alpha = app.attributes("-alpha")
    if alpha < 1:
        app.attributes("-alpha", alpha + 0.04)
        app.after(15, fade_in)

fade_in()

# MAXIMIZAR SEM COBRIR A BARRA DE TAREFAS
app.update_idletasks()
app.after(50, lambda: app.state("zoomed"))

# FUNDO
bg_view = ctk.CTkFrame(app, fg_color="#2b2b2b")
bg_view.place(x=0, y=0, relwidth=1, relheight=1)

main_view = ctk.CTkFrame(app, fg_color="transparent")
main_view.place(x=0, y=0, relwidth=1, relheight=1)

t = 0

def animar_fundo():
    global t
    intensidade = int(40 + 10 * math.sin(t))
    cor = f"#{intensidade:02x}{intensidade:02x}{intensidade:02x}"
    bg_view.configure(fg_color=cor)
    t += 0.05
    app.after(30, animar_fundo)
animar_fundo()

app.bind("<Return>", lambda e: abrir_wake_up())
app.bind("<Escape>", lambda e: app.quit())

mostrar_menu()
app.mainloop()
import customtkinter as ctk
import subprocess
import os
import sys
import json
import opcoes
import math

CONFIG_FILE = "config.json"

BG = "#18181b"
PANEL = "#212124"
CARD_BORDER = "#2c2c30"
TEXT = "#f4f4f5"
TEXT_MUTED = "#9ca3af"
TEXT_FAINT = "#6b7280"

GREEN = "#10b981"
GREEN_HOVER = "#064e3b"
BLUE = "#60a5fa"
BLUE_HOVER = "#1e3a8a"
RED = "#f87171"
RED_HOVER = "#7f1d1d"


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


def video_atual():

    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                caminho = config.get("video", "")
                if caminho:
                    return os.path.splitext(os.path.basename(caminho))[0]
    except Exception:
        pass

    return None


def mostrar_menu():

    for widget in main_view.winfo_children():
        widget.destroy()

    # PAINEL CENTRAL (card com leve profundidade)
    card = ctk.CTkFrame(
        main_view,
        fg_color=PANEL,
        corner_radius=24,
        border_width=1,
        border_color=CARD_BORDER,
    )
    card.place(relx=0.5, rely=0.5, anchor="center")

    center = ctk.CTkFrame(card, fg_color="transparent")
    center.pack(padx=70, pady=50)

    # SELO
    selo = ctk.CTkLabel(
        center,
        text="👁  ANTI-PROCRASTINAÇÃO",
        font=("Segoe UI", 12, "bold"),
        text_color=GREEN,
    )
    selo.pack(pady=(0, 12))

    # TITULO
    label = ctk.CTkLabel(
        center,
        text="WAKE UP",
        font=("Segoe UI", 46, "bold"),
        text_color=TEXT,
    )
    label.pack()

    # SUBTITULO
    sub = ctk.CTkLabel(
        center,
        text="Controle sua produtividade — olhar para o lado não é uma opção",
        font=("Segoe UI", 14),
        text_color=TEXT_MUTED,
    )
    sub.pack(pady=(6, 0))

    # BADGE COM O VIDEO CONFIGURADO
    nome_video = video_atual()

    badge = ctk.CTkFrame(
        center,
        fg_color="#1b1b1e",
        corner_radius=999,
        border_width=1,
        border_color=CARD_BORDER,
    )
    badge.pack(pady=(18, 34))

    ctk.CTkLabel(
        badge,
        text=(f"🎬  {nome_video}" if nome_video else "⚠  Nenhum vídeo configurado"),
        font=("Segoe UI", 12),
        text_color=TEXT_MUTED if nome_video else "#fbbf24",
    ).pack(padx=18, pady=8)

    def botao(texto, comando, cor, cor_hover):
        return ctk.CTkButton(
            center,
            text=texto,
            command=comando,
            fg_color="transparent",
            hover_color=cor_hover,
            border_width=2,
            border_color=cor,
            corner_radius=12,
            text_color=cor,
            height=52,
            width=300,
            font=("Segoe UI", 15, "bold"),
        )

    botao("▶   INICIAR", abrir_wake_up, GREEN, GREEN_HOVER).pack(pady=6)
    botao("⚙   OPÇÕES", abrir_opcoes, BLUE, BLUE_HOVER).pack(pady=6)
    botao("✕   SAIR", app.quit, RED, RED_HOVER).pack(pady=6)

    ctk.CTkLabel(
        center,
        text="Enter para iniciar  •  Esc para sair",
        font=("Segoe UI", 11),
        text_color=TEXT_FAINT,
    ).pack(pady=(26, 0))


ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("WAKE UP — Controle de Produtividade")

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
bg_view = ctk.CTkFrame(app, fg_color=BG)
bg_view.place(x=0, y=0, relwidth=1, relheight=1)

main_view = ctk.CTkFrame(app, fg_color="transparent")
main_view.place(x=0, y=0, relwidth=1, relheight=1)

t = 0


def animar_fundo():
    global t
    intensidade = int(24 + 6 * math.sin(t))
    cor = f"#{intensidade:02x}{intensidade:02x}{intensidade + 2:02x}"
    bg_view.configure(fg_color=cor)
    t += 0.05
    app.after(30, animar_fundo)


animar_fundo()

app.bind("<Return>", lambda e: abrir_wake_up())
app.bind("<Escape>", lambda e: app.quit())

mostrar_menu()
app.mainloop()

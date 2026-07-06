import customtkinter as ctk
from tkinter import filedialog
import os
import requests
import threading
import json

AUDIO_PATH = ""

TEXT = "#FFFFFF"
TEXT_MUTED = "#9ca3af"

GREEN = "#10b981"
BLUE = "#60a5fa"
RED = "#f87171"

SIDEBAR = "#1f1f1f"
CONTENT_BG = "#2b2b2b"

VIDEO_FOLDER = "videos"
VIDEO_PATH = ""

CONFIG_FILE = "config.json"

os.makedirs(VIDEO_FOLDER, exist_ok=True)


def salvar_config(video, audio):

    config = {
        "video": video,
        "audio": audio
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def escolher_video_pc(label):

    global VIDEO_PATH, AUDIO_PATH

    caminho = filedialog.askopenfilename(
        title="Selecionar arquivo",
        filetypes=[
            ("Arquivos de mídia", "*.mp4 *.mov *.avi *.mkv *.mp3"),
            ("Vídeo", "*.mp4 *.mov *.avi *.mkv"),
            ("Áudio", "*.mp3"),
            ("Todos arquivos", "*.*")
        ]
    )

    if caminho:

        ext = os.path.splitext(caminho)[1].lower()

        if ext == ".mp3":
            AUDIO_PATH = caminho
            label.configure(text=f"Áudio: {os.path.basename(caminho)}")

        else:
            VIDEO_PATH = caminho
            label.configure(text=f"Vídeo: {os.path.basename(caminho)}")

        if VIDEO_PATH and AUDIO_PATH:
            salvar_config(VIDEO_PATH, AUDIO_PATH)


def popup_download(parent, url):

    popup = ctk.CTkToplevel(parent)
    popup.title("Download")
    popup.geometry("420x180")
    popup.resizable(False, False)
    popup.grab_set()

    titulo = ctk.CTkLabel(
        popup,
        text="Baixando vídeo",
        font=("Inter", 22, "bold"),
        text_color=TEXT
    )
    titulo.pack(pady=(20, 5))

    status = ctk.CTkLabel(
        popup,
        text="Preparando download...",
        text_color=TEXT_MUTED
    )
    status.pack(pady=5)

    progress = ctk.CTkProgressBar(popup, width=320)
    progress.pack(pady=15)
    progress.set(0)

    def download():

        try:

            progress.set(0.3)
            status.configure(text="Enviando link...")

            r = requests.post(
                "http://127.0.0.1:5000/download",
                json={"url": url}
            )

            progress.set(0.7)
            status.configure(text="Processando vídeo...")

            data = r.json()

            progress.set(1)

            status.configure(
                text=f"Download concluído: {data['title']}",
                text_color=GREEN
            )

        except Exception as e:
            status.configure(text=str(e), text_color=RED)

    threading.Thread(target=download).start()


def baixar_video(parent, entry):

    url = entry.get()

    if not url:
        return

    popup_download(parent, url)


def abrir_opcoes(main_view, voltar_menu):

    global VIDEO_PATH

    for widget in main_view.winfo_children():
        widget.destroy()

    container = ctk.CTkFrame(main_view, fg_color=CONTENT_BG)
    container.pack(fill="both", expand=True)

    sidebar = ctk.CTkFrame(container, width=240, fg_color=SIDEBAR, corner_radius=0)
    sidebar.pack(side="left", fill="y")

    content = ctk.CTkFrame(container, fg_color="transparent")
    content.pack(side="right", fill="both", expand=True)

    def limpar():
        for w in content.winfo_children():
            w.destroy()

    def titulo(texto):
        ctk.CTkLabel(
            content,
            text=texto,
            font=("Inter", 36, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=80, pady=(25, 5))

    def subtitulo(texto):
        ctk.CTkLabel(
            content,
            text=texto,
            font=("Inter", 16),
            text_color=TEXT_MUTED
        ).pack(anchor="w", padx=80, pady=(0, 15))

    # DOWNLOAD INTERNET

    def tela_download():

        limpar()

        titulo("Download da internet")
        subtitulo("Baixar vídeos usando o servidor")

        entry = ctk.CTkEntry(
            content,
            width=420,
            height=42,
            placeholder_text="Cole o link do vídeo..."
        )
        entry.pack(anchor="w", padx=80, pady=5)

        ctk.CTkButton(
            content,
            text="⬇ Baixar vídeo",
            width=220,
            height=44,
            fg_color="transparent",
            border_width=2,
            border_color=GREEN,
            text_color=GREEN,
            hover_color="#064e3b",
            corner_radius=12,
            font=("Segoe UI", 14, "bold"),
            command=lambda: baixar_video(content, entry)
        ).pack(anchor="w", padx=80, pady=8)

    # ARQUIVO DO PC

    def tela_pc():

        limpar()

        titulo("Selecionar do computador")
        subtitulo("Escolher um vídeo direto do seu PC")

        label = ctk.CTkLabel(
            content,
            text="Nenhum vídeo selecionado",
            text_color=TEXT_MUTED
        )
        label.pack(anchor="w", padx=80, pady=5)

        ctk.CTkButton(
            content,
            text="📁 Escolher arquivo",
            width=220,
            height=44,
            fg_color="transparent",
            border_width=2,
            border_color=BLUE,
            text_color=BLUE,
            hover_color="#1e3a8a",
            corner_radius=12,
            font=("Segoe UI", 14, "bold"),
            command=lambda: escolher_video_pc(label)
        ).pack(anchor="w", padx=80, pady=8)

    # GERENCIAR VIDEOS

    def tela_gerenciar():

        limpar()

        titulo("Vídeos disponíveis")
        subtitulo("Escolha qual vídeo o WAKE UP vai usar")

        video_dir = "server/downloads/video"
        audio_dir = "server/downloads/audio"

        os.makedirs(video_dir, exist_ok=True)
        os.makedirs(audio_dir, exist_ok=True)

        videos = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
        audios = [f for f in os.listdir(audio_dir) if f.endswith(".mp3")]

        base_videos = {os.path.splitext(v)[0]: v for v in videos}
        base_audios = {os.path.splitext(a)[0]: a for a in audios}

        arquivos_validos = set(base_videos.keys()) & set(base_audios.keys())

        if not arquivos_validos:

            ctk.CTkLabel(
                content,
                text="Nenhum vídeo com áudio encontrado",
                text_color=TEXT_MUTED
            ).pack(anchor="w", padx=80, pady=10)

            return

        for nome in arquivos_validos:

            video_path = os.path.join(video_dir, base_videos[nome])
            audio_path = os.path.join(audio_dir, base_audios[nome])

            frame = ctk.CTkFrame(content, fg_color="transparent")
            frame.pack(anchor="w", padx=80, pady=5)

            ctk.CTkLabel(
                frame,
                text=base_videos[nome],
                width=300,
                anchor="w"
            ).pack(side="left")

            def selecionar(v=video_path, a=audio_path):

                salvar_config(v, a)

            ctk.CTkButton(
                frame,
                text="Usar",
                width=80,
                height=30,
                fg_color=GREEN,
                hover_color="#047857",
                command=selecionar
            ).pack(side="left", padx=10)

    # SIDEBAR

    ctk.CTkLabel(
        sidebar,
        text="WAKE UP",
        font=("Inter", 24, "bold"),
        text_color=TEXT
    ).pack(pady=(35, 5))

    ctk.CTkLabel(
        sidebar,
        text="Configurações",
        font=("Inter", 13),
        text_color=TEXT_MUTED
    ).pack(pady=(0, 20))

    def botao_sidebar(texto, comando):

        return ctk.CTkButton(
            sidebar,
            text=texto,
            height=42,
            fg_color="transparent",
            hover_color="#2b2b2b",
            text_color=TEXT,
            anchor="w",
            corner_radius=8,
            font=("Segoe UI", 14),
            command=comando
        )

    botao_sidebar("🌐 Download internet", tela_download).pack(fill="x", padx=20, pady=4)
    botao_sidebar("💻 Arquivo do PC", tela_pc).pack(fill="x", padx=20, pady=4)
    botao_sidebar("🎬 Gerenciar vídeos", tela_gerenciar).pack(fill="x", padx=20, pady=4)

    ctk.CTkButton(
        sidebar,
        text="← Voltar",
        height=44,
        fg_color="transparent",
        border_width=2,
        border_color=RED,
        text_color=RED,
        hover_color="#7f1d1d",
        font=("Segoe UI", 14, "bold"),
        corner_radius=12,
        command=voltar_menu
    ).pack(side="bottom", padx=20, pady=30, fill="x")

    tela_download()
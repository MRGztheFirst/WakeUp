import customtkinter as ctk
from tkinter import filedialog
import os
import requests
import threading
import json

AUDIO_PATH = ""

TEXT = "#f4f4f5"
TEXT_MUTED = "#9ca3af"
TEXT_FAINT = "#6b7280"

GREEN = "#10b981"
GREEN_HOVER = "#064e3b"
BLUE = "#60a5fa"
BLUE_HOVER = "#1e3a8a"
RED = "#f87171"
RED_HOVER = "#7f1d1d"

SIDEBAR = "#141416"
CONTENT_BG = "#18181b"
CARD_BG = "#212124"
CARD_BORDER = "#2c2c30"
SIDEBAR_ACTIVE = "#242427"

VIDEO_PATH = ""

CONFIG_FILE = "config.json"


def carregar_config():

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    return {}


def salvar_config(video, audio):

    config = {
        "video": video,
        "audio": audio
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def escolher_video_pc(label_video, label_audio):

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
            label_audio.configure(text=f"🎵  {os.path.basename(caminho)}", text_color=TEXT)

        else:
            VIDEO_PATH = caminho
            label_video.configure(text=f"🎬  {os.path.basename(caminho)}", text_color=TEXT)

        if VIDEO_PATH and AUDIO_PATH:
            salvar_config(VIDEO_PATH, AUDIO_PATH)


def popup_download(parent, url, on_finish=None):

    popup = ctk.CTkToplevel(parent)
    popup.title("Download")
    popup.geometry("440x200")
    popup.resizable(False, False)
    popup.configure(fg_color=CARD_BG)
    popup.grab_set()

    titulo = ctk.CTkLabel(
        popup,
        text="⬇  Baixando vídeo",
        font=("Segoe UI", 20, "bold"),
        text_color=TEXT
    )
    titulo.pack(pady=(24, 6))

    status = ctk.CTkLabel(
        popup,
        text="Preparando download...",
        text_color=TEXT_MUTED,
        wraplength=380
    )
    status.pack(pady=5)

    progress = ctk.CTkProgressBar(popup, width=340, progress_color=GREEN)
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

            if "error" in data:
                raise Exception(data["error"])

            progress.set(1)

            status.configure(
                text=f"✔  Download concluído: {data['title']}",
                text_color=GREEN
            )

        except Exception as e:
            status.configure(text=f"✕  {e}", text_color=RED)

        finally:
            if on_finish:
                popup.after(0, on_finish)

    threading.Thread(target=download, daemon=True).start()


def baixar_video(parent, entry, botao):

    url = entry.get()

    if not url:
        return

    botao.configure(state="disabled", text="⬇  Baixando...")

    def restaurar():
        botao.configure(state="normal", text="⬇  Baixar vídeo")

    popup_download(parent, url, on_finish=restaurar)


def abrir_opcoes(main_view, voltar_menu):

    for widget in main_view.winfo_children():
        widget.destroy()

    container = ctk.CTkFrame(main_view, fg_color=CONTENT_BG)
    container.pack(fill="both", expand=True)

    sidebar = ctk.CTkFrame(container, width=240, fg_color=SIDEBAR, corner_radius=0)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    content = ctk.CTkFrame(container, fg_color="transparent")
    content.pack(side="right", fill="both", expand=True)

    botoes_sidebar = {}

    def marcar_ativo(chave):
        for k, b in botoes_sidebar.items():
            b.configure(fg_color=SIDEBAR_ACTIVE if k == chave else "transparent")

    def limpar():
        for w in content.winfo_children():
            w.destroy()

    def titulo(texto):
        ctk.CTkLabel(
            content,
            text=texto,
            font=("Segoe UI", 32, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=70, pady=(35, 4))

    def subtitulo(texto):
        ctk.CTkLabel(
            content,
            text=texto,
            font=("Segoe UI", 14),
            text_color=TEXT_MUTED
        ).pack(anchor="w", padx=70, pady=(0, 22))

    def cartao():
        card = ctk.CTkFrame(
            content,
            fg_color=CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=CARD_BORDER,
        )
        card.pack(anchor="w", padx=70, fill="x")
        return card

    # DOWNLOAD INTERNET

    def tela_download():

        limpar()
        marcar_ativo("download")

        titulo("Download da internet")
        subtitulo("Baixar vídeos usando o servidor local")

        card = cartao()

        interno = ctk.CTkFrame(card, fg_color="transparent")
        interno.pack(fill="x", padx=28, pady=24)

        ctk.CTkLabel(
            interno,
            text="Link do vídeo",
            font=("Segoe UI", 12, "bold"),
            text_color=TEXT_MUTED
        ).pack(anchor="w", pady=(0, 6))

        entry = ctk.CTkEntry(
            interno,
            width=420,
            height=42,
            corner_radius=10,
            placeholder_text="Cole o link do vídeo (YouTube, etc.)..."
        )
        entry.pack(anchor="w", pady=(0, 16))

        botao_baixar = ctk.CTkButton(
            interno,
            text="⬇  Baixar vídeo",
            width=220,
            height=44,
            fg_color="transparent",
            border_width=2,
            border_color=GREEN,
            text_color=GREEN,
            hover_color=GREEN_HOVER,
            corner_radius=12,
            font=("Segoe UI", 14, "bold"),
        )
        botao_baixar.configure(command=lambda: baixar_video(content, entry, botao_baixar))
        botao_baixar.pack(anchor="w")

        ctk.CTkLabel(
            content,
            text="ℹ  Certifique-se de que o servidor (server.py) esteja rodando antes de baixar.",
            font=("Segoe UI", 12),
            text_color=TEXT_FAINT
        ).pack(anchor="w", padx=70, pady=(16, 0))

    # ARQUIVO DO PC

    def tela_pc():

        limpar()
        marcar_ativo("pc")

        titulo("Selecionar do computador")
        subtitulo("Escolher um vídeo e um áudio direto do seu PC")

        card = cartao()

        interno = ctk.CTkFrame(card, fg_color="transparent")
        interno.pack(fill="x", padx=28, pady=24)

        config_atual = carregar_config()

        video_txt = "Nenhum vídeo selecionado"
        audio_txt = "Nenhum áudio selecionado"

        if config_atual.get("video"):
            video_txt = f"🎬  {os.path.basename(config_atual['video'])}"
        if config_atual.get("audio"):
            audio_txt = f"🎵  {os.path.basename(config_atual['audio'])}"

        label_video = ctk.CTkLabel(interno, text=video_txt, text_color=TEXT_MUTED, anchor="w")
        label_video.pack(anchor="w", pady=(0, 6))

        label_audio = ctk.CTkLabel(interno, text=audio_txt, text_color=TEXT_MUTED, anchor="w")
        label_audio.pack(anchor="w", pady=(0, 18))

        ctk.CTkButton(
            interno,
            text="📁  Escolher arquivo",
            width=220,
            height=44,
            fg_color="transparent",
            border_width=2,
            border_color=BLUE,
            text_color=BLUE,
            hover_color=BLUE_HOVER,
            corner_radius=12,
            font=("Segoe UI", 14, "bold"),
            command=lambda: escolher_video_pc(label_video, label_audio)
        ).pack(anchor="w")

        ctk.CTkLabel(
            content,
            text="ℹ  É preciso escolher um vídeo (.mp4/.mov/.avi/.mkv) e um áudio (.mp3) para salvar.",
            font=("Segoe UI", 12),
            text_color=TEXT_FAINT
        ).pack(anchor="w", padx=70, pady=(16, 0))

    # GERENCIAR VIDEOS

    def tela_gerenciar():

        limpar()
        marcar_ativo("gerenciar")

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

        arquivos_validos = sorted(set(base_videos.keys()) & set(base_audios.keys()))

        if not arquivos_validos:

            card = cartao()
            ctk.CTkLabel(
                card,
                text="Nenhum vídeo com áudio correspondente encontrado.\nBaixe algo na aba \"Download internet\".",
                text_color=TEXT_MUTED,
                justify="left"
            ).pack(anchor="w", padx=28, pady=24)

            return

        config_atual = carregar_config()
        video_ativo = os.path.basename(config_atual.get("video", ""))

        lista = ctk.CTkScrollableFrame(
            content,
            fg_color="transparent",
            width=760,
            height=430,
        )
        lista.pack(anchor="w", padx=70, fill="both", expand=True)

        linhas = {}
        selos = {}
        titulos = {}

        def repintar():
            for nome, frame in linhas.items():
                ativo = base_videos[nome] == video_ativo
                frame.configure(border_color=GREEN if ativo else CARD_BORDER)
                selos[nome].configure(text="✔  Em uso" if ativo else "")
                titulos[nome].configure(font=("Segoe UI", 13, "bold" if ativo else "normal"))

        for nome in arquivos_validos:

            video_path = os.path.join(video_dir, base_videos[nome])
            audio_path = os.path.join(audio_dir, base_audios[nome])

            ativo = base_videos[nome] == video_ativo

            frame = ctk.CTkFrame(
                lista,
                fg_color=CARD_BG,
                corner_radius=14,
                border_width=2,
                border_color=GREEN if ativo else CARD_BORDER,
            )
            frame.pack(anchor="w", fill="x", pady=6, padx=2)
            linhas[nome] = frame

            interno = ctk.CTkFrame(frame, fg_color="transparent")
            interno.pack(fill="x", padx=18, pady=14)

            titulo_linha = ctk.CTkLabel(
                interno,
                text=f"🎬  {base_videos[nome]}",
                font=("Segoe UI", 13, "bold" if ativo else "normal"),
                text_color=TEXT,
                anchor="w"
            )
            titulo_linha.pack(side="left", fill="x", expand=True)
            titulos[nome] = titulo_linha

            selo = ctk.CTkLabel(
                interno,
                text="✔  Em uso" if ativo else "",
                font=("Segoe UI", 12, "bold"),
                text_color=GREEN,
                width=90
            )
            selo.pack(side="left", padx=10)
            selos[nome] = selo

            def selecionar(v=video_path, a=audio_path, n=nome):

                nonlocal video_ativo

                salvar_config(v, a)
                video_ativo = base_videos[n]
                repintar()

            ctk.CTkButton(
                interno,
                text="Usar",
                width=90,
                height=32,
                corner_radius=8,
                fg_color=GREEN,
                hover_color="#047857",
                font=("Segoe UI", 13, "bold"),
                command=selecionar
            ).pack(side="left")

    # SIDEBAR

    ctk.CTkLabel(
        sidebar,
        text="👁  WAKE UP",
        font=("Segoe UI", 22, "bold"),
        text_color=TEXT
    ).pack(pady=(35, 5))

    ctk.CTkLabel(
        sidebar,
        text="CONFIGURAÇÕES",
        font=("Segoe UI", 11, "bold"),
        text_color=TEXT_FAINT
    ).pack(pady=(0, 20))

    def botao_sidebar(texto, comando):

        return ctk.CTkButton(
            sidebar,
            text=texto,
            height=44,
            fg_color="transparent",
            hover_color=SIDEBAR_ACTIVE,
            text_color=TEXT,
            anchor="w",
            corner_radius=10,
            font=("Segoe UI", 14),
            command=comando
        )

    botoes_sidebar["download"] = botao_sidebar("🌐   Download internet", tela_download)
    botoes_sidebar["download"].pack(fill="x", padx=18, pady=4)

    botoes_sidebar["pc"] = botao_sidebar("💻   Arquivo do PC", tela_pc)
    botoes_sidebar["pc"].pack(fill="x", padx=18, pady=4)

    botoes_sidebar["gerenciar"] = botao_sidebar("🎬   Gerenciar vídeos", tela_gerenciar)
    botoes_sidebar["gerenciar"].pack(fill="x", padx=18, pady=4)

    ctk.CTkButton(
        sidebar,
        text="←   Voltar",
        height=46,
        fg_color="transparent",
        border_width=2,
        border_color=RED,
        text_color=RED,
        hover_color=RED_HOVER,
        font=("Segoe UI", 14, "bold"),
        corner_radius=12,
        command=voltar_menu
    ).pack(side="bottom", padx=18, pady=30, fill="x")

    tela_download()

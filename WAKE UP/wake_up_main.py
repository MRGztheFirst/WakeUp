import cv2
import mediapipe as mp
import threading
import time
import pygame
import os
import sys
import subprocess
import json

JANELA = "WAKE UP — Monitorando"

# Cores em BGR (para desenhar com OpenCV)
VERDE = (129, 185, 16)      # #10b981
AMBAR = (36, 191, 251)      # #fbbf24
VERMELHO = (113, 113, 248)  # #f87171
BRANCO = (245, 245, 245)
CINZA = (175, 163, 156)     # #9ca3af
PRETO_HUD = (24, 24, 27)    # #18181b

CORES_DIRECAO = {
    "CENTRO": VERDE,
    "ESQUERDA": AMBAR,
    "DIREITA": AMBAR,
    "CIMA": AMBAR,
    "BAIXO": AMBAR,
}


def voltar_ao_menu():
    # voltar para o menu
    menu_path = os.path.join(os.path.dirname(__file__), "menu.py")
    try:
        subprocess.Popen([sys.executable, menu_path])
    except Exception as e:
        print(f"Erro ao voltar para o menu: {e}")

    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()
    sys.exit()


def desenhar_hud(frame, direcao, cor):
    h, w = frame.shape[:2]

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 56), PRETO_HUD, -1)
    cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)

    cv2.circle(frame, (30, 28), 9, cor, -1)
    cv2.putText(frame, "WAKE UP", (52, 36), cv2.FONT_HERSHEY_DUPLEX, 0.7, BRANCO, 1, cv2.LINE_AA)

    texto_status = f"STATUS: {direcao}"
    (tw, _), _ = cv2.getTextSize(texto_status, cv2.FONT_HERSHEY_DUPLEX, 0.7, 1)
    cv2.putText(frame, texto_status, (w - tw - 24, 36), cv2.FONT_HERSHEY_DUPLEX, 0.7, cor, 1, cv2.LINE_AA)

    dica = "ESC para sair"
    (dw, _), _ = cv2.getTextSize(dica, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.putText(frame, dica, (w - dw - 16, h - 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, CINZA, 1, cv2.LINE_AA)


def desenhar_banner_punicao(frame, centro):
    h, w = frame.shape[:2]

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 50), PRETO_HUD, -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    cor = VERDE if centro else VERMELHO
    texto = "Pode continuar!" if centro else "Olhe para o CENTRO para continuar..."
    (tw, _), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_DUPLEX, 0.75, 1)
    cv2.putText(frame, texto, ((w - tw) // 2, 33), cv2.FONT_HERSHEY_DUPLEX, 0.75, cor, 1, cv2.LINE_AA)

    cv2.circle(frame, (26, 25), 8, cor, -1)


def desenhar_pip(frame, frame_cam, centro):
    h, w = frame.shape[:2]

    pip_w, pip_h = 200, 150
    pip = cv2.resize(frame_cam, (pip_w, pip_h))

    x0, y0 = w - pip_w - 20, h - pip_h - 20
    cor_borda = VERDE if centro else VERMELHO

    frame[y0:y0 + pip_h, x0:x0 + pip_w] = pip
    cv2.rectangle(frame, (x0, y0), (x0 + pip_w, y0 + pip_h), cor_borda, 3)


# Inicializa o mixer do pygame
pygame.mixer.init()

CONFIG_FILE = "config.json"

VIDEO_PATH = ""
AUDIO_PATH = ""

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
        VIDEO_PATH = config.get("video", "")
        AUDIO_PATH = config.get("audio", "")

# Inicializa MediaPipe Face Landmarker
mp_face_landmarker = mp.tasks.vision.FaceLandmarker.create_from_model_path("face_landmarker.task")
cap = cv2.VideoCapture(0)

ultima_abertura = 0
DELAY = 2
mostrando_video = False


def tocar_video_no_frame(video_path, audio_path):
    global mostrando_video
    mostrando_video = True

    cap_video = cv2.VideoCapture(video_path)

    # Carrega e toca o MP3
    try:
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Erro ao tocar áudio: {e}")

    while cap_video.isOpened():
        ret, frame_video = cap_video.read()
        if not ret:
            break

        # Captura frame da câmera em background para checar o rosto
        ret_cam, frame_cam_temp = cap.read()
        if not ret_cam:
            break

        # Exibe o vídeo redimensionado
        frame_video_resized = cv2.resize(frame_video, (frame_cam_temp.shape[1], frame_cam_temp.shape[0]))

        # Checa se o usuário voltou a olhar para o centro
        frame_cam_check = cv2.flip(frame_cam_temp, 1)
        h, w, _ = frame_cam_check.shape
        mp_image_check = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame_cam_check, cv2.COLOR_BGR2RGB))
        results_check = mp_face_landmarker.detect(mp_image_check)

        centro = False
        if results_check.face_landmarks:
            for face_landmarks in results_check.face_landmarks:
                nariz = face_landmarks[1]
                x, y = int(nariz.x * w), int(nariz.y * h)
                if 0.4 * w <= x <= 0.6 * w and 0.4 * h <= y <= 0.6 * h:
                    centro = True

        desenhar_banner_punicao(frame_video_resized, centro)
        desenhar_pip(frame_video_resized, frame_cam_check, centro)

        cv2.imshow(JANELA, frame_video_resized)

        if centro or (cv2.waitKey(30) & 0xFF == 27):
            break

    pygame.mixer.music.stop()
    cap_video.release()
    mostrando_video = False


print("Sistema WAKE UP ativo. Pressione ESC para sair.")

while True:
    if not mostrando_video:
        ret, frame_cam = cap.read()
        if not ret:
            break

        frame_cam = cv2.flip(frame_cam, 1)
        h, w, _ = frame_cam.shape
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame_cam, cv2.COLOR_BGR2RGB))
        results = mp_face_landmarker.detect(mp_image)

        direcao = "CENTRO"
        if results.face_landmarks:
            for face_landmarks in results.face_landmarks:
                nariz = face_landmarks[1]
                x, y = int(nariz.x * w), int(nariz.y * h)

                if x < 0.4 * w: direcao = "ESQUERDA"
                elif x > 0.6 * w: direcao = "DIREITA"
                elif y < 0.4 * h: direcao = "CIMA"
                elif y > 0.6 * h: direcao = "BAIXO"
                else: direcao = "CENTRO"

        desenhar_hud(frame_cam, direcao, CORES_DIRECAO.get(direcao, AMBAR))

        agora = time.time()
        if direcao != "CENTRO" and agora - ultima_abertura > DELAY:
            threading.Thread(target=tocar_video_no_frame, args=(VIDEO_PATH, AUDIO_PATH), daemon=True).start()
            ultima_abertura = agora

        cv2.imshow(JANELA, frame_cam)

    if cv2.waitKey(1) & 0xFF == 27:
        voltar_ao_menu()

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()

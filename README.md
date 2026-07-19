# WakeUp

Desejas não procrastinar?

Um projeto feito com um propósito de apenas diversão: olhar para o lado não é uma opção. A webcam acompanha seu rosto e, se você desviar o olhar do centro da tela, um vídeo "castigo" (com áudio) toma conta da janela até você voltar a olhar para o centro.

## Requisitos

- Python 3.11+ (testado com 3.12)
- Uma webcam

## Instalação

```
cd "WAKE UP"
pip install -r requirements.txt
```

## Como usar

Abrir o menu principal:

```
python menu.py
```

Nele dá pra configurar qual vídeo/áudio será usado como "castigo" (baixando da internet ou escolhendo um arquivo do PC) e depois clicar em **INICIAR**.

Se quiser usar a opção de baixar vídeos pela internet, rode também o servidor local (em outro terminal):

```
cd server
python server.py
```

## Estrutura do projeto

```
WAKE UP/
├── menu.py               menu principal (interface)
├── opcoes.py             tela de configurações (vídeo/áudio, download)
├── wake_up_main.py        rastreamento facial + reprodução do "castigo"
├── config.json            vídeo/áudio atualmente selecionados
├── face_landmarker.task   modelo do MediaPipe usado para detectar o rosto
├── requirements.txt
└── server/
    ├── server.py          API local que baixa vídeos (yt-dlp) para a tela "Gerenciar vídeos"
    └── downloads/         vídeos e áudios baixados
```

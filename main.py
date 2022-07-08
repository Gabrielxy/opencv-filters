from os import system
from matplotlib import pyplot as plt
import cv2
import numpy as np

## Util 1: Verificar Alpha Channel
### Verifica se a imagem possui 4 canais, (R G B A) e converte para RGBA caso não tenha.
def verificar_alpha_channel(imagem):
    try:
        imagem.shape[3] # 4 indice
    except IndexError:
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGBA)
    return imagem

## Util 2: Aplicar sobreposição de cor
## Aplica uma máscara de cor na imagem (pode ser usado para aplicar qualquer cor).
def Aplicar_Sobr_Cor(imagem, intensidade=0.2, blue=0, green=0, red=0):
    imagem = verificar_alpha_channel(imagem)
    imagem_h, imagem_w, imagem_c = imagem.shape
    color_bgra = (blue, green, red, 1)
    overlay = np.full((imagem_h, imagem_w, 4), color_bgra, dtype='uint8')
    cv2.addWeighted(overlay, intensidade, imagem, 1.0, 0, imagem)
    alt = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    return alt

## Filtro 1: Converter para Negativo
### Inverte os bits da imagem usando o 'bitwise_not'.
def cvt_Negativo(imagem):
    alt = cv2.bitwise_not(imagem)
    return alt

## Filtro 2: Converter para Cinza
### Coverte o esquema de cores R G B para Cinza, depois mescla usando o 'merge'.
def cvt_Cinza(imagem):
    gray = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
    alt = cv2.merge((gray, gray, gray))
    return alt

## Filtro 3: Aplicar Óleo
### Aplica o efeito de Óleo (suavisação) na imagem usando diltros de convolução.
def add_Oleo(imagem):
    alt = cv2.edgePreservingFilter(imagem, flags=1, sigma_s=60, sigma_r=0.4)
    return alt

## Filtro 4: Aplicar Blur
### Aplica o efeito de Blur (borrão) na imagem usando o kernel size.
def add_Blur(imagem):
    alt = cv2.blur(imagem, (5,5))
    return alt

## Filtro 5: Aplicar Sépia
### Aplica a máscara de cor Sépia na imagem (usa o método de Aplicar_Sobr_Cor)
def add_Sepia(imagem, intensidade = 1):
    blue = 20
    green = 66
    red = 116
    alt = Aplicar_Sobr_Cor(imagem, intensidade=intensidade, blue=blue, green=green, red=red)
    return alt

## Filtro 6: Aprimorar Detalhes
### Usa o 'detailEnhance' de acordo com as propriedades de sigma já explicadas para aprimorar as cores
def Aprimorar_Detalhes(imagem):
    alt = cv2.detailEnhance(imagem, sigma_s=15, sigma_r=0.15)
    return alt

## Mostrando comparação - Interface PyPlot
def ShowImg(imagem, alterada):
    plt.subplot(121), plt.imshow(imagem), plt.title('Original')
    plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(alterada), plt.title('Alterada')
    plt.xticks([]), plt.yticks([])
    plt.show()

## Carregando Imagem - Interface Console
def Start():
    print("====== Carregar imagem ======")
    path = input("Caminho: ")
    print("=============================")
    Menu(path)

## Gerando Menu - Interface Console
def Menu(path="image.jpg"):
    system('cls')

    currentPath = path

    ## Lendo a imagem orignal (por padrão faz a leitura em BGR)
    original = cv2.imread(currentPath)

    ## Convertendo de BGR para RGB
    img = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

    print('''====== Filtros OpenCV ======
1. Converter para Negativo
2. Converter para Cinza
3. Aplicar Blur
4. Aplicar Óleo
5. Aplicar Sépia
6. Aprimorar detalhes
0. Sair
============================''')

    opt = int(input("Selecione (0-6): "))

    match opt:
        case 1:
            ShowImg(img, cvt_Negativo(img))
            Menu(currentPath)
        case 2:
            ShowImg(img, cvt_Cinza(img))
            Menu(currentPath)
        case 3:
            ShowImg(img, add_Blur(img))
            Menu(currentPath)
        case 4:
            ShowImg(img, add_Oleo(img))
            Menu(currentPath)
        case 5:
            ShowImg(img, add_Sepia(img))
            Menu(currentPath)
        case 6:
            ShowImg(img, Aprimorar_Detalhes(img))
            Menu(currentPath)
        case 0:
            exit()
        case _:
            Menu(currentPath)

## Iniciando aplicação
Start()

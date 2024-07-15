from PIL import Image
import os
import cv2
import numpy as np


# Função para ajustar o brilho da imagem
def ajustar_brilho(imagem, alpha=1.5, beta=30):
        imagem_array = np.array(imagem)

        imagem_array_ajustada = cv2.convertScaleAbs(imagem_array, alpha=alpha, beta=beta)

        imagem_ajustada = Image.fromarray(imagem_array_ajustada)

        return imagem_ajustada

# Ajustar o brilho e borrões da imagem
def aumentar_gradual_brilho(input_folder, output_folder):
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for nome_doc in os.listdir(input_folder):
        if nome_doc.endswith(".png"):
            caminho_imagem = os.path.join(input_folder, nome_doc)

            imagem = Image.open(caminho_imagem)

            imagem_ajustada = ajustar_brilho(imagem, alpha=1.1, beta=20)

            caminho_saida = os.path.join(output_folder, nome_doc)
            imagem_ajustada.save(caminho_saida)
            imagem.close()
            imagem_ajustada.close()


print('--------------------------------------------')
print('Qualidade das imagens alteradas com sucesso!')
print('--------------------------------------------')

input_folder = r".\1_pdfImagem"
output_folder = r".\2_limiarizacao"

aumentar_gradual_brilho(input_folder, output_folder)

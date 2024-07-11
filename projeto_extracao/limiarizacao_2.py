from PIL import Image
import os
import cv2
import numpy as np


# Função para ajustar o brilho da imagem
def adjust_brightness(image, alpha=1.5, beta=30):
    img_array = np.array(image)

    adjusted_image_array = cv2.convertScaleAbs(img_array, alpha=alpha, beta=beta)

    adjusted_image = Image.fromarray(adjusted_image_array)

    return adjusted_image

# Ajustar o brilho e borrões da imagem
def gradually_increase_brightness(input_folder, output_folder):
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            image_path = os.path.join(input_folder, filename)

            image = Image.open(image_path)

            adjusted_image = adjust_brightness(image, alpha=1.1, beta=20)

            output_path = os.path.join(output_folder, filename)
            adjusted_image.save(output_path)
            image.close()
            adjusted_image.close()
    
    print('--------------------------------------------')
    print('Qualidade das imagens alteradas com sucesso!')
    print('--------------------------------------------')

input_folder = r".\1_pdfImagem"
output_folder = r".\2_limiarizacao"

gradually_increase_brightness(input_folder, output_folder)

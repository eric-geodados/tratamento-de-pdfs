import os
from PIL import Image
import pytesseract
from pathlib import Path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def converter_imagens_para_pdf(pasta_entrada, pasta_saida):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    for nome_arquivo in os.listdir(pasta_entrada):
        caminho_imagem = os.path.join(pasta_entrada, nome_arquivo)
        nome_sem_extensao = Path(nome_arquivo).stem
        
        pdf = pytesseract.image_to_pdf_or_hocr(caminho_imagem, extension='pdf')
        
        with open(os.path.join(pasta_saida, (f'{nome_sem_extensao}.pdf')), 'w+b') as f:
            f.write(pdf)

    print('-----------------------------------------------')
    print("Conversão de imagem para PDF feita com sucesso!")
    print('-----------------------------------------------')
    
pasta_entrada = r".\2_limiarizacao"
pasta_saida = r".\3_imagemPdfOCR"

converter_imagens_para_pdf(pasta_entrada, pasta_saida)

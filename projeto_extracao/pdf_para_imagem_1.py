from pdf2image import convert_from_path
import os
from pathlib import Path
import pytesseract
import logging
from tkinter import messagebox

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def pdf_para_imagens(pasta_entrada, pasta_saida):
    # Certifique-se de que a pasta de saída existe
    os.makedirs(pasta_saida, exist_ok=True)

    for doc in os.listdir(pasta_entrada): 
        if doc.endswith(".pdf"):
            caminho_pdf_entrada = os.path.join(pasta_entrada, doc)
            
            # Converter cada página do PDF em uma imagem
            imagens = convert_from_path(caminho_pdf_entrada, poppler_path=r"C:\Program Files\poppler-24.02.0\Library\bin")
            
            # Salvar cada imagem em arquivos separados
            for i, imagem in enumerate(imagens):
                # Rodar a função que retorna se a imagem é branca ou não
                caminho_imagem_saida = os.path.join(pasta_saida, f'{i+1}_{Path(caminho_pdf_entrada).stem}.png')
                imagem.save(caminho_imagem_saida, 'PNG')
                
                # Caso a imagem salva estiver em branco será removida
                if verificar_pdf_em_branco(caminho_imagem_saida):
                    logging.info(f'Página salva como {caminho_imagem_saida}')
                else:
                    os.remove(caminho_imagem_saida)
                    logging.warning('Página do PDF está em branco!')
                
            # logging.info('PROCESSAMENTO FINALIZADO COM SUCESSO!')

    messagebox.showinfo("STATUS DE PROCESSAMENTO", "Processamento finalizado com sucesso!!!")


def verificar_pdf_em_branco(caminho_pdf_entrada):
    str_resultado = pytesseract.image_to_string(caminho_pdf_entrada, lang='por')

    if str_resultado == "":
        return False
    return True


pdf_para_imagens(r'.\semTratamento', r'.\2_limiarizacao')
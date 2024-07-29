from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter
import os
from pathlib import Path
import pytesseract
import logging
from tkinter import messagebox
import cv2
import numpy as np
from PIL import Image
from config import ENDPOINT, PREDICTION_KEY
import requests


class Processamento:    
    def __init__(self, pasta_entrada, pasta_saida):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        self.pasta_entrada = pasta_entrada
        self.pasta_saida = pasta_saida
        
        # Executar as funções da classe
        # Processo 1
        self.pdf_para_imagens()
        # Processo 2
        self.identificar_orientacao()
        # Processo 3
        self.aumentar_gradual_brilho()
        # Processo 4
        self.converter_imagens_para_pdf()
        # Processo 5
        self.apagar_arquivos_indesejados()

    # PROCESSO 1
    def pdf_para_imagens(self):
        # Certifique-se de que a pasta de saída existe
        os.makedirs(self.pasta_saida, exist_ok=True)

        for doc in os.listdir(self.pasta_entrada): 
            if doc.endswith(".pdf"):
                self.caminho_pdf_entrada = os.path.join(self.pasta_entrada, doc)
                
                # Converter cada página do PDF em uma imagem
                imagens = convert_from_path(self.caminho_pdf_entrada, poppler_path=r"C:\Program Files\poppler-24.02.0\Library\bin")
                
                # Salvar cada imagem em arquivos separados
                for i, imagem in enumerate(imagens):
                    # Rodar a função que retorna se a imagem é branca ou não
                    self.caminho_imagem_saida = os.path.join(self.pasta_saida, f'{i+1}_{Path(self.caminho_pdf_entrada).stem}.png')
                    imagem.save(self.caminho_imagem_saida, 'PNG')
                    
                    # Caso a imagem salva estiver em branco será removida
                    if self.verificar_pdf_em_branco():
                        logging.info(f'Página salva como {self.caminho_imagem_saida}')
                    else:
                        os.remove(self.caminho_imagem_saida)
                        logging.warning('Página do PDF está em branco!')
        

    def verificar_pdf_em_branco(self):
        str_resultado = pytesseract.image_to_string(self.caminho_imagem_saida, lang='por')
        if str_resultado == "":
            return False
        return True

    
    # PROCESSO 2
    def identificar_orientacao(self):
        # Configurar os cabeçalhos da solicitação
        headers = {
            "Prediction-Key": PREDICTION_KEY,
            "Content-Type": "application/octet-stream"
        }

        for nome_arquivo in os.listdir(self.pasta_saida):
            if nome_arquivo.endswith(".png"):
                caminho_imagem = os.path.join(self.pasta_saida, nome_arquivo)
                nome_sem_extensao = Path(nome_arquivo).stem

                # Ler o arquivo de imagem em modo binário
                with open(caminho_imagem, "rb") as arquivo_imagem:
                    imagem_data = arquivo_imagem.read()

                # Enviar a solicitação
                response = requests.post(ENDPOINT, headers=headers, data=imagem_data)

                # Verificar e exibir os resultados
                if response.status_code == 200:
                    predicoes = response.json()["predictions"]
                    # Encontrar a predição com a maior probabilidade
                    melhor_predicao = max(predicoes, key=lambda p: p["probability"])
                    if melhor_predicao['tagName'] == '90 graus':
                        graus = -90
                    elif melhor_predicao['tagName'] == '180 graus':
                        graus = -180
                    elif melhor_predicao['tagName'] == '270 graus':
                        graus = -270
                    print(graus)
                    self.rotacionar_imagens(caminho_imagem, self.pasta_entrada, nome_arquivo, graus)
            else:
                print(f"Error: {response.status_code}, {response.text}")

    def rotacionar_imagens(self, caminho_imagem, caminho_saida, nome_arq, graus=0):
        imagem = Image.open(caminho_imagem)
        
        imagem_rotacionada = imagem.rotate(graus, expand=True)
        
        imagem_rotacionada.save(f'{caminho_saida}\{nome_arq}')


    # PROCESSO 3
    # Função para ajustar o brilho da imagem
    def ajustar_brilho(self, imagem, alpha=1.5, beta=30):
        imagem_array = np.array(imagem)

        imagem_array_ajustada = cv2.convertScaleAbs(imagem_array, alpha=alpha, beta=beta)

        imagem_ajustada = Image.fromarray(imagem_array_ajustada)

        return imagem_ajustada

    # Ajustar o brilho e borrões da imagem
    def aumentar_gradual_brilho(self):
        if not os.path.exists(self.pasta_saida):
            os.makedirs(self.pasta_saida)

        if not os.path.exists(self.pasta_entrada):
            os.makedirs(self.pasta_entrada)

        for nome_doc in os.listdir(self.pasta_entrada):
            if nome_doc.endswith(".png"):
                caminho_imagem = os.path.join(self.pasta_entrada, nome_doc)

                imagem = Image.open(caminho_imagem)

                imagem_ajustada = self.ajustar_brilho(imagem, alpha=1.1, beta=20)

                caminho_saida = os.path.join(self.pasta_saida, nome_doc)
                imagem_ajustada.save(caminho_saida)
                imagem.close()
                imagem_ajustada.close()
                
                logging.info(f'Qualidade da imagem {nome_doc} alterada com sucesso!')


    # PROCESSO 4
    def converter_imagens_para_pdf(self):
        if not os.path.exists(self.pasta_saida):
            os.makedirs(self.pasta_saida)

        for nome_arquivo in os.listdir(self.pasta_saida):
            if nome_arquivo.endswith(".png"):
                caminho_imagem = os.path.join(self.pasta_saida, nome_arquivo)
                nome_sem_extensao = Path(nome_arquivo).stem
                
                pdf = pytesseract.image_to_pdf_or_hocr(caminho_imagem, extension='pdf')
                
                with open(os.path.join(self.pasta_entrada, (f'{nome_sem_extensao}.pdf')), 'w+b') as f:
                    f.write(pdf)

                logging.info(f'Conversão de {nome_arquivo} para PDF feita com sucesso!')
                
                # Limpar os arquivos 
                os.remove(caminho_imagem)
    
    # PROCESSO 5
    def apagar_arquivos_indesejados(self):
        for nome_arquivo in os.listdir(self.pasta_entrada):
            if nome_arquivo.endswith(".png"):
                caminho_arquivo = os.path.join(self.pasta_entrada, nome_arquivo)
                os.remove(caminho_arquivo)


        messagebox.showinfo("STATUS DE PROCESSAMENTO", "Processamento finalizado com sucesso!!!")

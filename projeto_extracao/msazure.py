import os
from pathlib import Path
import requests
from PIL import Image


def identificar_orientacao():
    # Defina os detalhes da API
    endpoint = "https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/2f52a48e-2c9e-4e9d-90a7-ce99c8dac971/detect/iterations/SegundoTreinamento/image"
    prediction_key = "243a93d9544a4a408f4a564154b2fdbb"

    # Configurar os cabeçalhos da solicitação
    headers = {
        "Prediction-Key": prediction_key,
        "Content-Type": "application/octet-stream"
    }

    for nome_arquivo in os.listdir(pasta_entrada):
        if nome_arquivo.endswith(".png"):
            caminho_imagem = os.path.join(pasta_entrada, nome_arquivo)

        # Ler o arquivo de imagem em modo binário
        with open(caminho_imagem, "rb") as arquivo_imagem:
            imagem_data = arquivo_imagem.read()

        # Enviar a solicitação
        response = requests.post(endpoint, headers=headers, data=imagem_data)

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
            rotacionar_imagens(caminho_imagem, pasta_saida, nome_arquivo, graus)
        else:
            print(f"Error: {response.status_code}, {response.text}")


def rotacionar_imagens(caminho, cam_saida, nome_arq, graus):
    imagem = Image.open(caminho)
    
    imagem_rotacionada = imagem.rotate(graus, expand=True)
    
    imagem_rotacionada.save(f'{cam_saida}\{nome_arq}.png')

pasta_entrada = r'.\3_imagemPdfOCR'
pasta_saida = r'.\comTratamento'
identificar_orientacao()

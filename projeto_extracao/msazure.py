import os
from pathlib import Path
import requests

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
            nome_sem_extensao = Path(nome_arquivo).stem

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
            print(f"Nome do arquivo: {nome_sem_extensao}, Tag: {melhor_predicao['tagName']}, Probability: {melhor_predicao['probability']*100:.2f}%")
        else:
            print(f"Error: {response.status_code}, {response.text}")


pasta_entrada = r'.\2_limiarizacao'
pasta_saida = r'.\comTratamento'
identificar_orientacao()

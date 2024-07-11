import pymupdf
import os


def obter_orientacao_pagina(caminho_pdf, numero_pagina):
    """Retorna a orientação de uma página específica em um PDF.

    Args:
        caminho_pdf (str): Caminho para o arquivo PDF.
        numero_pagina (int): Número da página (começando em 0).

    Returns:
        str: "Retrato", "Paisagem" ou "Rotação desconhecida".
    """
    doc = pymupdf.open(caminho_pdf)
    pagina = doc.load_page(numero_pagina)
    rotacao = pagina.rotation
    if rotacao == 0:
        return "Retrato"
    elif rotacao == 90 or rotacao == 270:
        return "Paisagem"
    else:
        return "Rotação desconhecida"

# Exemplo de uso:
pasta_entrada = r".\3_imagemPdfOCR"
pasta_saida = r".\4_extracaoTexto"
caminho_do_arquivo = os.path.join(pasta_entrada, '1_2012_000000_004723_98-2012_000000_000000_ALV_004.pdf')
orientacao = obter_orientacao_pagina(caminho_do_arquivo, 0)  # Verifica a primeira página
print(f"Orientação da página: {orientacao}")

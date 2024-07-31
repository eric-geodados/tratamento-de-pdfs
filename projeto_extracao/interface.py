import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import tkinter.font as tkFont
import processamento_completo_atualizado as processamento_atualizado
import utils
from utils import logging

class Interface:

    cor = "#13191C"
    cor_botoes = "#00ABD1"
    fonte = "Segoe UI"

    # Configurações da janela principal
    def iniciar_interface(self):
        janela = tk.Tk()
        janela.title("Processador de PDFs")
        janela.geometry("1050x450")
        janela.configure(bg=self.cor)

        # Estilos
        fonte_titulos = tkFont.Font(family="Segoe UI", size=22, weight="bold")
        fonte_padrao = tkFont.Font(family="Segoe UI", size=14, weight="bold")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=fonte_padrao, background=self.cor_botoes, foreground="white", padding=3)
        style.map("TButton", background=[("active", "#008CAB")])

        # Frame principal com cor de fundo
        frame = ttk.Frame(janela, padding="20", style="Custom.TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Configurando a cor de fundo do frame
        style.configure("Custom.TFrame", background=self.cor)

        # Variáveis para armazenar os caminhos das pastas
        self.pasta_entrada = tk.StringVar()
        self.pasta_entrada.trace("w", self.desabilitador_botao)  # Monitora alterações no StringVar
        self.pasta_saida = tk.StringVar()
        self.pasta_saida.trace("w", self.desabilitador_botao)  # Monitora alterações no StringVar
    

        ttk.Label(frame, text="PROCESSADOR DE PDFS", font=fonte_titulos, background=self.cor, foreground="white").grid(column=0, row=0, padx=10, pady=5, columnspan=4)
        ttk.Label(frame, text="―――"*29, font=(self.fonte, 8), background=self.cor, foreground="white").grid(column=0, row=1, padx=10, pady=5, columnspan=4)


        # Labels para mostrar os caminho da pasta de entrada
        ttk.Label(frame, text="Caminho de entrada:", font=(self.fonte, 16), background=self.cor, foreground="white").grid(column=0, row=2, padx=10, pady=10, sticky="e")
        ttk.Label(frame, textvariable=self.pasta_entrada, font=(self.fonte, 12), background="white", width=60).grid(column=1, row=2, padx=10, pady=10)

        # Labels para mostrar os caminho da pasta de saída
        ttk.Label(frame, text="Caminho de saída:", font=(self.fonte, 16), background=self.cor, foreground="white").grid(column=0, row=3, padx=10, pady=10, sticky="e")
        ttk.Label(frame, textvariable=self.pasta_saida, font=(self.fonte, 12), background="white", width=60).grid(column=1, row=3, padx=10, pady=10)

        # Botões para abrir pastas
        ttk.Button(frame, text="Selecionar Pasta", command=self.abrir_pasta_entrada).grid(column=2, row=2, pady=10)
        ttk.Button(frame, text="Selecionar Pasta", command=self.abrir_pasta_saida).grid(column=2, row=3, pady=10)

        # Botão Processar
        self.botao_processar = ttk.Button(frame, text="Processar", command=self.processamento, padding=10)
        self.botao_processar.grid(column=0, row=4, sticky="ew", columnspan=4, pady=10)
        self.botao_processar.config(state=tk.DISABLED)

        # Text widget para exibir o log
        self.log_texto = tk.Text(frame, state='disabled', height=5)
        self.log_texto.grid(column=0, row=5, sticky="ew", columnspan=4, pady=10)
        

        # Configurar o logger
        self.texto_handler = utils.TextHandler(self.log_texto)
        utils.logging.basicConfig(level=utils.logging.INFO, handlers=[self.texto_handler], format='%(asctime)s - %(levelname)s - %(message)s')

        # Créditos ao Desenvolvedor
        ttk.Label(frame, text="2024 © Desenvolvido por Eric Cabral", font=('Segoe UI', 10), background=self.cor, foreground="white").grid(column=0, row=6, padx=5, pady=10, sticky='w', columnspan=4)

        janela.mainloop()
      
        
    # Função para abrir os seletores de pasta
    def abrir_pasta_entrada(self):
        caminho = filedialog.askdirectory()
        if caminho:
            self.pasta_entrada.set(caminho)

    def abrir_pasta_saida(self):
        caminho = filedialog.askdirectory()
        if caminho:
            self.pasta_saida.set(caminho)

            
    # Função para desabilitar botão até selecionar pastas
    def desabilitador_botao(self, *args):
        if self.pasta_entrada.get().strip() and self.pasta_saida.get().strip():
            self.botao_processar.config(state=tk.NORMAL)
        else:
            self.botao_processar.config(state=tk.DISABLED)


    # Função para executar os processos já elaborados
    def processamento(self):
        # pdf_para_imagem_1.pdf_para_imagens(self.pasta_entrada.get(), self.pasta_saida.get())
        processamento_atualizado.Processamento(self.pasta_entrada.get(), self.pasta_saida.get())

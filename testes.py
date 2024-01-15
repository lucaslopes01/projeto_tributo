import os
import csv
from zipfile import ZipFile
from threading import Thread

class SuaClasse:
    def __init__(self):
        # Inicialize aqui, se necessário
        pass

    def processa_arquivo(self, caminho_arquivo):
        lista = []
        with open(caminho_arquivo, 'r') as file:
            csv_reader = csv.DictReader(file)
            for linha in csv_reader:
                cnpj = linha['cnpj'].replace('.', '').replace('/', '').replace('-', '')
                cnpj_base = linha['cnpj'].replace('.', '').replace('/', '').replace('-', '')[:8]
                cnpj_scp = linha['cnpj_da_scp'].replace('.', '').replace('/', '').replace('-', '')

                lista.append((linha['ano'], cnpj, cnpj_base, cnpj_scp, linha['forma_de_tributacao'], linha['quantidade_de_escrituracoes']))

        return lista

    def processa_zip(self, caminho_arquivo):
        with ZipFile(caminho_arquivo, 'r') as arquivos:
            arquivos.extractall(os.getenv('CAMINHO_ZIP'))

        caminho = os.getenv('CAMINHO_ZIP').replace('\\\\', '\\')
        arquivos_zip = [os.path.join(caminho, arquivo) for arquivo in os.listdir(caminho)]
        
        threads = []
        for arquivo in arquivos_zip:
            thread = Thread(target=self.processa_e_insere, args=(arquivo,))
            threads.append(thread)
            thread.start()

        # Aguarda todas as threads concluírem
        for thread in threads:
            thread.join()

    def processa_e_insere(self, caminho_arquivo):
        lista = self.processa_arquivo(caminho_arquivo)
        inserir = "insert into regime_tributario(ano, cnpj, cnpj_base, cnpj_da_scp, forma_tributacao, quantidade_de_escrituracoes) values(%s, %s, %s, %s, %s, %s)"
        self.mysql.ExecMany(inserir, lista)
        print(f'{len(lista)} foram adicionadas ao banco')

    def remover_arquivos_zip(self, caminho):
        for arquivo in os.listdir(caminho):
            os.remove(os.path.join(caminho, arquivo))

    def envia_arquivo_banco(self, caminho_arquivo, nome_arquivo):
        self.processa_zip(caminho_arquivo)
        self.remover_arquivos_zip(os.getenv('CAMINHO_ZIP'))


# Uso da classe
# instancia = SuaClasse()
# instancia.envia_arquivo_banco(caminho_do_arquivo_zip, nome_do_arquivo_zip)
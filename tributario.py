import requests
from zipfile import ZipFile
import csv 
import os
class Tributario:
    def __init__(self, pymysql) :
        self.mysql = pymysql
        
    def baixa_arquivo(self, urls, filename):
        url = urls
        local_filename = filename

        headers = {
            'Referer': 'https://dados.rfb.gov.br/CNPJ/regime_tributario/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"'
        }

        response = requests.get(url, headers=headers)


        if response.status_code == 200:
            with open(local_filename, 'wb') as file:
                file.write(response.content)
            print(f'arquivo baixado {local_filename}')
        else:
            print(f'arquivo não baixado {response.status_code}')




    def envia_arquivo_banco(self, caminho_arquivo, nome_arquivo):
        with ZipFile(caminho_arquivo, 'r') as arquivos:
          arquivos.extractall(os.getenv('CAMINHO_ZIP'))
          

       
        caminho = os.getenv('CAMINHO_ZIP').replace('\\\\', '\\')
        os.listdir(caminho)
        verifica = 0
        linhas = 0
        with open(os.path.join(caminho, os.listdir(caminho)[0] ), 'r' ) as file:
            csv_reader = csv.DictReader(file)
            for linha in csv_reader:
                
                if verifica <=3:
                    cnpj = linha['cnpj'].replace('.', '').replace('/', '').replace('-', '')
                    cnpj_base = linha['cnpj'].replace('.', '').replace('/', '').replace('-', '')[:8]
                    
                    listando = {'ano':linha['ano'], 'cnpj': cnpj, 'cnpj_base': cnpj_base, 'cnpj_scp': linha['cnpj_da_scp'], 'forma_de_tributacao': linha['forma_de_tributacao'], 'quantidade_de_escrituracoes': linha['quantidade_de_escrituracoes'] }
                    
                    inserir = f"""insert into regime_tributario(ano, cnpj, cnpj_base, cnpj_da_scp, forma_tributacao, quantidade_de_escrituracoes)value('{listando["ano"]}', '{cnpj}', '{cnpj_base}', '{listando["cnpj_scp"]}', '{listando["forma_de_tributacao"]}', '{listando["quantidade_de_escrituracoes"]}')"""
                    self.mysql.processa_comando(inserir)
                    linhas += 1
                    print(f'{linhas} foi adicionada ao banco')
                    verifica+=1
                else:
                    break
        
                
                
        os.remove(os.path.join(os.getenv('CAMINHO_ZIP'), os.listdir(caminho)[0]))
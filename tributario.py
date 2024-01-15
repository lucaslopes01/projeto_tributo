import requests
from zipfile import ZipFile
import csv 
import os
import threading as th
import multiprocessing as mp

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




    def le_arquivo(self ):
        destino = os.getenv('CAMINHO_ZIP')
      
        
        if not os.path.exists(destino):
            os.makedirs(destino)
        else:
            print('não consegui criar a pasta')
        
               
        for l in os.listdir(os.getenv('CAMINHO')):
            with ZipFile(os.path.join(os.getenv('CAMINHO'),l ).replace('\\\\', '\\'), 'r') as arquivos:
                arquivos.extractall(os.getenv('CAMINHO_ZIP'))
    
          
          

     

      
       
        
    
       
    def trata_arquivo(self):
        lst_process = {0: None, 1: None, 2: None}
        caminho = os.getenv('CAMINHO_ZIP').replace('\\\\', '\\')
        self.lista = []
        self.lista_atual = []
        linhas = 0
        conta = 0
        for i in os.listdir(caminho):
            with open(os.path.join(caminho, i), 'r' ) as file:
                csv_reader = csv.DictReader(file)
                for linha in csv_reader:
                    
                    cnpj = linha['cnpj'].replace('.', '').replace('/', '').replace('-', '')
                    cnpj_base = linha['cnpj'].replace('.', '').replace('/', '').replace('-', '')[:8]
                    cnpj_scp = linha['cnpj_da_scp'].replace('.', '').replace('/', '').replace('-', '')
                    # listando = {'ano':linha['ano'], 'cnpj': cnpj, 'cnpj_base': cnpj_base, 'cnpj_scp': linha['cnpj_da_scp'], 'forma_de_tributacao': linha['forma_de_tributacao'], 'quantidade_de_escrituracoes': linha['quantidade_de_escrituracoes'] }
                    
                    self.lista_atual.append((linha['ano'], cnpj, cnpj_base, cnpj_scp ,linha['forma_de_tributacao'],linha['quantidade_de_escrituracoes'])   )
                    print(f'ja li {linhas}')
                    linhas += 1
                    if len(self.lista_atual) == 500:
                        #self.lista.append(self.lista_atual)
                        #self.lista_atual = []
                        v_th = th.Thread(target=self.envia_banco, args=(self.lista_atual, ))
                        v_th.start()
                        self.lista_atual = []
                        conta += 1

                    # if conta == 2:
                    #     for x in lst_process:
                    #         if lst_process[x]:
                    #             lst_process[x].start()
                    
        if self.lista_atual:
            self.lista.append(self.lista_atual)

                        
    
    
            
       
                    

                    # values = '
                    # for i in lista:
                    #     values = values + f"""('{i["ano"]}', '{i["cnpj"]}', '{i["cnpj_base"]}', '{i["cnpj_scp"]}', '{i["forma_de_tributacao"]}', '{i["quantidade_de_escrituracoes"]}'),"""
                    
                    # dado_final = inserir + values+ ")"
                
                    # print (dado_final)
                    
                    # inserir = f"""insert into regime_tributario(ano, cnpj, cnpj_base, cnpj_da_scp, forma_tributacao, quantidade_de_escrituracoes)value('{listando["ano"]}', '{cnpj}', '{cnpj_base}', '{listando["cnpj_scp"]}', '{listando["forma_de_tributacao"]}', '{listando["quantidade_de_escrituracoes"]}')"""
                    
         
    def envia_banco(self, dados):
        inserir = "insert into regime_tributario(ano, cnpj, cnpj_base, cnpj_da_scp, forma_tributacao, quantidade_de_escrituracoes)values"
        sql = ""
        for i in dados:
            sql += f"('{i[0]}','{i[1]}','{i[2]}','{i[3]}','{i[4]}','{i[5]}'),"
        
        query_insere = f"{inserir}{sql[:len(sql)-1]}"
        self.mysql.processa_comando(query_insere)
        # for i in dados:
        #     envia_banco = i[0]
        #     self.mysql.ExecMany(inserir, envia_banco)
            
        # if len(dados) != 0:
        #     self.mysql.ExecMany(inserir, envia_banco)
        #     print(f'{dados} foi adicionada ao banco')
        
        
    # def le_arquivo(self, caminho_arquivo ):
    #     for l in os.listdir(caminho_arquivo):
    #         with ZipFile(l, 'r') as arquivos:
    #             arquivos.extractall(os.getenv('CAMINHO_ZIP'))

        



                


                
    
                
                
        # os.remove(os.path.join(os.getenv('CAMINHO_ZIP'), os.listdir(caminho)[0]))
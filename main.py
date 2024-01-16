import os
from class_mysql import BDMySQL
from tributario import Tributario


def inicial():
    mysql = BDMySQL('b7')
    tribut = Tributario(mysql)
    caminho = os.getenv('CAMINHO')

# Certifique-se de que o caminho existe ou crie-o se não existir
    if not os.path.exists(caminho):
     os.makedirs(caminho)
    else:
       print('não consegui criar a pasta')
    # for i in os.getenv('LISTA_URLS').split(','):
       
    #     file = os.path.join(caminho,i.split('.zip')[0].split('/')[-1].replace('%20', "_")+'.zip')
        
    #     tribut.baixa_arquivo(i, file)
    tribut.le_arquivo()
    tribut.trata_arquivo()


    

    del mysql
       
if __name__ == '__main__':
    inicial()




# mysql = BDMySQL('b7')


# url = "https://dados.rfb.gov.br/CNPJ/regime_tributario/Imunes%20e%20isentas.zip"
# local_filename = "Imunes_e_isentas.zip"

# headers = {
#     'Referer': 'https://dados.rfb.gov.br/CNPJ/regime_tributario/',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#     'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Linux"'
# }

# response = requests.get(url, headers=headers)


# if response.status_code == 200:
#     with open(local_filename, 'wb') as file:
#         file.write(response.content)
#     print(f'arquivo baixado {local_filename}')
# else:
#     print(f'arquivo não baixado {response.status_code}')

# with ZipFile('Imunes_e_isentas.zip', 'r') as arquivos:
#     arquivos.extractall()

# csv_filename = 'Imunes e isentas.csv'
# coluna_desejada = 'Nome_da_Coluna'  # Substitua pelo nome real da coluna desejada

# # Lista para armazenar os valores da coluna
# ano = []
# lista = []

# with open(csv_filename, 'r') as file:
#     csv_reader = csv.DictReader(file)
    
#     for linha in csv_reader:
#         cnpj = linha['cnpj'].replace('.', '').replace('/', '').replace('-', '')
#         cnpj_base = linha['cnpj'].replace('.', '').replace('/', '').replace('-', '')[:8]
        
#         listando = {'ano':linha['ano'], 'cnpj': cnpj, 'cnpj_base': cnpj_base, 'cnpj_scp': linha['cnpj_da_scp'], 'forma_de_tributacao': linha['forma_de_tributacao'], 'quantidade_de_escrituracoes': linha['quantidade_de_escrituracoes'] }
#         lista.append(listando)
#         inserir = f"""insert into regime_tributario(ano, cnpj, cnpj_base, cnpj_da_scp, forma_tributacao, quantidade_de_escrituracoes)value('{listando["ano"]}', '{cnpj}', '{cnpj_base}', '{listando["cnpj_scp"]}', '{listando["forma_de_tributacao"]}', '{listando["quantidade_de_escrituracoes"]}')"""#
#         mysql.processa_comando(inserir)
#     print(lista)




        


# for valor in cnpj:
#     print(valor)

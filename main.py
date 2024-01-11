import requests
from zipfile import ZipFile
import os
import csv 

url = "https://dados.rfb.gov.br/CNPJ/regime_tributario/Imunes%20e%20isentas.zip"
local_filename = "Imunes_e_isentas.zip"

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

with ZipFile('Imunes_e_isentas.zip', 'r') as arquivos:
    arquivos.extractall()

csv_filename = 'Imunes e isentas.csv'
coluna_desejada = 'Nome_da_Coluna'  # Substitua pelo nome real da coluna desejada

# Lista para armazenar os valores da coluna
ano = []
cnpj = []

with open(csv_filename, 'r') as file:
    csv_reader = csv.DictReader(file)
    
    for linha in csv_reader:
        valor = linha['ano']
        valore = linha['cnpj']
        cnpj.append(valore)
        ano.append(valor)

# Imprime os valores da coluna
print(f"Valores da coluna '{coluna_desejada}':")
for valor in cnpj:
    print(valor)

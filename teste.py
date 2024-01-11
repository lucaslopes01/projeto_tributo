import requests

url = "https://dados.rfb.gov.br/CNPJ/regime_tributario/Lucro%20Arbitrado.zip"

payload = {}
headers = {
  'Referer': 'https://dados.rfb.gov.br/CNPJ/regime_tributario/',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

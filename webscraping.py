import os
import requests
import zipfile
from bs4 import BeautifulSoup

# URL do site
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Fazendo a requisição HTTP para obter o HTML da página
response = requests.get(url)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Encontrando todos os links da página
    links = soup.find_all("a", href=True)
    
    # Filtrando apenas os PDFs que contêm "Anexo I" e "Anexo II" no nome
    pdf_links = [link["href"] for link in links if "Anexo" in link.text and link["href"].endswith(".pdf")]
    
    print("Links encontrados:", pdf_links)
else:
    print("Erro ao acessar o site")

# Criar uma pasta para armazenar os arquivos
os.makedirs("anexos", exist_ok=True)

# Baixar cada PDF
for link in pdf_links:
    pdf_url = link if link.startswith("http") else "https://www.gov.br" + link  # Se o link for relativo, completamos a URL
    pdf_name = pdf_url.split("/")[-1]  # Nome do arquivo
    
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(f"anexos/{pdf_name}", "wb") as file:
            file.write(response.content)
        print(f"Baixado: {pdf_name}")
    else:
        print(f"Erro ao baixar: {pdf_url}")

# Nome do arquivo ZIP final
zip_filename = "anexos_compactados.zip"

# Criar o arquivo ZIP
with zipfile.ZipFile(zip_filename, "w") as zipf:
    for root, _, files in os.walk("anexos"):
        for file in files:
            zipf.write(os.path.join(root, file), file)

print(f"Arquivos compactados em {zip_filename}")

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os

# Inicialize o WebDriver
driver = webdriver.Chrome()

def login(driver):
    """Faz login no site."""
    driver.get("https://app.servicedesk.stefanini.io/login")

    try:
        # Aguarde até que o campo de email esteja visível e insira o email
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys("vgsousa@stefanini.com")

        # Aguarde até que o campo de senha esteja visível e insira a senha
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys("Mudar@123")

        # Clique no botão de login
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "rt-submit-login"))
        )
        login_button.click()
        time.sleep(5)

        # Aguarde e clique no botão "Continuar"
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Continuar']]"))
        )
        continue_button.click()
        time.sleep(5)
        
    except Exception as e:
        print("Erro ao fazer login:", e)

def navigate_to_summary(driver):
    """Navega até a página de resumo."""
    driver.get("https://app.servicedesk.stefanini.io/p/summarized")
    time.sleep(5)
    try:
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Continuar']]"))
        )
        continue_button.click()
    except Exception as e:
        print("Erro ao navegar para a página de resumo:", e)

def make_api_request(auth_token, start_date, end_date):
    """Realiza a requisição GET para a API."""
    url = "https://api.servicedesk.stefanini.io/reports/f/queue_log_full"
    params = {
        "start": start_date,
        "end": end_date,
        "queues": [42, 43, 44, 308],
        "includeRecordings": "true"
    }
    headers = {
        "Authorization": auth_token  # Use o token diretamente
    }
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        dados = response.json()
        
        # Debug: imprima a estrutura do JSON recebido
        print("Estrutura dos dados recebidos:", dados)

        # Filtrar dados
        audio_files = []
        if isinstance(dados, dict):  # Verifique se dados é um dicionário
            for item in dados.get('data', []):  # Substitua 'data' pela chave correta se necessário
                if isinstance(item, dict) and item.get('name') not in ['D/CNI/SAC', 'D/CNI/UNINDUSTRIA']:
                    audio_files.append(item)

        print("Dados recebidos e filtrados:", audio_files)

        # Extrair URLs dos arquivos de áudio
        audio_urls = [audio['url'] for audio in audio_files if 'url' in audio]
        
        # Chame a função para baixar os arquivos
        download_audio_files(audio_urls, "downloads/audios")
    else:
        print(f"Erro na requisição: {response.status_code}")

def download_audio_files(audio_urls, download_folder):
    """Faz o download dos arquivos de áudio a partir dos URLs fornecidos."""
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for url in audio_urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                file_name = url.split("/")[-1]
                file_path = os.path.join(download_folder, file_name)

                with open(file_path, 'wb') as audio_file:
                    audio_file.write(response.content)
                print(f"Baixado: {file_name}")
            else:
                print(f"Erro ao baixar {url}: {response.status_code}")
        except Exception as e:
            print(f"Erro ao baixar {url}: {e}")

def main():
    login(driver)
    navigate_to_summary(driver)
    
    # Use o token já existente diretamente aqui
    auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywiaWF0IjoxNjc5MDYwMDI4fQ.BGHVHV4gjKjJzragAlv_S_TK-EMJop-B_G1qBXv5hcw"
    
    # Defina as datas que você deseja filtrar
    start_date = "2024-10-25T00:00:00-03:00"
    end_date = "2024-10-26T23:59:59-03:00"
    make_api_request(auth_token, start_date, end_date)
    
    input("A página está aberta. Pressione Enter para fechar o navegador...")
    driver.quit()

if __name__ == "__main__":
    main()

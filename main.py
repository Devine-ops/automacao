import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Defina o caminho para o ChromeDriver
service = Service("C:/Users/Vinic/Desktop/python click/chromedriver.exe")

# Inicialize o WebDriver
driver = webdriver.Chrome(service=service)

# Acesse a página de login
driver.get("https://quality.necxt-ai.com/#/login")

# Tente carregar cookies existentes
try:
    with open("cookies.txt", "r") as file:
        for line in file:
            line = line.strip().rstrip(';')  # Remover espaços em branco e o ponto e vírgula
            if '=' in line:  # Verifique se há um '=' na linha
                name, value = line.split('=', 1)  
                driver.add_cookie({"name": name, "value": value})
except FileNotFoundError:
    print("Cookies não encontrados, será necessário fazer login.")

# Atualizar a página para usar os cookies
driver.refresh()

# A partir daqui, você pode continuar com a lógica de login
try:
    # Aguarde até que o botão esteja clicável e clique nele
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "full"))
    )
    button.click()

    # Aguarde até que o campo de email esteja visível
    email_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )

    # Preencha o campo de email
    email_field.send_keys("vgsousa@stefanini.com")

    # Clique no botão de submit usando o ID fornecido
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "idSIButton9"))
    )
    submit_button.click()

    # Aguarde até que o campo de senha esteja visível
    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
    )

    # Preencha o campo de senha
    password_field.send_keys("Wick#369357321")

    # Aguarde até que o botão de login (submitButton) esteja visível e clique nele
    final_submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "submitButton"))
    )
    final_submit_button.click()

    # Aguarde até que o botão que você deseja clicar esteja visível
    target_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "idSIButton9"))  # ID do botão que você quer clicar
    )
    target_button.click()

except Exception as e:
    print("Erro:", e)

# Aguarde indefinidamente até que o usuário feche manualmente o navegador
input("A página está aberta. Pressione Enter para fechar o navegador...")



#Passo de inserir as ligações na IA Stefanini


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import pandas as pd
import time

# Caminho do arquivo Excel
excel_file = "C:\\Users\\valfr\\Downloads\\REDS_ABERTOS.xlsx"

# Carregar os dados da aba "REDS"
df = pd.read_excel(excel_file, sheet_name="REDS")

# Configuração do Selenium WebDriver
driver = webdriver.Chrome()
driver.get("https://intranet.policiamilitar.mg.gov.br/autenticacaosso/login.jsf")

# Realizar login na intranet
username_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "formLogin:textLogin"))
)
password_field = driver.find_element(By.ID, "formLogin:senha")
login_button = driver.find_element(By.NAME, "formLogin:j_idt15")

# Enviar as credenciais
username_field.send_keys("1438704")
password_field.send_keys("Valfr1d@")
login_button.click()

# Clicar na opção "Google Authenticator"
google_auth_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "linkGoogle"))
)
google_auth_button.click()

# Usar PyAutoGUI para lidar com um pop-up ou clique baseado em imagem
print("Aguardando para usar PyAutoGUI...")
time.sleep(5)  # Aguarde que o pop-up ou elemento apareça

# Exemplo: Clique em um botão usando uma imagem
button_location = pyautogui.locateCenterOnScreen("google_auth_button.png", confidence=0.8)
if button_location:
    pyautogui.moveTo(button_location)
    pyautogui.click()
    print("Botão clicado com sucesso usando PyAutoGUI!")
else:
    print("Botão não encontrado na tela!")

# Aguardar a entrada manual do código do Google Authenticator
input("Digite o código de autenticação no navegador e pressione ENTER para continuar...")

# Continuar com a automação Selenium
print("Autenticação concluída, prosseguindo com o envio de mensagens...")

# Iterar pelos dados da aba "REDS" e enviar mensagens
for _, row in df.iterrows():
    masp = row['Numero_PM']
    doc_num = row['Numero_REDS']

    # Preencher o campo "Para"
    try:
        to_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "cdk-drop-list-0"))
        )
        to_field.send_keys(str(masp))
        time.sleep(1)
        to_field.send_keys(Keys.ARROW_DOWN)
        to_field.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Erro ao interagir com o campo 'Para': {e}")
        continue

    # Preencher o campo "Assunto"
    try:
        subject_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "assunto-txt"))
        )
        subject_field.send_keys("REDS em aberto")
    except Exception as e:
        print(f"Erro ao interagir com o campo 'Assunto': {e}")
        continue

    # Preencher o corpo da mensagem
    try:
        message_field = driver.find_element(By.ID, "conteudo-txt")
        message_text = (
            f"Mensagem enviada pelo Sistema.\n"
            f"Foi verificado que existe REDS em aberto sendo este usuário o relator.\n"
            f"Respeitosamente, altere o documento número: {doc_num}"
        )
        message_field.send_keys(message_text)
    except Exception as e:
        print(f"Erro ao interagir com o campo 'Mensagem': {e}")
        continue

    # Aguardar antes de enviar
    time.sleep(10)
    input("Mensagem escrita, pressione ENTER aqui no console para continuar.")

    # Enviar a mensagem
    try:
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_botao_enviar"))
        )
        send_button.click()
    except Exception as e:
        print(f"Erro ao clicar no botão 'Enviar': {e}")
        continue

    time.sleep(2)

# Manter o navegador aberto
print("Automação concluída. Feche o navegador manualmente.")
input("Pressione ENTER para finalizar.")
driver.quit()

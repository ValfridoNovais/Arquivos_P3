from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import pandas as pd
import time
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Obter credenciais de forma segura
usuario_pm = os.getenv("USUARIO_PM")
senha_intranet = os.getenv("SENHA_INTRANE")

# Verificar se as credenciais foram carregadas corretamente
if not usuario_pm or not senha_intranet:
    raise ValueError("Credenciais não encontradas! Verifique se o arquivo .env está configurado corretamente.")


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
username_field.send_keys(usuario_pm)
password_field.send_keys(senha_intranet)
login_button.click()

# Clicar na opção "Google Authenticator"
google_auth_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "linkGoogle"))
)
google_auth_button.click()


# Aguardar a entrada manual do código do Google Authenticator
input("Digite o código de autenticação no navegador e pressione ENTER para continuar...")

# Continuar com a automação Selenium
print("Autenticação concluída, prosseguindo com o envio de mensagens...")

# Iterar pelos dados da aba "REDS" e enviar mensagens
for _, row in df.iterrows():
    masp = row['Numero_PM']
    digitador = row["Digitador"]  # Obtém o nome do digitador
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
        subject_field.send_keys("🛑🛑REGISTROS EM ABERTO - ENCERRAMENTO DE REDS UU🛑🛑")
    except Exception as e:
        print(f"Erro ao interagir com o campo 'Assunto': {e}")
        continue

    # Preencher o corpo da mensagem
    try:
        message_field = driver.find_element(By.ID, "conteudo-txt")
        # Construção da mensagem
        message_text = (
            f"Caro {digitador}\n\n"
            f"Existe REDS {doc_num} em aberto sob sua responsabilidade. Por isso, incumbiu-me o Sr. Chefe da P3 / 27 BPM de encaminhar mensagem recomendando ENCERRAMENTO UU!!!\n\n"
            f"Observação: O Comando do 27º BPM recomenda que os Comandos de Companhias inste os relatores ao cumprimento das diretrizes constantes no BOLETIM TÉCNICO Nº 02 / 2016, BEM COMO RESPONSABILIZAR ADMINISTRATIVAMENTE OS DIGITADORES contumazes.\n\n"
            f"===================================================================================\n"
            f"BOLETIM TÉCNICO Nº 02 / 2016 – DAOp/Cinds (BGPM Nº 12 de 16 de Fevereiro de 2016)\n\n"
            f"\"Do Encerramento de REDS\n\n"
            f"Diante disso, a recomendação técnica é para que o policial militar registre o REDS de todas as atendidas ou integradas para o militar, durante o turno de serviço, salvo em casos justificadamente comprovados e autorizado pelo CPU/CPCia.\"\n"
            f"==================================================================================="
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

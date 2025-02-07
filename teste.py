from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 📂 Caminho do perfil correto do Chrome
user_data_dir = r"C:\Users\valfr\AppData\Local\Google\Chrome\User Data"
profile_directory = "Default"  # Substitua pelo nome correto encontrado no "chrome://version/"

# 🛠️ Configuração do ChromeOptions
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={user_data_dir}")  # Usa o diretório do Chrome
options.add_argument(f"--profile-directory={profile_directory}")  # Usa o perfil específico
options.add_experimental_option("detach", True)  # Mantém o Chrome aberto após execução

# 🚀 Inicializa o Chrome com o perfil correto
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Abre o Google para testar
driver.get("https://www.google.com")
time.sleep(5)  # Espera 5 segundos para visualizar

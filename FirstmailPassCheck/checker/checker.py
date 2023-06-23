import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

script_path = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.dirname(script_path)
os.chdir(folder_path)

config_name = "config.cfg"
config_path = os.path.join(folder_path, config_name)
config = {}

with open(config_path, "r") as file:
    for line in file:
        line = line.strip()
        if line:
            key, value = line.split("=")
            config[key.strip()] = value.strip()

file_name = config.get("file_name")
valid_file_name = config.get("valid_file_name")
new_passw = config.get("new_passw")
print("Буду менять пароли на: ", new_passw)
file_path = os.path.join(folder_path, file_name)
valid_file_path = os.path.join(folder_path, valid_file_name)
if not os.path.isfile(file_path):
    print("Ошибка: Файл не найден!")
    input("Нажмите Enter для выхода...")
    exit()

with open(file_path, "r") as file:
    accounts = file.readlines()

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

valid_accounts = []
nevalid_accounts = []

os.system('cls')


def change_pass(username, old_passw):
    driver.get("https://firstmail.ltd/webmail/settings")

    # Найти элементы для изменения пароля
    current_password_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="newPassword"]')))
    new_password_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="formAccountSettings"]/div[2]/div[1]/div/input')))
    confirm_password_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="formAccountSettings"]/div[2]/div[2]/div/input')))

    # Вставить текущий и новый пароли
    current_password_input.send_keys(old_passw)
    new_password_input.send_keys(new_passw)
    confirm_password_input.send_keys(new_passw)

    # Нажать на кнопку сохранения изменений
    save_changes_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="formAccountSettings"]/DIV[2]/DIV[4]/BUTTON[1]')))
    save_changes_button.click()
    print(f'{str(count) + ")"} {"Сменил пароль:   " + username}')


for count, account in enumerate(accounts, 1):
    while True:
        try:
            nevalid = False

            account_data = account.strip().split(":")
            username = account_data[0]
            old_passw = account_data[1]

            driver.get("https://firstmail.ltd/webmail/login")

            # Вход в аккаунт
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))).send_keys(
                username)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))).send_keys(
                old_passw)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="formAuthentication"]/div[3]/button'))).click()

            # проверка, вошел ли в аккаунт
            try:
                not_error = WebDriverWait(driver, 7).until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="__layout"]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/DIV[3]/DIV[1]/DIV[1]/A[1]/DIV[1]/DIV[2]/H6[1]')))
                if not_error:
                    valid_accounts.append(account)
                    print(f'{str(count) + ")"} {"Вошел в аккаунт:   " + username}')
                    change_pass(username, old_passw)
                    break
                    
            except:
                nevalid = True
                nevalid_accounts.append(account)

            if nevalid:
                raise

        except:
            break


driver.quit()

with open(valid_file_path, "w") as valid_file:
    for account in valid_accounts:
        valid_file.write(account)

nevalid_file_path = os.path.join(folder_path, "nevalid.txt")
with open(nevalid_file_path, "w") as nevalid_file:
    for account in nevalid_accounts:
        nevalid_file.write(account)

os.system('cls')

filename = valid_file_name

# Открыть файл для чтения
with open(filename, "r") as file:
    lines = file.readlines()

# Изменить строки
new_lines = [parts[0] + ":" + new_passw + "\n" for line in lines for parts in [line.split(":")]]


# Открыть файл для записи
with open(filename, "w") as file:
    file.writelines(new_lines)
print('============Проверка окончена!============')
print(f'Проверено {count} аккаунтов. ')
print(f'Валидных аккаунтов: {len(valid_accounts)} Сохранены в {valid_file_name}')
print(f'Невалидных аккаунтов: {count - len(valid_accounts)} Сохранены в nevalid.txt')
print('==========================================')

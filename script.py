import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# URL страницы входа
login_url = "https://hh.ru/"
# URL страницы резюме
resume_url = "https://hh.ru/applicant/resumes"

# print("Открывается страница:", login_url)

# Адрес электронной почты и пароль для входа
email = ""
password = ""

# Создание объекта опций Chrome
chrome_options = Options()
# Добавление опции, чтобы скрыть всплывающее окно Chrome при использовании драйвера в фоновом режиме
chrome_options.add_argument("--headless")
# Указание пути к драйверу
driver_path = "C:/chromedriver.exe"
# Инициализация драйвера Chrome с передачей объекта опций
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(30)



# Функция для входа на сайт
def login(driver):
    logging.info("Starting login process...")
    # Открытие страницы входа
    driver.get(login_url)
    logging.info("Opened login page")

    # Ждем, пока элементы не станут видимыми
    wait = WebDriverWait(driver, 30)
    wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    logging.info("Login page elements loaded")

    # Ввод адреса электронной почты и пароля
    email_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    email_input.send_keys(email)
    password_input.send_keys(password)

    logging.info("Email and password entered")

    # Нажатие кнопки "Войти"
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    logging.info("Login button clicked")

    # Ожидание перехода на страницу резюме
    wait.until(EC.url_to_be(resume_url))
    logging.info("Logged in successfully")


# Функция для поднятия резюме
def raise_resume(driver):
    logging.info("Starting resume raising process...")
    # Открытие страницы hh.ru
    driver.get(resume_url)
    logging.info("Opened resume page")

    # Ждем, пока элемент не станет видимым
    wait = WebDriverWait(driver, 10)
    try:
        last_update_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".applicant-resumes-action_second")))
    except TimeoutException:
        logging.error("Element with class 'applicant-resumes-action_second' not found")
        return

    # Получение текста времени последнего обновления резюме
    last_update_text = last_update_element.find_element(By.TAG_NAME, "span").text
    logging.info("Last update time: %s", last_update_text)

    # Определение времени следующего обновления
    next_update_time = time.strptime(last_update_text, "сегодня в %H:%M")
    next_update_time_plus_one_minute = time.mktime(next_update_time) + 60
    next_update_time_plus_one_minute = time.strftime("%H:%M", time.localtime(next_update_time_plus_one_minute))
    logging.info("Next update time plus one minute: %s", next_update_time_plus_one_minute)

    # Ожидание до времени следующего обновления
    current_time = time.strftime("%H:%M", time.localtime())
    while current_time != next_update_time_plus_one_minute:
        time.sleep(30)
        current_time = time.strftime("%H:%M", time.localtime())

    # Поднятие резюме
    raise_button = driver.find_element(By.CSS_SELECTOR, "button[data-qa='resume-update-button_actions']")
    raise_button.click()
    logging.info("Resume raised successfully at %s", current_time)


# Запуск скрипта
if __name__ == "__main__":
    try:
        login(driver)
        raise_resume(driver)
    except KeyboardInterrupt:
        logging.info("Script terminated by user")
    except TimeoutException:
        logging.error("Timeout occurred during login or resume raising")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        driver.quit()  # Закрываем браузер после завершения работы скрипта

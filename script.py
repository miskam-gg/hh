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

# Адрес электронной почты и пароль для входа
email = "your_email@example.com"
password = "your_password"

# Создание объекта опций Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
driver_path = "C:/chromedriver.exe"
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(30)

# Функция для входа на сайт
def login(driver):
    logging.info("Starting login process...")
    driver.get(login_url)
    logging.info("Opened login page")

    wait = WebDriverWait(driver, 30)
    try:
        wait.until(EC.visibility_of_element_located((By.NAME, "username")))
        logging.info("Login page elements loaded")

        email_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys(email)
        password_input.send_keys(password)
        logging.info("Email and password entered")

        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        logging.info("Login button clicked")

        wait.until(EC.url_contains("applicant/resumes"))
        logging.info("Logged in successfully")
    except TimeoutException:
        logging.error("Timeout occurred during login")
        raise
    except Exception as e:
        logging.error(f"An error occurred during login: {str(e)}")
        raise

# Функция для поднятия резюме
def raise_resume(driver):
    logging.info("Starting resume raising process...")
    driver.get(resume_url)
    logging.info("Opened resume page")

    wait = WebDriverWait(driver, 30)
    try:
        last_update_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".applicant-resumes-action_second span")))
        last_update_text = last_update_element.text
        logging.info(f"Last update time: {last_update_text}")

        next_update_time = time.strptime(last_update_text, "%H:%M")
        next_update_time_plus_one_minute = time.mktime(next_update_time) + 60
        next_update_time_plus_one_minute = time.strftime("%H:%M", time.localtime(next_update_time_plus_one_minute))
        logging.info(f"Next update time plus one minute: {next_update_time_plus_one_minute}")

        current_time = time.strftime("%H:%M", time.localtime())
        while current_time != next_update_time_plus_one_minute:
            time.sleep(30)
            current_time = time.strftime("%H:%M", time.localtime())

        raise_button = driver.find_element(By.CSS_SELECTOR, "button[data-qa='resume-update-button_actions']")
        raise_button.click()
        logging.info(f"Resume raised successfully at {current_time}")
    except TimeoutException:
        logging.error("Timeout occurred during resume raising")
        raise
    except Exception as e:
        logging.error(f"An error occurred during resume raising: {str(e)}")
        raise

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
        driver.quit()

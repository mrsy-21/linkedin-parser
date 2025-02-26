import logging
from random import randint
import time
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
from time import sleep
from random import uniform


load_dotenv()
username = os.getenv("LINKEDIN_USER")
password = os.getenv("LINKEDIN_PASS")


class Parser:
    """Клас Parser для авторизації на LinkedIn, отримання cookies та завантаження фото профілю.

    Атрибути:
        - login_url : str
            URL сторінки входу в LinkedIn.
        - headers_dict : dict
            Заголовки HTTP-запитів для імітації браузера.

    """

    headers_dict = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.linkedin.com/",
        "Host": "www.linkedin.com",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Origin": "https://www.linkedin.com",
        "DNT": "1",
        "Sec-GPC": "1",
        "Cookie": "",
    }

    def __init__(self, login_url: str) -> None:
        """Конструктор класу. Ініціалізує логування та веб-драйвер"""

        self.login_url = login_url
        self._setup_logger()
        self._init_driver()

    def _setup_logger(self) -> None:
        """Ініціалізує логування для відстеження процесу парсингу.

        Логи зберігаються у файлі 'logs/out.info'
        """

        logging.basicConfig(
            filename="logs/out.log",
            filemode="w",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        logging.info("Logger initialization was successful")

    def _init_driver(self) -> None:
        """Ініціалізує браузерний драйвер Chrome за допомогою undetected-chromedriver.

        Є можливість працювати в headless-режимі.
        """
        options = webdriver.ChromeOptions()
        options.binary_location = "/usr/bin/chromium"
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Якщо потрібен headless-режим:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")

        service = Service("/usr/bin/chromedriver")
        self.driver = webdriver.Chrome(service=service, options=options)
        logging.info("Undetected Chromium driver successfully initialized")

    def _find_element(self, by, value, timeout=10) -> EC.WebElement:
        """Пошук елемента на сторінці з очікуванням

        Параметри:
            - by : selenium.webdriver.common.by.By
                Тип селектора (ID, CLASS_NAME, XPATH, тощо).
            - value : str
                Значення селектора.
            - timeout : int, optional
                Час очікування в секундах (за замовчуванням 10).

        Повертає:
            - WebElement
                Знайдений веб-елемент або викликає TimeoutException.
        """

        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def _check_for_captcha(self) -> None:
        """Перевіряє наявність капчі та очікує ручного розв’язання, якщо вона є."""
        try:
            captcha = self.driver.find_element(By.ID, "captcha-internal")
            if captcha:
                logging.warning("CAPTCHA detected. Manual intervention required.")
                input("Solve the CAPTCHA in the browser and press Enter to continue...")
                logging.info("CAPTCHA resolved. Continuing execution.")
        except:
            logging.info("No CAPTCHA detected. Continuing execution.")

    def random_scroll(self, times=3) -> None:
        """Виконує випадкове прокручування сторінки для імітації поведінки користувача.

        Параметри:
            - times : int, optional
                Кількість прокручувань (за замовчуванням 3).
        """

        for _ in range(times):
            scroll_height = randint(100, 800)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_height});")
            time.sleep(randint(2, 6))

    def human_typing(self, element, text) -> None:
        """Імітує введення тексту користувачем, вводячи символи по одному з випадковою затримкою."""
        for char in text:
            element.send_keys(char)
            sleep(uniform(0.1, 0.3))

    def login(self, username: str, password: str) -> None:
        """Виконує логін на LinkedIn, використовуючи вказані логін та пароль.

        Параметри:
            - username : str
                Ім'я користувача (email або логін LinkedIn).
            - password : str
                Пароль користувача.
        """

        logging.info("Navigating to the login page.")
        self.driver.get(self.login_url)
        self.random_scroll(1)

        self.driver.delete_all_cookies()
        logging.info("Cookies cleared before login attempt.")

        logging.info("Attempting to enter username and password.")
        try:
            username_input = self.driver.find_element(By.ID, "username")
            self.human_typing(username_input, username)

            password_input = self.driver.find_element(By.ID, "password")
            self.human_typing(password_input, password)

            sign_in_button = self.driver.find_element(
                By.XPATH, '//button[@type="submit"]'
            )
            sign_in_button.click()

            self._check_for_captcha()
        except Exception as e:
            logging.error(f"An error occurred during login.: {e}")
        self.random_scroll(2)

        if "feed" in self.driver.current_url:
            logging.info("Login successful.")
        else:
            logging.error("Login failed.")
            raise Exception("Login failed.")

    def update_cookie(self) -> None:
        """Оновлює cookies після авторизації для подальшого використання у HTTP-запитах."""

        logging.info("Attempting to retrieve cookies....")
        cookies = self.driver.get_cookies()
        cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        self.headers_dict["cookie"] = cookie_string
        logging.info(f"Cookies updated.")

    def parse_profile_photo(self, save_path: str = "profile_photo.jpg") -> None:
        """Завантажує та зберігає фото профілю користувача LinkedIn.

        Параметри:
            - save_path : str, optional
                Шлях для збереження фото (за замовчуванням 'profile_photo.jpg').
        """

        try:
            logging.info("Searching for profile photo on the homepage....")
            profile_photo_element = self._find_element(
                By.CLASS_NAME, "profile-card-profile-picture"
            )

            self.random_scroll(3)

            photo_url = profile_photo_element.get_attribute("src")
            logging.info(f"Profile photo found, attempting to download: {photo_url}")

            headers = {
                "User-Agent": self.headers_dict["User-Agent"],
                "Referer": "https://www.linkedin.com/",
                "Cookie": self.headers_dict.get("cookie", ""),
            }

            response = requests.get(photo_url, headers=headers)
            self.random_scroll(2)
            if response.status_code == 200:
                with open(save_path, "wb") as file:
                    file.write(response.content)
                logging.info(f"Profile photo successfully saved at: {save_path}")
            else:
                logging.error(
                    f"Failed to download profile photo. Status code: {response.status_code}, Response: {response.text}"
                )

        except Exception as e:
            logging.error(f"Error occurred while parsing profile photo: {e}")

    def close(self) -> None:
        """Закриває браузерний драйвер для звільнення ресурсів."""

        logging.info("Closing the browser driver.")
        self.driver.quit()


if __name__ == "__main__":
    parser = Parser("https://www.linkedin.com/checkpoint/lg/sign-in-another-account")
    try:
        parser.login(username, password)
        parser.update_cookie()
        parser.parse_profile_photo()
    finally:
        parser.close()

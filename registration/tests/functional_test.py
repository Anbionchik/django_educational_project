import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as es
from selenium.webdriver.common.by import By
# from .conftest import TEST_CLIENT

TEST_CLIENT = {
    'username': 'TestUser',
    'email': '123@123.ru',
    'password': 'q1w2e3r4TT',
}


def test_open_login_page(live_server, new_client):
    """
    Новый пользователь Юля, открывает
    браузер и решает ввести 'http://127.0.0.1:8000/'.
    Попадает на страницу с title 'Войти' и заголовком
    И надписью ВХОД
    """
    browser = webdriver.Chrome(
        executable_path=
        r"C:\Users\Андрей\PycharmProjects\Khlopkov\Khlopkov\chromedriver.exe"
    )
    browser.get(live_server.url)
    assert browser.title == 'Войти'
    login = browser.find_element_by_name('login')
    password = browser.find_element_by_name('password')
    login.send_keys(TEST_CLIENT['username'])
    password.send_keys(TEST_CLIENT['password'])

    button = browser.find_element_by_id('login-submit-btn')
    button.click()

    time.sleep(3)
    assert browser.title == 'Главная'

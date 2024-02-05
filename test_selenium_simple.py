import time
from selenium.webdriver.common.by import By
from selenium import webdriver
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()

def test_petfriends(driver):
    # Open PetFriends base page:
    driver.get("https://petfriends.skillfactory.ru/")

    time.sleep(3)

    # click on the new user button
    btn_newuser = driver.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()

    # click user button
    btn_exist_acc = driver.find_element(By.LINK_TEXT, u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    # add email
    field_email = driver.find_element(By.ID, "email")
    field_email.clear()
    field_email.send_keys("kidsuper@email.ru")

    # add password
    field_pass = driver.find_element(By.ID, "pass")
    field_pass.clear()
    field_pass.send_keys("yakish")

    # click submit button
    btn_submit = driver.find_element(By.XPATH, "//button[@type='submit']")
    btn_submit.click()

    time.sleep(3)

    assert driver.current_url == 'https://petfriends.skillfactory.ru/all_pets', "login error"

def test_show_all_pets(driver):
    # Устанавливаем неявное ожидание в 10 секунд
    driver.implicitly_wait(10)
    # Open PetFriends base page:
    driver.get("https://petfriends.skillfactory.ru/login")
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('kidsuper@email.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('yakish')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    #Переходим в раздел Мои Питомцы
    driver.find_element(By.CSS_SELECTOR,'a.nav-link[href="/my_pets"]').click()

    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') is not None and images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''

        assert ', ' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
    # Убираем неявное ожидание после завершения теста
    driver.implicitly_wait(0)

def test_show_my_pets(driver):
    driver.find_element(By.ID, 'email').send_keys('kidsuper@email.ru')
    driver.find_element(By.ID, 'pass').send_keys('yakish')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))
    time.sleep(2)

    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    time.sleep(2)
    driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()
    # Явное ожидание видимости элемента с количеством питомцев
    pets_number_element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]'))
    )

    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    # Явное ожидание видимости элементов таблицы
    pets_count = WebDriverWait(driver, 5).until(
        EC.visibility_of_all_elements_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr'))
    )

    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    assert int(pets_number) == len(pets_count)

import uuid
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver_args():
    return ['--log-level=LEVEL']

@pytest.fixture()
def driver():
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service)
    driver.maximize_window()
    yield driver
    driver.save_screenshot('result.png')
    driver.quit()

@pytest.fixture
def web_browser(request, driver):

    browser = driver
    browser.set_window_size(1400, 1000)

    # Вернуть объект браузера
    yield browser

    # Этот код выполнится после отрабатывания теста:
    if request.node.rep_call.failed:
        # Сделать скриншот, если тест провалится:
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            # Создаем папку screenshots и кладем туда скриншот с генерированным именем:
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

            # Для дебагинга, печатаем информацию в консоль
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # Детект упавших тестов
    # Тирдаун

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep

@pytest.fixture
def web_browser(request, selenium):

    browser = selenium
    browser.set_window_size(1400, 1000)

    # Return browser instance to test case:
    yield browser

    # Тирдаун

    if request.node.rep_call.failed:
        # Используем данные из request.node.rep_call.failed для распознавания того, успешно ли прошёл тест.
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            # Make screen-shot for local debug:
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

            # For happy debugging:
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass # just ignore any errors here
from api import Petfriends
from settings import valid_email, valid_password
import os
import pytest

pf = Petfriends()


@pytest.fixture(scope='session')
def token():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    return auth_key

# GET API_KEY:
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email,password)
    assert status == 200
    assert 'key' in result
#Негативные тесты Email/Password:

    def test_invalid_email_for_api_key():
        status, result = pf.get_api_key("invalid_email@example.com", valid_password)
        assert status == 401

    def test_invalid_password_for_api_key():
        status, result = pf.get_api_key(valid_email, "invalid_password")
        assert status == 401


#GET Список питомцев с валидными данными входа
def test_get_all_pets_with_valid_key(token, filter=''):
    status, result = pf.get_list_of_pets(token, filter)
    assert status == 200
    assert len(result['pets']) > 0

#Негативные: Неверный ключ/неверный фильтр

def test_invalid_key_for_all_pets():
    status, result = pf.get_list_of_pets("invalid_key", "")
    assert status == 403

def test_invalid_filter_for_all_pets():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, "invalid_filter")
    assert status == 200
    assert len(result['pets']) == 0


# POST Добавление нового питомца:


def test_add_new_pet_with_valid_data(token):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    #    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key

    name = 'Матроскин'
    animal_type = 'Боевой кот'
    age = '4'
    pet_photo = 'C:\\Users\KiDsuper\PycharmProjects\RestfulTests\Tests\images\cat.jpg'

    # Добавляем питомца
    status, result = pf.add_new_pet(token,name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

#Негативные тесты:Отсутствие параметра возраст и Добавление питомца с некорректным типом животного:

def test_missing_required_parameter_for_add_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, "Fluffy", "Cat", "", "path/to/image.jpg")
    assert status == 400

def test_invalid_animal_type_for_add_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, "Buddy", "InvalidType", "3", "path/to/image.jpg")
    assert status == 400


# DELETE Удаление питомца
def test_delete_pet(token):
    name = 'Боба'
    animal_type = 'двортербул'
    age = '1'
    pet_photo = 'C:\\Users\KiDsuper\PycharmProjects\RestfulTests\Tests\images\cat.jpg'

    status, result =pf.add_new_pet(token,name,animal_type,age,pet_photo)
    assert status==200
    petid = result['id']

#Негативные: Удаление несуществующего питомца(404) и Удаление питомца без прав доступа(403):

    def test_delete_nonexistent_pet():
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.delete_pet(auth_key, "nonexistent_pet_id")
        assert status == 404

    def test_delete_pet_without_access():
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, result = pf.add_new_pet(auth_key, "Fido", "Dog", "2", "path/to/image.jpg")
        status, _ = pf.delete_pet("invalid_key", result['id'])
        assert status == 403

    status, result =pf.delete_pet(auth_key=token,pet_id=petid)
    assert status==200

# PUT обновление информации о питомце :

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


#Негативные: Обновление информации о несуществующем питомце(404) и Обновление информации без указания обязательных параметров(400)

    def test_update_nonexistent_pet_info():
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, _ = pf.update_pet_info(auth_key, "nonexistent_pet_id", "UpdatedName", "UpdatedType", "UpdatedAge")
        assert status == 404

    def test_update_pet_info_missing_required_parameters():
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        if len(my_pets['pets']) > 0:
            pet_id = my_pets['pets'][0]['id']
            status, _ = pf.update_pet_info(auth_key, pet_id, "", "", "")
            assert status == 400
        else:
            raise Exception("There is no my pets")


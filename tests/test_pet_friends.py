from api import PetFriends
from settings import valid_email, valid_password
import os
import pytest

pf = PetFriends()

def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_list_of_pets_with_valid_user(filter = ""):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

class TestPetFriends:
    def setup_method(self):
        self.pf = PetFriends()
        self.email = valid_email
        self.password = valid_password
        self.auth_key = self.pf.get_api_key(self.email, self.password)[1]

    def test_add_new_pet_valid(self):
        """Позитивный тест: добавление нового питомца с валидными данными"""
        status, result = self.pf.add_new_pet(self.auth_key, 'Бармалей', 'Панда', '4', 'images/_102609291_animals7.jpg')
        assert status == 200
        assert 'Барсик' in result['name']

    def test_add_new_pet_invalid(self):
        """Негативный тест: добавление питомца с отсутствующим полем имени"""
        status, result = self.pf.add_new_pet(self.auth_key, '', 'Панда', '4', 'images/_102609291_animals7.jpg')
        assert status == 400  # Ожидаем ошибку 400
        assert 'name' in result['message']  # Ожидаем сообщение об ошибке

    def test_delete_pet_valid(self):
        """Позитивный тест: удаление питомца"""
        pet_id = self.pf.get_list_of_pets(self.auth_key, '')[1]['pets'][0][
            'id']  # Предполагаем, что существует хотя бы один питомец
        status = self.pf.delete_pet(self.auth_key, pet_id)
        assert status == 200

    def test_delete_pet_invalid(self):
        """Негативный тест: попытка удалить питомца с несуществующим ID"""
        status = self.pf.delete_pet(self.auth_key, 'invalid_id')
        assert status == 404  # Ожидаем ошибку 404

    def test_add_photo_to_pet_valid(self):
        """Позитивный тест: добавление фото к питомцу"""
        pet_id = self.pf.get_list_of_pets(self.auth_key, '')[1]['pets'][0]['id']
        status, result = self.pf.add_photo_to_pet(self.auth_key, pet_id, 'images/_102609291_animals7.jpg')
        assert status == 200
        assert 'pet_photo' in result  # Предполагаем, что ответ содержит поле pet_photo

    def test_add_photo_to_pet_invalid(self):
        """Негативный тест: добавление фото к питомцу с несуществующим ID"""
        status, result = self.pf.add_photo_to_pet(self.auth_key, 'invalid_id', 'images/_102609291_animals7.jpg')
        assert status == 404  # Ожидаем ошибку 404

    def test_update_pet_info_valid(self):
        """Позитивный тест: обновление информации о питомце"""
        pet_id = self.pf.get_list_of_pets(self.auth_key, '')[1]['pets'][0]['id']
        status, result = self.pf.update_pet_info(self.auth_key, pet_id, 'Ричи', 'Собака', '5')
        assert status == 200
        assert result['name'] == 'Том'

    def test_update_pet_info_invalid(self):
        """Негативный тест: обновление информации о питомце с несуществующим ID"""
        status, result = self.pf.update_pet_info(self.auth_key, 'invalid_id', 'Ричи', 'Собака', '5')
        assert status == 404  # Ожидаем ошибку 404








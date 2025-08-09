import os
import pytest
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

@pytest.mark.skipif(valid_email == "your_email@example.com", reason="Set valid_email in settings.py")
def test_get_api_key_for_valid_user():
    status, result = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in result

@pytest.mark.skipif(valid_email == "your_email@example.com", reason="Set valid_email in settings.py")
def test_get_all_pets_with_valid_key():
    status, auth = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    status, result = pf.get_list_of_pets(auth['key'])
    assert status == 200
    assert isinstance(result.get('pets', []), list)

@pytest.mark.skipif(valid_email == "your_email@example.com", reason="Set valid_email in settings.py")
def test_add_pet_without_photo():
    _, auth = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth['key'], "TestPet", "cat", "2")
    assert status == 200
    assert result.get('name') == "TestPet"

@pytest.mark.skipif(valid_email == "your_email@example.com", reason="Set valid_email in settings.py")
def test_add_pet_with_photo_if_exists():
    _, auth = pf.get_api_key(valid_email, valid_password)
    image_path = os.path.join(os.path.dirname(__file__), "../images/cat.jpg")
    if not os.path.exists(image_path):
        pytest.skip("Image not present — skipping upload test")
    status, result = pf.add_new_pet(auth['key'], "PhotoPet", "dog", "3", image_path)
    assert status == 200
    assert result.get('name') == "PhotoPet"

@pytest.mark.skipif(valid_email == "your_email@example.com", reason="Set valid_email in settings.py")
def test_update_pet_info():
    _, auth = pf.get_api_key(valid_email, valid_password)
    status, pets_res = pf.get_list_of_pets(auth['key'])
    pets = pets_res.get('pets', [])
    if not pets:
        pytest.skip("No pets available to update")
    pet_id = pets[0]['id']
    status, result = pf.update_pet_info(auth['key'], pet_id, "NewName", "cat", "5")
    assert status == 200
    assert result.get('name') == "NewName"

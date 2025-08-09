import os
import pytest
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

# 1. Invalid credentials
def test_get_api_key_invalid_credentials():
    status, result = pf.get_api_key("wrong@example.com", "nope")
    assert status in (403, 401, 400)

# 2. Invalid auth key for listing pets
def test_get_pets_invalid_key():
    status, result = pf.get_list_of_pets("invalid_key_123")
    assert status in (403, 401, 400)

# 3. Add pet with empty name
@pytest.mark.skipif(valid_email == "your_email@example.com", reason="Set valid_email in settings.py")
def test_add_pet_empty_name():
    _, auth = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth['key'], "", "dog", "3")
    assert status in (400, 422)

# 4. Add pet with negative age
@pytest.mark.skipif(valid_email == "your_email@example.com", reason="Set valid_email in settings.py")
def test_add_pet_negative_age():
    _, auth = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth['key'], "NegAge", "cat", "-5")
    assert status in (400, 422)

# 5. Add pet with enormous age
@pytest.mark.skipif(valid_email == "your_email@example.com", reason="Set valid_email in settings.py")
def test_add_pet_huge_age():
    _, auth = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth['key'], "Oldie", "turtle", "9999999999")
    assert status in (400, 422)

# 6. Delete pet with invalid id
@pytest.mark.skipif(valid_email == "your_email@example.com", reason="Set valid_email in settings.py")
def test_delete_pet_invalid_id():
    _, auth = pf.get_api_key(valid_email, valid_password)
    status, result = pf.delete_pet(auth['key'], "wrong_id_123")
    assert status in (400, 404)

# 7. Update pet info with invalid id
@pytest.mark.skipif(valid_email == "your_email@example.com", reason="Set valid_email in settings.py")
def test_update_invalid_pet_id():
    _, auth = pf.get_api_key(valid_email, valid_password)
    status, result = pf.update_pet_info(auth['key'], "nope_id", "Name", "type", "1")
    assert status in (400, 404)

# 8. Add photo with invalid pet id
@pytest.mark.skipif(valid_email == "your_email@example.com", reason="Set valid_email in settings.py")
def test_add_photo_invalid_pet():
    _, auth = pf.get_api_key(valid_email, valid_password)
    image_path = os.path.join(os.path.dirname(__file__), "../images/cat.jpg")
    if not os.path.exists(image_path):
        pytest.skip("Image not present — skipping")
    status, result = pf.add_photo_to_pet(auth['key'], "invalid_id_123", image_path)
    assert status in (400, 404)

# 9. Try using missing auth header in add pet
def test_add_pet_missing_auth():
    # call API client directly with blank key
    status, result = pf.add_new_pet_simple("", "NoAuth", "cat", "2")
    assert status in (403, 401, 400)

# 10. Request with invalid filter param
@pytest.mark.skipif(valid_email == "your_email@example.com", reason="Set valid_email in settings.py")
def test_get_pets_with_invalid_filter():
    _, auth = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth['key'], filter="invalid_filter_value_!@#")
    assert status in (400, 200)  # some servers ignore invalid filters, accept both

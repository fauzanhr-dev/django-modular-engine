import pytest

pytestmark = pytest.mark.django_db

def test_superuser_can_open_module_manager(client, superuser, module_installed, module_list_url):
    client.force_login(superuser)
    r = client.get(module_list_url)
    assert r.status_code == 200
    assert "Module Manager" in r.content.decode()

def test_non_superuser_redirected_from_module_manager(client, user_member, module_installed, module_list_url, access_choose_url):
    client.force_login(user_member)
    r = client.get(module_list_url)
    assert r.status_code == 302
    assert access_choose_url in r["Location"]

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

def test_anonymous_can_view_only(client, module_installed, product, product_list_url):
    r = client.get(product_list_url)
    assert r.status_code == 200
    html = r.content.decode()
    assert product.name in html
    assert "Add Product" not in html
    assert "Edit" not in html
    assert "Delete" not in html

def test_user_group_sees_add_and_edit(client, user_member, module_installed, product, product_list_url):
    client.force_login(user_member)
    r = client.get(product_list_url)
    html = r.content.decode()
    assert "Add Product" in html
    assert "Edit" in html
    assert "Delete" not in html

def test_manager_sees_delete(client, user_manager, module_installed, product, product_list_url):
    client.force_login(user_manager)
    r = client.get(product_list_url)
    html = r.content.decode()
    assert "Add Product" in html
    assert "Edit" in html
    assert "Delete" in html

def test_delete_view_is_protected(client, user_member, module_installed, product):
    client.force_login(user_member)
    url = reverse("product_module:product_delete", args=[product.pk])
    r_get = client.get(url)
    assert r_get.status_code in (302, 403)
    r_post = client.post(url, data={"post": "yes"})
    assert r_post.status_code in (302, 403)

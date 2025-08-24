import pytest
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from product_module.models import Product
from engine_modular.services import discover_manifests, install_app

User = get_user_model()

# ---------- Factories ----------

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    is_active = True
    is_staff = False
    is_superuser = False
    password = factory.PostGenerationMethodCall("set_password", "pass12345")

class SuperuserFactory(UserFactory):
    is_staff = True
    is_superuser = True

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    barcode = factory.Sequence(lambda n: f"BC{1000+n}")
    price = "99.99"
    stock = 5

# ---------- Shared fixtures ----------

@pytest.fixture
def module_installed(db):
    """
    Ensure product_module exists in DB registry and is installed
    (sets is_installed, runs migrations, creates groups & perms).
    """
    discover_manifests()
    install_app("product_module")

@pytest.fixture
def superuser(db):
    return SuperuserFactory()

@pytest.fixture
def user_member(db, module_installed):
    """User group (CRU)"""
    u = UserFactory()
    grp, _ = Group.objects.get_or_create(name="user")
    u.groups.add(grp)
    return u

@pytest.fixture
def user_manager(db, module_installed):
    """Manager group (CRUD)"""
    u = UserFactory()
    grp, _ = Group.objects.get_or_create(name="manager")
    u.groups.add(grp)
    return u

@pytest.fixture
def product(db, module_installed):
    return ProductFactory()

@pytest.fixture
def product_list_url():
    return reverse("product_module:product_list")

@pytest.fixture
def module_list_url():
    return reverse("engine_modular:module_list")

@pytest.fixture
def access_choose_url():
    return reverse("engine_modular:access_choose")

@pytest.fixture
def login_url():
    return reverse("login")

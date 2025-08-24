from importlib import import_module
from django.apps import apps as django_apps
from django.utils import timezone
from django.core.management import call_command
from django.core.management.base import CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Module
from django.conf import settings

# --- discovery / registry (writes to DB) ---------------------------------

def register_manifest(manifest: dict):
    key = manifest["key"]
    defaults = {
        "title": manifest.get("title", key),
        "landing_url_name": manifest.get("landing_url_name"),
        # installed_version is set on install/upgrade
    }
    Module.objects.update_or_create(key=key, defaults=defaults)

def discover_manifests():
    for app_cfg in django_apps.get_app_configs():
        try:
            mod = import_module(app_cfg.name)
            manifest = getattr(mod, "MODULAR_MANIFEST", None)
            if isinstance(manifest, dict) and "key" in manifest:
                register_manifest(manifest)
        except Exception:
            continue

def _get_row_or_raise(key: str) -> Module:
    discover_manifests()
    try:
        return Module.objects.get(key=key)
    except Module.DoesNotExist:
        raise RuntimeError(
            f"Unknown module '{key}'. Ensure the app is in INSTALLED_APPS and "
            f"defines MODULAR_MANIFEST, or create a Module row via Admin."
        )

def _manifest_version(key: str) -> str | None:
    """Read current code version from the app manifest (or __version__)."""
    try:
        mod = import_module(key)
        manifest = getattr(mod, "MODULAR_MANIFEST", {}) or {}
        return manifest.get("version") or getattr(mod, "__version__", None)
    except Exception:
        return None

# --- safe wrappers --------------------------------------------------------

def _safe_makemigrations(app_label: str):
    try:
        call_command("makemigrations", app_label, interactive=False, verbosity=0)
    except (SystemExit, CommandError) as e:
        raise RuntimeError(
            f"makemigrations aborted for '{app_label}'. Add default/null=True or create the migration manually."
        ) from e

def _safe_migrate(app_label: str, target: str | None = None):
    try:
        if target is None:
            call_command("migrate", app_label, interactive=False, verbosity=0)
        else:
            call_command("migrate", app_label, target, interactive=False, verbosity=0)
    except (SystemExit, CommandError) as e:
        raise RuntimeError(f"migrate failed for '{app_label}': {e}") from e

# --- product_module perms -------------------------------------------------

def _apply_product_permissions():
    try:
        from product_module.models import Product
    except Exception:
        return
    ct = ContentType.objects.get_for_model(Product)
    perms = {p.codename: p for p in Permission.objects.filter(content_type=ct)}
    manager, _ = Group.objects.get_or_create(name="manager")
    user, _ = Group.objects.get_or_create(name="user")
    manager.permissions.set([p for c,p in perms.items() if c in {"add_product","change_product","delete_product","view_product"}])
    user.permissions.set([p for c,p in perms.items() if c in {"add_product","change_product","view_product"}])

# --- core actions (DB-only) -----------------------------------------------

def install_app(key: str):
    row = _get_row_or_raise(key)
    _safe_migrate(key)
    if key == "product_module":
        _apply_product_permissions()
    row.is_installed = True
    row.installed_version = _manifest_version(key)  # write the current code version
    row.installed_at = timezone.now()
    row.save(update_fields=["is_installed","installed_version","installed_at"])

def upgrade_app(key: str):
    row = _get_row_or_raise(key)
    if settings.DEBUG:
        _safe_makemigrations(key)
    _safe_migrate(key)
    if key == "product_module":
        _apply_product_permissions()
    row.installed_version = _manifest_version(key)
    row.save(update_fields=["installed_version"])

def uninstall_app(key: str):
    _safe_migrate(key, "zero")
    Module.objects.filter(key=key).update(is_installed=False)

# engine_modular/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Module
from .services import discover_manifests, install_app, upgrade_app, uninstall_app


class AccessChooserView(View):
    template_name = "engine_modular/access_choose.html"

    def get(self, request):
        installed_modules = Module.objects.filter(is_installed=True)
        options = []

        for module in installed_modules:
            links = [
                {
                    "label": "View Page",
                    "url": reverse(module.landing_url_name),
                    "show": True,
                }
            ]
            options.append({"title": module.title, "links": links})

        return render(request, self.template_name, {"options": options})


class ModuleListView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "login"
    template_name = "engine_modular/module_list.html"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect("engine_modular:access_choose")

    def get(self, request):
        discover_manifests()
        modules = Module.objects.order_by("key")
        return render(request, "engine_modular/module_list.html", {"modules": modules})


@login_required
def do_install(request, key):
    if not request.user.is_superuser:
        return redirect("engine_modular:access_choose")
    try:
        install_app(key)
        messages.success(request, f"{key} installed.")
    except Exception as e:
        messages.error(request, f"Install failed: {e}")
    return redirect("engine_modular:module_list")


@login_required
def do_upgrade(request, key):
    if not request.user.is_superuser:
        return redirect("engine_modular:access_choose")
    try:
        upgrade_app(key)
        messages.success(request, f"{key} upgraded.")
    except Exception as e:
        messages.error(request, f"Upgrade failed: {e}")
    return redirect("engine_modular:module_list")


@login_required
def do_uninstall(request, key):
    if not request.user.is_superuser:
        return redirect("engine_modular:access_choose")
    try:
        uninstall_app(key)
        messages.success(request, f"{key} uninstalled.")
    except Exception as e:
        messages.error(request, f"Uninstall failed: {e}")
    return redirect("engine_modular:module_list")

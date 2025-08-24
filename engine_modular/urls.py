from django.urls import path
from .views import ModuleListView, AccessChooserView, do_install, do_upgrade, do_uninstall


app_name = 'engine_modular'


urlpatterns = [
    path('', ModuleListView.as_view(), name='module_list'),
    path('access/', AccessChooserView.as_view(), name='access_choose'),
    path('install/<str:key>/', do_install, name='module_install'),
    path('upgrade/<str:key>/', do_upgrade, name='module_upgrade'),
    path('uninstall/<str:key>/', do_uninstall, name='module_uninstall'),
]
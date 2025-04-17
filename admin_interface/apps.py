from django.apps import AppConfig
from django.contrib import admin

from admin_interface.admin import AdminInterface

 

class AdminInterfaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_interface'

    def ready(self):
        # Import here to avoid AppRegistryNotReady error
        # from django.contrib import admin
        # admin.site = AdminInterface(name='admin')

  
        # Create new admin instance
        new_admin = AdminInterface(name='admin')

        # Copy existing registrations from default admin
        new_admin._registry = admin.site._registry.copy()

        # Replace default admin
        admin.site = new_admin

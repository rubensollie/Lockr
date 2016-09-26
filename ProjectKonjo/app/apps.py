from django.apps import AppConfig
class LockerAppConfig(AppConfig):
    name = 'app'
    verbose_name = 'locker'
    
    def ready(self):
        print("Ready")
        pass
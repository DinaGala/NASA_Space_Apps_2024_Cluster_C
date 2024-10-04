from django.contrib import admin

# Register your models here.
# Permet gestionar els usuaris desde la interficie d'admin de Django

#from .models import App_back
from .models import Usuario

#admin.site.register(App_back)
admin.site.register(Usuario)
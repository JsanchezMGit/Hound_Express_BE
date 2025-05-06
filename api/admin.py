from django.contrib import admin

from .models import Guia, Usuario, Estatus

admin.site.register(Guia)
admin.site.register(Usuario)
admin.site.register(Estatus)
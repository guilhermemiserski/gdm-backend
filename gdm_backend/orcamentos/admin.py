from django.contrib import admin
from .models import Cliente, Item, Orcamento

admin.site.register(Cliente)
admin.site.register(Orcamento)
admin.site.register(Item)
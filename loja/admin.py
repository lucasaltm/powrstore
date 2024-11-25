from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Categoria, Produto, Pedido, ItemPedido

class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}

admin.site.register(Usuario, UserAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(ItemPedido)

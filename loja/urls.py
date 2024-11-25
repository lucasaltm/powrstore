from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('categoria/<slug:categoria_slug>/', views.lista_produtos, name='produtos_por_categoria'),
    path('login/', views.usuario_login, name='login'),
    path('logout/', views.usuario_logout, name='logout'),
    path('', views.lista_produtos, name='lista_produtos'),
    path('produto/<int:produto_id>/', views.detalhe_produto, name='detalhe_produto'),
    path('add_carrinho/<int:produto_id>/', views.add_carrinho, name='add_carrinho'),
    path('remover_carrinho/<int:produto_id>/', views.remover_carrinho, name='remover_carrinho'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('checkout/', views.checkout, name='checkout'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
]

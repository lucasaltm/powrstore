from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Produto, Categoria, Pedido, ItemPedido
from django.urls import reverse

def usuario_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['password']
        user = authenticate(request, username=username, password=senha)
        if user:
            login(request, user)
            return redirect('lista_produtos')
        else:
            return render(request, 'login.html', {'erro': 'Credenciais inválidas'})
    return render(request, 'login.html')

def usuario_logout(request):
    logout(request)
    return redirect('login')

def lista_produtos(request):
    categorias = Categoria.objects.all()
    categoria_selecionada = None
    produtos = Produto.objects.all()

    categoria_slug = request.GET.get('categoria')
    if categoria_slug:
        categoria_selecionada = get_object_or_404(Categoria, slug=categoria_slug)
        produtos = produtos.filter(categoria=categoria_selecionada)

    context = {
        'categorias': categorias,
        'produtos': produtos,
        'categoria_selecionada': categoria_selecionada,
    }
    return render(request, 'lista_produtos.html', context)


def detalhe_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    return render(request, 'detalhe_produto.html', {'produto': produto})

def add_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    quantidade = int(request.POST.get('quantidade', 1))
    carrinho[produto_id] = carrinho.get(produto_id, 0) + quantidade
    request.session['carrinho'] = carrinho
    return redirect('carrinho')

def remover_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    if str(produto_id) in carrinho:
        del carrinho[str(produto_id)]
    request.session['carrinho'] = carrinho
    return redirect('carrinho')

def carrinho(request):
    carrinho = request.session.get('carrinho', {})
    itens = []
    total = 0
    for produto_id, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, id=produto_id)
        subtotal = produto.preco * quantidade
        total += subtotal
        itens.append({'produto': produto, 'quantidade': quantidade, 'subtotal': subtotal})
    return render(request, 'carrinho.html', {'itens': itens, 'total': total})

@login_required
def checkout(request):
    if request.method == 'POST':
        forma_pagamento = request.POST['forma_pagamento']
        carrinho = request.session.get('carrinho', {})
        if not carrinho:
            return redirect('lista_produtos')
        pedido = Pedido.objects.create(usuario=request.user, forma_pagamento=forma_pagamento)
        for produto_id, quantidade in carrinho.items():
            produto = get_object_or_404(Produto, id=produto_id)
            ItemPedido.objects.create(pedido=pedido, produto=produto, quantidade=quantidade)
        request.session['carrinho'] = {}
        return redirect('lista_pedidos')
    return render(request, 'checkout.html')

@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, 'lista_pedidos.html', {'pedidos': pedidos})

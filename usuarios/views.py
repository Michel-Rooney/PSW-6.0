from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.contrib import auth


def cadastro(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.error(request, 'Não pode acessar está pagina estando logado.')
            return redirect('/eventos/novo_evento/')

        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if not password == confirm_password:
            messages.error(request, 'As senhas não coicidem.')
            return redirect(reverse('cadastro'))
        
        #TODO: Validar a força da senha

        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            messages.error(request, 'Esse usuário já existe.')
            return redirect(reverse('cadastro'))

        user = User.objects.create_user(username, email, password)
        user.save()
        messages.success(request, 'Usuário criado com sucesso')
        return redirect('/usuarios/login/')
    
def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            messages.error(request, 'Não pode acessar está pagina estando logado.')
            return redirect('/eventos/novo_evento/')
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if not user:
            messages.error(request, 'Username ou senha inválidos')
            return redirect(reverse('login'))
        
        auth.login(request, user)
        return redirect('/eventos/novo_evento/')
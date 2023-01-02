from django.shortcuts import render
from passagens.forms import PassagemForms

def index(request):
    form = PassagemForms()
    contexto = {
        'form': form
    }
    return render(request, 'index.html', context=contexto)

def revisao_consulta(request):
    if request.method == 'POST':
        form = PassagemForms(request.POST)
        if form.is_valid():
            contexto = {
                'form': form
            }
            return render(request, 'minha_consulta.html', context=contexto)
        else:
            print('Form inválido')
            contexto = {
                'form': form
            }
            return render(request, 'index.html', context=contexto)

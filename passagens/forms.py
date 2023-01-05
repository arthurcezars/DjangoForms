from django import forms
from tempus_dominus.widgets import DatePicker
from datetime import datetime
from passagens.classe_viagem import tipos_de_classes
from passagens.validation import *
from passagens.models import Passagem, ClasseViagem, Pessoa

class PassagemForms(forms.ModelForm):
    data_pesquisa = forms.DateField(label='Data da pesquisa', disabled=True, initial=datetime.today)
    class Meta:
        model = Passagem
        fields = '__all__'
        labels = {
            'data_ida': 'Data de ida',
            'data_volta': 'Data de volta',
            'informacoes': 'Informações',
            'classe_viagem': 'Classe do vôo'
        }
        widgets = {
            'data_ida': DatePicker(),
            'data_volta': DatePicker()
        }

    # Realiza a validação somente do campo origem
    # def clean_origem(self):
    #     origem = self.cleaned_data.get('origem')
    #     if any(char.isdigit() for char in origem):
    #         raise forms.ValidationError('Origem inválida: Não inclua números')
    #     else:
    #         return origem

    # Realiza a validação somente do campo destino
    # def clean_destino(self):
    #     destino = self.cleaned_data.get('destino')
    #     if any(char.isdigit() for char in destino):
    #         raise forms.ValidationError('Destino inválido: Não inclua números')
    #     else:
    #         return destino

    # Pode ser usado para validar todos os campos.
    # O Django chama primeiro as funções de validação de campos individuais.
    def clean(self):
        origem = self.cleaned_data.get('origem')
        destino = self.cleaned_data.get('destino')
        data_ida = self.cleaned_data.get('data_ida')
        data_volta = self.cleaned_data.get('data_volta')
        data_pesquisa = self.cleaned_data.get('data_pesquisa')
        lista_de_erros = {}
        campo_tem_algum_numero(origem, 'origem', lista_de_erros)
        campo_tem_algum_numero(destino, 'destino', lista_de_erros)
        origem_destino_iguais(origem, destino, lista_de_erros)
        data_ida_maior_que_data_volta(data_ida, data_volta, lista_de_erros)
        data_ida_menor_data_de_hoje(data_ida, data_pesquisa, lista_de_erros)
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class PessoaForms(forms.ModelForm):
    class Meta:
        model = Pessoa
        exclude = ['nome']

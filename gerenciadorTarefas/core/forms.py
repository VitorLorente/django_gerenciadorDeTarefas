from django.forms import ModelForm, DateField, DateInput
from core.models import *

class TarefaForm(ModelForm):
    
    class Meta:
        model = Tarefa
        fields = ['tipo', 'prazo', 'id_turma', 'id_professor', 'descricao']
        widgets = {
        'prazo': DateInput(format=('%m/%d/%Y')),
        }
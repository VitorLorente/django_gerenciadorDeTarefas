from django.shortcuts import render
from core.models import *

# Create your views here.

class AlunoAux:
    def __init__(self, nome, numero, feitas, nfeitas, incompletas, slug, totalTarefas):
        self.nome = nome
        self.numero = numero
        self.feitas = feitas
        self.nfeitas = nfeitas
        self.incompletas = incompletas
        self.slug = slug
    def porcentagem(self, total):
        fporcem = (self.feitas * 100)/total
        nfporcem = (self.nfeitas * 100)/total
        inporcem = (self.incompletas *100)/total

        return {'feitas':fporcem,'naoFeitas':nfporcem,'incompletas':inporcem}        
        

def area_professor(request):

    professor = Professor.objects.get(id=3)
    turmas = Professorturma.objects.all()
    turmas_professor = []

    for turma in turmas:
        if turma.id_professor.id == professor.id:
            turmas_professor.append(turma.id_turma)

    context = {
        'turmas':turmas_professor,
        'professor': professor
    }

    return render(request, "area_professor.html", context)

def turma(request, slug):

    
    turma = Turma.objects.get(slug=slug)
    alunos_turma = Aluno.objects.filter(id_turma = turma.id)
    

    context = {
        'alunos':alunos_turma
    }    

    return render(request, "turma.html", context)
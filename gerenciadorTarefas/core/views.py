from django.shortcuts import render
from core.models import *
import simplejson

# Create your views here.

class AlunoAux:
    def __init__(self, nome, numero, feitas, nfeitas, incompletas, slug):
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
        slugId = self.slug

        return {
            "slug": self.slug,
            "feitas": self.feitas,
            "naoFeitas": self.nfeitas,
            "incompletas": self.incompletas
        }

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
    alunosAux = []
    dadosAlunos = []
    tarefas = Alunotarefa.objects.all()
    tarefas_turma = Tarefa.objects.filter(id_turma = turma.id)

    for aluno in alunos_turma:
        tarefas_aluno = Alunotarefa.objects.filter(id_aluno = aluno.id)
        feitas = 0
        nFeitas = 0
        incom = 0

        for tarefa in tarefas_aluno:
            if tarefa.visto == 'f':
                feitas += 1
            elif tarefa.visto == 'n':
                nFeitas += 1
            else:
                incom += 1

        alunosAux.append(AlunoAux(aluno.nome, aluno.numero_chamada, feitas, nFeitas, incom, aluno.slug))
    
    for aluno in alunosAux:
        dadosAlunos.append(aluno.porcentagem(len(tarefas_turma)))    
    
    dados_tarefa = simplejson.dumps(dadosAlunos)
    context = {
        'alunos':alunosAux,
        'dadosAlunos': dados_tarefa
    }    

    return render(request, "turma.html", context)
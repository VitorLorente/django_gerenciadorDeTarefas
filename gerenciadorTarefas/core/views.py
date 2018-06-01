from django.shortcuts import render
from core.models import *
from core.forms import *
import simplejson, json
from datetime import date

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

        return {
            "slug": self.slug,
            "feitas": ('%.1f' %fporcem),
            "naoFeitas": ('%.1f' %nfporcem),
            "incompletas": ('%.1f' %inporcem)
        }

def slug_tarefa(tipo, prazo, id_professor):
    prazo = str(prazo)
    idAux = str(id_professor)

    tipoAux = tipo[0]
    prazoAux = ''.join(prazoLista.split('-'))

    return '{}{}{}'.format(tipoAux, prazoAux, idAux)



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

    professor = Professor.objects.get(id=3)
    turma = Turma.objects.get(slug=slug)
    alunos_turma = Aluno.objects.filter(id_turma = turma.id)
    alunosAux = []
    dadosAlunos = []
    tarefas = Alunotarefa.objects.all() #todas as tarefas da tabela AlunoTarefa
    tarefas_id = [] #id's das tarefas da tabela AlunoTarefa
    tarefas_turma = Tarefa.objects.filter(id_turma = turma.id) #todas as tarefas desta turma
    tarefas_professor = [] #todas as tarefas do professor logado
    tarefasVistas = [] #tarefas já vistadas
    tarefasNvistas = [] #tarefas ainda não vistadas

    for tarefa in tarefas:
        tarefas_id.append(tarefa.id)

    for tarefa in tarefas_turma:
        if tarefa.id_professor.id == professor.id:
            tarefas_professor.append(tarefa)

    for tarefa in tarefas_professor:
        if tarefa.id in tarefas_id:
            tarefasVistas.append(tarefa)
        else:
            tarefasNvistas.append(tarefa)  

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
        'dadosAlunos': dados_tarefa,
        'turma' : turma,
        'tarefasV': tarefasVistas,
        'tarefasN': tarefasNvistas
    }    

    return render(request, "turma.html", context)

def aluno(request, slug):

    aluno = Aluno.objects.get(slug=slug)
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

    alunoAux = AlunoAux(aluno.nome, aluno.numero_chamada, feitas, nFeitas, incom, aluno.slug)
    tarefasTurma = len(Tarefa.objects.filter(id_turma=aluno.id_turma.id))
    tarefasAluno = simplejson.dumps(alunoAux.porcentagem(tarefasTurma))



    context = {
        'aluno': alunoAux,
        'dadosTarefas': tarefasAluno,
        'tarefas': tarefas_aluno
    }

    return render(request, "aluno.html", context)

def tarefa(request, slug):
    tarefa = Tarefa.objects.get(slug=slug)
    alunos = Alunotarefa.objects.filter(id_tarefa=tarefa)
    alunosTarefa = []

    '''for aluno in alunos:
        if aluno.id_turma == tarefa.id_turma:
            alunosTarefa.append(aluno)'''

    if request.is_ajax():
        if request.POST:
            vistos = request.body
            for aluno in alunos:
                for visto in vistos:
                    if visto.numero == aluno.id_aluno.numero_chamada:
                        status = 'F'
                        if visto.visto == 'nao fez':
                            status = 'N'
                        elif visto.visto == 'incompleto':
                            status = 'I'
                        aluno.visto = status

    context = {
        'alunos': alunos
    }
            
            
    return render(request, "vistar_tarefa.html", context)

def cadastrar_tarefa(request):
    today = date.today()
    today = today.strftime('%d/%m/%Y')
    if request.POST:
        form = TarefaForm(request.POST)
        if form.is_valid():
            forms = form.save(commit=false)
            forms.slug = slug_tarefa(forms.tipo, forms.prazo, forms.id_professor.id)
            forms.data = today
            forms.save()
            return redirect('/cadastrar_tarefa')

    else:
        form = TarefaForm()

    context = {
        'form':form,
        'hoje':today
    }

    return render(request, "cadastrar_tarefa.html", context)
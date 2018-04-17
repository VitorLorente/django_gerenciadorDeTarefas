from django.shortcuts import render
from core.models import *

# Create your views here.

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

    return render(request, "turma.html")
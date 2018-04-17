# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Professor(models.Model):
    nome = models.CharField(max_length=70)
    email = models.CharField(max_length=85)

    class Meta:
        db_table = 'Professor'

class Turma(models.Model):
    turno = models.CharField(max_length=1)
    nivel = models.CharField(max_length=35)
    serie = models.IntegerField()
    identificador = models.CharField(max_length=1)
    slug = models.SlugField(max_length=20)

    class Meta:
        db_table = 'Turma'
        unique_together = (('turno', 'nivel', 'serie', 'identificador'),)

    def __str__(self):
        return '{}º{}'.format(self.serie, self.identificador)

class Tarefa(models.Model):
    tipo = models.CharField(max_length=25)
    descricao = models.TextField(blank=True, null=True)
    data = models.DateField()
    prazo = models.DateField()
    id_turma = models.ForeignKey('Turma', models.DO_NOTHING, db_column='id_turma')
    id_professor = models.ForeignKey(Professor, models.DO_NOTHING, db_column='id_professor')
    slug = models.SlugField(max_length=20)

    class Meta:
        db_table = 'Tarefa'

class Responsavel(models.Model):
    nome = models.CharField(max_length=70)
    email = models.CharField(max_length=85, blank=True, null=True)
    celular = models.CharField(max_length=15)

    class Meta:
        db_table = 'Responsavel'


class Aluno(models.Model):
    nome = models.CharField(max_length=70)
    ra = models.IntegerField(unique=True)
    email = models.CharField(max_length=85)
    celular = models.CharField(max_length=15)
    id_responsavel = models.ForeignKey('Responsavel', models.DO_NOTHING, db_column='id_responsavel')
    id_turma = models.ForeignKey('Turma', models.DO_NOTHING, db_column='id_turma')
    slug = models.SlugField(max_length=20)

    class Meta:
        db_table = 'Aluno'


class Alunotarefa(models.Model):
    visto = models.CharField(max_length=1)
    id_aluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='id_aluno')
    id_tarefa = models.ForeignKey('Tarefa', models.DO_NOTHING, db_column='id_tarefa')

    class Meta:
        db_table = 'AlunoTarefa'
        unique_together = (('id_aluno', 'id_tarefa'),)


class Professorturma(models.Model):
    disciplina = models.CharField(max_length=25)
    id_professor = models.ForeignKey(Professor, models.DO_NOTHING, db_column='id_professor')
    id_turma = models.ForeignKey('Turma', models.DO_NOTHING, db_column='id_turma')

    class Meta:
        db_table = 'ProfessorTurma'
        unique_together = (('id_professor', 'id_turma'),)


class Responsaveltarefa(models.Model):
    id_responsavel = models.ForeignKey(Responsavel, models.DO_NOTHING, db_column='id_responsavel')
    id_tarefa = models.ForeignKey('Tarefa', models.DO_NOTHING, db_column='id_tarefa')
    visualizado = models.IntegerField()

    class Meta:
        db_table = 'ResponsavelTarefa'
        unique_together = (('id_responsavel', 'id_tarefa'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

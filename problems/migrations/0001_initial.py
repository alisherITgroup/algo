# Generated by Django 4.1.6 on 2023-03-01 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('problemsets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveProblem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='Masala nomi')),
                ('problem', models.TextField(verbose_name='Masala matni')),
                ('timelimit', models.IntegerField(verbose_name='TimeLimit')),
                ('memorylimit', models.IntegerField(verbose_name='MemoryLimit')),
                ('difficulty', models.IntegerField(verbose_name='Masala qiyinchiligi')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Masala uchun izoh.')),
                ('infoin', models.TextField(blank=True, default="Kirish ma'lumotlari mavjud emas.", null=True, verbose_name="Kirish ma'lumotlari")),
                ('infoout', models.TextField(blank=True, default='Masala javobi.', null=True, verbose_name="Chiqish ma'lumotlari")),
                ('simpletests', models.TextField(blank=True, default='{}', null=True, verbose_name='Simple testlar')),
                ('tests', models.TextField(verbose_name='Testlar')),
                ('solution', models.TextField(blank=True, default='Muallif bu masala yechimini taqdim qilmagan.', null=True, verbose_name='Masalar yechimi.')),
                ('allowedlangs', models.ManyToManyField(related_name='archive_problem_langs', to='problemsets.programminglanguage')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archive_problem_author', to=settings.AUTH_USER_MODEL)),
                ('category', models.ManyToManyField(related_name='archive_problem_category', to='problemsets.category')),
                ('errors', models.ManyToManyField(related_name='problem_errors', to=settings.AUTH_USER_MODEL)),
                ('solvers', models.ManyToManyField(related_name='problem_solvers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArchiveProblemComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.IntegerField(default=0)),
                ('body', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems.archiveproblem')),
            ],
        ),
    ]
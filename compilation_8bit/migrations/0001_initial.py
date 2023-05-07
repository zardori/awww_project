# Generated by Django 4.1.7 on 2023-05-07 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now_add=True)),
                ('delete_status_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SectionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'compiles without warnings'), (1, 'compiles with warning(s)'), (2, 'not compiles'), (3, 'not compiled yet')])),
            ],
        ),
        migrations.CreateModel(
            name='SectionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'procedure'), (1, 'comment'), (2, 'directive'), (3, 'variables declaration'), (4, 'assembly code')])),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('login', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(null=True)),
                ('start', models.PositiveIntegerField()),
                ('end', models.PositiveIntegerField()),
                ('status', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='compilation_8bit.sectionstatus')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now_add=True)),
                ('delete_status_date', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compilation_8bit.user')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compilation_8bit.directory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='directory',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compilation_8bit.user'),
        ),
        migrations.AddField(
            model_name='directory',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compilation_8bit.directory'),
        ),
        migrations.CreateModel(
            name='CompilationStatusInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_line', models.PositiveIntegerField()),
                ('info', models.TextField()),
                ('info_type', models.PositiveSmallIntegerField(choices=[(0, 'warning'), (1, 'error')])),
                ('section_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compilation_8bit.sectionstatus')),
            ],
        ),
    ]

# Generated by Django 3.2.12 on 2022-11-18 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_remove_surveypage_survey'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveypage',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='Data de nascimento'),
        ),
        migrations.AddField(
            model_name='surveypage',
            name='cnpj',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='CNPJ'),
        ),
        migrations.AddField(
            model_name='surveypage',
            name='contract_type',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Tipo de contrato'),
        ),
        migrations.AddField(
            model_name='surveypage',
            name='cpf',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='CPF'),
        ),
        migrations.AddField(
            model_name='surveypage',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='E-mail da empresa'),
        ),
        migrations.AddField(
            model_name='surveypage',
            name='exam_type',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Tipo de exame'),
        ),
        migrations.AddField(
            model_name='surveypage',
            name='function',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Função'),
        ),
        migrations.AddField(
            model_name='surveypage',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome'),
        ),
        migrations.AddField(
            model_name='surveypage',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Telefone'),
        ),
        migrations.AddField(
            model_name='surveypage',
            name='rg',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='RG'),
        ),
        migrations.AddField(
            model_name='surveypage',
            name='social_reason',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Razão Social'),
        ),
        migrations.AddField(
            model_name='surveypage',
            name='toxicologic',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Toxicológico?'),
        ),
    ]
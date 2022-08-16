# Generated by Django 3.2.12 on 2022-08-16 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0021_renomeia_pls'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessaoVeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispositivo', models.CharField(max_length=12)),
                ('proposicao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessoes_vetos', to='candidate.proposicao')),
            ],
        ),
        migrations.CreateModel(
            name='VotacaoDispositivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_parlamentar', models.CharField(max_length=120)),
                ('tipo_voto', models.CharField(max_length=26)),
                ('casa', models.CharField(choices=[('senado', 'senado'), ('camara', 'camara')], max_length=7)),
                ('sessao_veto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votacoes', to='candidate.sessaoveto')),
            ],
        ),
        migrations.AddIndex(
            model_name='votacaodispositivo',
            index=models.Index(fields=['nome_parlamentar', 'sessao_veto'], name='votacaodispositivo_nomsess_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='votacaodispositivo',
            unique_together={('nome_parlamentar', 'sessao_veto')},
        ),
        migrations.AddIndex(
            model_name='sessaoveto',
            index=models.Index(fields=['dispositivo', 'proposicao'], name='sessaoveto_disp_prop_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='sessaoveto',
            unique_together={('dispositivo', 'proposicao')},
        ),
    ]

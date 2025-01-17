# Generated by Django 4.1.3 on 2023-03-01 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conditions', '0004_get_condition_pixels'),
        ('plan', '0015_remove_scenario_max_budget_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectarea',
            name='scenario',
        ),
        migrations.AddField(
            model_name='scenario',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Processing'), (2, 'Processed'), (3, 'Failed')], default=0),
        ),
        migrations.AlterField(
            model_name='scenarioweightedpriority',
            name='priority',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='conditions.condition'),
        ),
        migrations.CreateModel(
            name='RankedProjectArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('weighted_score', models.FloatField()),
                ('project_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.projectarea')),
                ('scenario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.scenario')),
            ],
        ),
        migrations.CreateModel(
            name='ConfigPriority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conditions.condition')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.project')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='priorities_new',
            field=models.ManyToManyField(related_name='pri_new', through='plan.ConfigPriority', to='conditions.condition'),
        ),
    ]

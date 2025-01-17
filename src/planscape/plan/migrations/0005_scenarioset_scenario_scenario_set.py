# Generated by Django 4.1.3 on 2023-01-05 22:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conditions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plan', '0004_plan_creation_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScenarioSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('priorities', models.ManyToManyField(to='conditions.condition')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.project')),
            ],
        ),
        migrations.AddField(
            model_name='scenario',
            name='scenario_set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plan.scenarioset'),
        ),
    ]

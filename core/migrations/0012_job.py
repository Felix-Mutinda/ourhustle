# Generated by Django 3.1.4 on 2020-12-08 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_jobcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('allow_comments', models.BooleanField(default=True)),
                ('start_accepting_applications_at', models.DateTimeField()),
                ('stop_accepting_applications_at', models.DateTimeField()),
                ('employment_term', models.CharField(blank=True, max_length=255)),
                ('seniority_level', models.CharField(blank=True, max_length=255)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.jobcategory')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.userprofile')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.organisation')),
            ],
        ),
    ]
# Generated by Django 4.0.1 on 2022-03-21 18:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_alter_answer_text_alter_question_text_questionnaire_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userresponse',
            old_name='question',
            new_name='questionnaire',
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questionnairesDone', models.ManyToManyField(blank=True, null=True, to='main.Questionnaire')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.myuser'),
        ),
    ]

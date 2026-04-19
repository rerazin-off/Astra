# Автор карточки — Users_System вместо Django User

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module_project', '0003_alter_cards_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cards',
            name='author',
        ),
        migrations.AddField(
            model_name='cards',
            name='author',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='authored_cards',
                to='module_project.users_system',
                verbose_name='Автор карточки',
            ),
        ),
    ]

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    ApplicationCheck.application_id was originally declared as
    IntegerField(OneToOneField(...)) — a broken field definition
    (a relation passed as an argument to IntegerField). This replaces
    it with a proper OneToOneField named `application`.
    """

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationcheck',
            name='application_id',
        ),
        migrations.AddField(
            model_name='applicationcheck',
            name='application',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to='users.application',
                default=None,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='applicationcheck',
            name='application',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to='users.application',
            ),
        ),
    ]

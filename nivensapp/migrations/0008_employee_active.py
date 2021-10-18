from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nivensapp', '0007_auto_20210803_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]

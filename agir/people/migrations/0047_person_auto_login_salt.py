# Generated by Django 2.1.3 on 2018-12-03 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("people", "0046_auto_20181114_1416")]

    operations = [
        migrations.AddField(
            model_name="person",
            name="auto_login_salt",
            field=models.CharField(blank=True, default="", max_length=255),
        )
    ]
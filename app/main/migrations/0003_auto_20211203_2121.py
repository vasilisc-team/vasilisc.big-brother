# Generated by Django 3.2.9 on 2021-12-03 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_image_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images_face')),
            ],
        ),
        migrations.RenameModel(
            old_name='Image',
            new_name='ImageRubbish',
        ),
    ]

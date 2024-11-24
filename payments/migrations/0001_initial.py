# Generated by Django 5.1.2 on 2024-10-28 14:47

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buyers',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='CodeRepository',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code_emage', models.ImageField(upload_to='')),
                ('github_url', models.URLField()),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserCodeAccess',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('access_granted_at', models.DateTimeField(auto_now_add=True)),
                ('is_invitation_sent', models.BooleanField(default=False)),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.coderepository')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.buyers')),
            ],
        ),
    ]

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rolls', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ordine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indirizzo_spedizione', models.CharField(max_length=255)),
                ('metodo_pagamento', models.CharField(choices=[('visa', 'Visa'), ('mastercard', 'Mastercard'), ('paypal', 'PayPal'), ('klarna', 'Klarna')], max_length=20)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordini', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrdineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prezzo_unitario', models.FloatField()),
                ('quantita', models.PositiveIntegerField(default=1)),
                ('ordine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='rolls.ordine')),
                ('roll', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rolls.roll')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_nascita', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

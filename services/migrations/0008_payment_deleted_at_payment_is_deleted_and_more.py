# Generated by Django 5.1.2 on 2024-10-27 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_payment_staff_payment_staff_payment_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='staff_payment_percentage',
            field=models.DecimalField(decimal_places=2, default=0.4, max_digits=5),
        ),
    ]

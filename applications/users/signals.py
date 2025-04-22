from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser  # Importación relativa

@receiver(post_save, sender=CustomUser)
def assign_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'MESONERO':
            group = Group.objects.get(name="Mesoneros")
        elif instance.role == 'CAJERO':
            group = Group.objects.get(name="Cajeros")
        else:
            return
        instance.groups.add(group)
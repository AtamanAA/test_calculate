from django.db import models

# Create your models here.

class Material(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)    
    type = models.CharField(max_length=40)
    condition = models.CharField(max_length=40, blank=True,)
    hardness = models.FloatField(help_text="HB")
    yield_strenght = models.FloatField(help_text="МПа")

    def __str__(self):
        return f"{self.name} {self.type} {self.condition}"

    def __repr__(self):
        return f"Material(id={self.pk})"

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all materials
        """
        return list(Material.objects.all())
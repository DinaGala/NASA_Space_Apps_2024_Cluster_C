from django.db import models

# Create your models here.
#class App_back(models.Model):
#	nombre = models.CharField(max_length=100)
#	fecha = models.DateField()
#	latitud = models.FloatField()
#	longitud = models.FloatField()
	#...

#	def __str__(self):
#		return self.nombre

class Usuario(models.Model):
	nombre = models.CharField(max_length=100)
	email = models.EmailField()
	fecha_registro = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.nombre
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UsuarioNoRegistrados(models.Model):
	email = models.EmailField()
	latitud = models.FloatField()
	longitud = models.FloatField()
	fecha_solicitud = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.email} - {self.latitud}, {self.longitud}"


class UsuarioManager(BaseUserManager):
	def create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError('El usuario debe tener un email')
		if not password:
			raise ValueError('El usuario debe tener una contraseña')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

class Usuario(AbstractBaseUser):
	email = models.EmailField(unique=True)
	nombre = models.CharField(max_length=100)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	longitud = models.FloatField()
	latitud = models.FloatField()
	#path = 
	#row = 
	#next_image_time_utc = //timestamp yer-month-day
	#next_image_time_user = //hour:min
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['nombre', 'apellidos']
	objects = UsuarioManager()

	def __str__(self):
		return self.nombre


class Medicion(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	fecha = models.DateTimeField(auto_now_add=True)
	valor_R = models.FloatField()
	valor_G = models.FloatField()
	valor_B = models.FloatField()

	def __str__(self):
		return f"Medición en {self.fecha}: R={self.valor_R}, G={self.valor_G}, B={self.valor_B}"



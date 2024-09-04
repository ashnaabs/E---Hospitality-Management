from django.db import models
from Eproject import settings

# Create your models here.
class Registration(models.Model):
    id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=250, unique=True)
    age = models.IntegerField()
    place = models.CharField(max_length=250)
    phone = models.IntegerField()

    def __str__(self):
        return self.patient_name


class Login_patient(models.Model):
    patient_name = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
        if not Registration.objects.filter(patient_name=self.patient_name).exists():
            raise ValueError("User is not registered")
        super(Login_patient, self).save(*args, **kwargs)

class Doctor(models.Model):
    doctor = models.CharField(max_length=250,null=True)
    def __str__(self):
        return '{}'.format(self.doctor)


class Slots(models.Model):
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True)
    date = models.DateField()
    time = models.TimeField()
    category = models.CharField(max_length=270)
    phone = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class history(models.Model):
    patient_name=models.CharField(max_length=270)
    age=models.IntegerField()
    gender=models.CharField(max_length=240)
    BMI = models.IntegerField()
    background_notes = models.TextField()
    drug_history = models.TextField()
    patient_issues = models.CharField(max_length=500)
    Medications = models.CharField(max_length=240)

from django.contrib.auth.models import User


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment {self.id} - {self.status}'

class admin_resource(models.Model):
    doctor=models.CharField(max_length=240)
    address=models.TextField()


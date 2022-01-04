from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Detector(models.Model):
    word = models.TextField()

    def __str__(self):
        return self.word

class Percentage(models.Model):
    number = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return str(self.number)

def lofensivo(value):
    lsofensiva = Detector.objects.all()
    lsofensiva2 =[]
    
    for detector in lsofensiva:
        lsofensiva2.append(detector.word)

    if("¿" in value):
        value=value.replace("¿", "")
    if("?" in value):
        value=value.replace("?", "")
    if("." in value):
        value=value.replace(".", "")
    if("," in value):
        value=value.replace(",", "")
    if("(" in value):
        value=value.replace("(", "")
    if(")" in value):
        value=value.replace(")", "")

    value=value.lower()

    palabras = value.split()

    
    numero= Percentage.objects.last()
    if len(Percentage.objects.all())==0:
        numero= Percentage(number=15)
        numero.save()
    porcentaje= numero.number /100
    cont = 0
    res= False

    for palabra in palabras:
        if(palabra in lsofensiva2):
            cont+=1
        
    if(cont/len(palabras)>porcentaje):
        res=True
    return res
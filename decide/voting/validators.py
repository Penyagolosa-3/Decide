from django.core.exceptions import ValidationError

from . import models
"""Comentar y descomentar lsofensiva para hacer las migraciones de las bd, por defecto da
 error si se hace con los datos de los modelos"""
def lofensivo(value):
    #lsofensiva=[]
    lsofensiva = models.Detector.objects.all()
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

    
    numero= models.Percentage.objects.last()
    #numero= 15
    if len(models.Percentage.objects.all())==0:
        numero= models.Percentage(number=15)
        numero.save()
    porcentaje= numero.number /100
    #porcentaje= 15 /100
    cont = 0
    res= False

    for palabra in palabras:
        if(palabra in lsofensiva2):
            cont+=1
        
    if(cont/len(palabras)>porcentaje):
        res=True
    return res
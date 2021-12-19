from django.core.exceptions import ValidationError

from . import models
value = "puta puta puta"

def lofensivo(value):
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
    porcentaje= numero.number /100
    cont = 0
    res= False

    for palabra in palabras:
        if(palabra in lsofensiva2):
            cont+=1
        
    if(cont/len(palabras)>porcentaje):
        res=True
    return res
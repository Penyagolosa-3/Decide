from django.core.exceptions import ValidationError
value = "puta puta puta"

def lofensivo(value):
    lsofensiva = ["puta", "puto", "cabrón", "gilipollas", "maricón", "imbécil", "estúpido", "subnormal", "anormal", "chupapollas"]

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

    porcentaje=0.15
    cont = 0

    for palabra in palabras:
        if(palabra in lsofensiva):
            cont+=1
        
    if(cont/len(palabras)>porcentaje):
        raise ValidationError(("Se ha encontrado lenguaje ofensivo en la pregunta"), params={"palabras": palabras} )


##print(lofensivo(value))
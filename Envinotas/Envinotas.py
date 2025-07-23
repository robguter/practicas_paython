import pandas as pnd # type: ignore
from datetime import datetime
from docxtpl import DocxTemplate

doc = DocxTemplate("Notas.docx")

nombre = "Robert"
apellido = "Gutiérrez"
correo = "robgutgom@gmail.com"
fecha = datetime.today().strftime("%d/%m/%Y")

""" print(pnd.__version__)
print(fecha) """

constantes = {
    "nombre" : nombre,
    "apellido" : apellido,
    "correo" : correo,
    "fecha" : fecha
}

""" print(constantes) """

dtfrm = pnd.read_excel("Notas.xlsx")
for indice, fila in dtfrm.iterrows():
    contenido = {
        "nomb_a" : fila["Nombre"],
        "apel_a" : fila["Apellido"],
        "cedu_a" : fila["Cedula"],
        "mate_a" : fila["Matematicas"],
        "fisi_a" : fila["Fisica"],
        "quim_a" : fila["Quimica"]
    }
    contenido.update(constantes)
    doc.render(contenido)
    doc.save(f"notas_de_{fila['Cedula']}.docx")
    

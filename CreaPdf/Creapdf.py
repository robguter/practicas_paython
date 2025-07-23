import streamlit as stl
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        if hasattr(self, "document_title"):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, self.document_title, 0, 1, "C")
            
    def footer(self):
        self.set_y(-10)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")
        
    def chapter_title(self, title, font='Arial', size=13):
        self.set_font(font, "B", size)
        self.cell(0, 7, title, 0, 1, "L")
        self.ln(3)
        
    def chapter_body(self, body, font='Arial', size=12):
        self.set_font(font, "", size)
        self.multi_cell(0, 7, body)
        self.ln()
        
def create_pdf(filename, document_title, author, chapters, image_path=None):
    pdf = PDF()
    pdf.document_title = document_title
    pdf.add_page()
    if author:
        pdf.set_author(author)
        
    if image_path:
        pdf.image(image_path, x=(pdf.w / 2) - ((pdf.w / 6)/2), y=20, w=pdf.w / 6)
        pdf.ln(25)
    
    for chapter in chapters:
        title, body, font, size = chapter
        pdf.chapter_title(title, font, size)
        pdf.chapter_body(body, font, size)
        
    pdf.output(filename)
        
def main():
    stl.title("Generador de PDF con Python")
    stl.header("Configuración del Documento")
    documento_title = stl.text_input("Título del Documento", "Escribe el Título del Documento")
    author = stl.text_input("Autor", "Indique el Autor")
    uploaded_image = stl.file_uploader("Sube una imagen para el documento (Opcional)", type=["jpg", "png"])
    stl.header("Capítulos del Documento")
    chapters = []
    chapter_count = stl.number_input("Número de capítulos", min_value=1, max_value=10, value=1)
    
    for i in range(chapter_count):
        stl.subheader(f"Capitulo {i + 1}")
        title = stl.text_input(f"Título del Capítulo {i + 1}",
                               f"Título del Capítulo {i + 1}")
        body = stl.text_area(f"Cuerpo del Capítulo {i + 1}",
                             f"Contenido del Capítulo {i + 1}")
        font = stl.selectbox(f"Fuente del Capítulo {i + 1}",
                             ["Arial", "Courier", "Times"])
        size = stl.slider(f"Tamaño de la Fuente del Capítulo {i + 1}", 8, 24, 12)
        chapters.append((title, body, font, size))
        
    if stl.button("Generar PDF"):
        image_path = uploaded_image.name if uploaded_image else None
        if image_path:
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())
                
        create_pdf("historia.pdf", documento_title, author, chapters, image_path)
        
        with open("historia.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()
            
        stl.download_button(
            label="Descargar PDF",
            data=PDFbyte,
            file_name="output_fpdf.pdf",
            mime="application/octet-stream"
        )
        
        stl.success("PDF Generado Exitosamente")

if __name__ == "__main__":
    main()

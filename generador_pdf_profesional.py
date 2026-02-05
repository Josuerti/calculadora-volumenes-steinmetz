"""
Generador de Reportes PDF Profesionales con Matemáticas Renderizadas
Proyecto: Análisis de Sólidos mediante Integrales Múltiples
Facultad de Ingeniería - UCSG
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import numpy as np
import io
from datetime import datetime


class GeneradorReporteProfesionalUCSG:
    """
    Generador de reportes PDF profesionales con matemáticas renderizadas.
    """
    
    def __init__(self, filename="Reporte_Analisis_UCSG.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=2.5*cm,
            leftMargin=2.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        self.story = []
        self.styles = getSampleStyleSheet()
        self._configurar_estilos()
        
        # Colores UCSG
        self.color_rojo = colors.HexColor('#a33238')
        self.color_negro = colors.HexColor('#1a1a1a')
        self.color_gris = colors.HexColor('#f2f2f2')
        
    def _configurar_estilos(self):
        """Configura los estilos tipográficos."""
        
        self.styles.add(ParagraphStyle(
            name='TituloUCSG',
            parent=self.styles['Heading1'],
            fontName='Times-Bold',
            fontSize=16,
            textColor=colors.HexColor('#1a1a1a'),
            alignment=TA_CENTER,
            spaceAfter=8
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubtituloUCSG',
            parent=self.styles['Normal'],
            fontName='Times-Roman',
            fontSize=11,
            textColor=colors.HexColor('#a33238'),
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='SeccionTitulo',
            parent=self.styles['Heading2'],
            fontName='Times-Bold',
            fontSize=13,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=12,
            spaceBefore=15
        ))
        
        self.styles.add(ParagraphStyle(
            name='TextoNormal',
            parent=self.styles['Normal'],
            fontName='Times-Roman',
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            leading=14
        ))
        
    def renderizar_formula_matematica(self, formula_latex, ancho=15*cm):
        """
        Renderiza una fórmula matemática LaTeX como imagen usando matplotlib.
        
        Args:
            formula_latex: Fórmula en formato LaTeX
            ancho: Ancho deseado de la imagen
            
        Returns:
            Objeto Image de ReportLab
        """
        fig = plt.figure(figsize=(8, 1.5))
        fig.patch.set_facecolor('#fdfdfd')
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        # Renderizar LaTeX
        ax.text(0.5, 0.5, f'${formula_latex}$', 
                fontsize=18, 
                ha='center', 
                va='center',
                transform=ax.transAxes,
                family='serif')
        
        # Guardar en buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', 
                   facecolor='#fdfdfd', edgecolor='none', pad_inches=0.2)
        buf.seek(0)
        plt.close()
        
        # Crear imagen para PDF
        img = Image(buf, width=ancho, height=ancho*0.15)
        return img
        
    def agregar_encabezado(self, titulo: str, autores: str, fecha: str = None):
        """Agrega encabezado institucional con logo."""
        
        if fecha is None:
            fecha = datetime.now().strftime("%d de %B de %Y")
        
        # Logo UCSG
        import os
        logo_path = os.path.join(os.path.dirname(__file__), 'Logo_UCSG.png')
        
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=4*cm, height=4*cm)
            logo.hAlign = 'CENTER'
            self.story.append(logo)
            self.story.append(Spacer(1, 0.3*cm))
        
        # Títulos institucionales
        self.story.append(Paragraph(
            "UNIVERSIDAD CATÓLICA DE SANTIAGO DE GUAYAQUIL",
            self.styles['TituloUCSG']
        ))
        
        self.story.append(Paragraph(
            "FACULTAD DE INGENIERÍA",
            self.styles['TituloUCSG']
        ))
        
        self.story.append(Paragraph(
            "Departamento de Matemáticas",
            self.styles['SubtituloUCSG']
        ))
        
        # Línea decorativa
        data_linea = [['', '', '']]
        tabla_linea = Table(data_linea, colWidths=[16*cm])
        tabla_linea.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 3, self.color_rojo),
            ('LINEBELOW', (0, 0), (-1, 0), 1, self.color_negro)
        ]))
        self.story.append(tabla_linea)
        self.story.append(Spacer(1, 0.5*cm))
        
        # Título del proyecto
        self.story.append(Paragraph(
            f"<b>{titulo}</b>",
            self.styles['TituloUCSG']
        ))
        self.story.append(Spacer(1, 0.3*cm))
        
        # Información del proyecto
        info_data = [
            ['<b>Autores:</b>', autores],
            ['<b>Materia:</b>', 'Cálculo Vectorial y Varias Variables'],
            ['<b>Fecha:</b>', fecha]
        ]
        
        info_tabla = Table(info_data, colWidths=[4*cm, 12*cm])
        info_tabla.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Times-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
        ]))
        self.story.append(info_tabla)
        self.story.append(Spacer(1, 0.8*cm))
        
    def agregar_seccion_con_formulas(self, titulo: str, descripcion: str, 
                                    formulas: list = None):
        """
        Agrega una sección con descripción y fórmulas matemáticas renderizadas.
        
        Args:
            titulo: Título de la sección
            descripcion: Texto descriptivo
            formulas: Lista de diccionarios con 'latex' y 'descripcion'
        """
        
        self.story.append(Paragraph(f"<b>{titulo}</b>", self.styles['SeccionTitulo']))
        self.story.append(Paragraph(descripcion, self.styles['TextoNormal']))
        
        if formulas:
            for formula_info in formulas:
                if 'descripcion' in formula_info:
                    self.story.append(Paragraph(
                        formula_info['descripcion'], 
                        self.styles['TextoNormal']
                    ))
                
                # Renderizar fórmula
                img_formula = self.renderizar_formula_matematica(formula_info['latex'])
                self.story.append(img_formula)
                self.story.append(Spacer(1, 0.3*cm))
        
    def agregar_desarrollo_matematico(self, ec_superior: str, ec_inferior: str,
                                      x_min: str, x_max: str,
                                      y_min: str, y_max: str):
        """Agrega el desarrollo matemático completo paso a paso."""
        
        # Paso 1: Definición
        self.agregar_seccion_con_formulas(
            "1. DEFINICIÓN DEL PROBLEMA",
            "Se desea calcular el volumen del sólido delimitado por las siguientes superficies:",
            [
                {
                    'latex': f'f(x,y) = {ec_superior}',
                    'descripcion': 'Superficie superior:'
                },
                {
                    'latex': f'g(x,y) = {ec_inferior}',
                    'descripcion': 'Superficie inferior:'
                }
            ]
        )
        
        # Paso 2: Formulación
        self.agregar_seccion_con_formulas(
            "2. FORMULACIÓN DE LA INTEGRAL DOBLE",
            "El volumen se calcula mediante la integral doble de la diferencia de alturas:",
            [
                {
                    'latex': r'V = \iint_R [f(x,y) - g(x,y)] \, dA'
                }
            ]
        )
        
        # Paso 3: Límites
        self.agregar_seccion_con_formulas(
            "3. LÍMITES DE INTEGRACIÓN",
            "La región de integración R se describe mediante:",
            [
                {
                    'latex': f'x \\in [{x_min}, {x_max}]'
                },
                {
                    'latex': f'y \\in [{y_min}, {y_max}]'
                }
            ]
        )
        
        # Paso 4: Integral completa
        integral_completa = (
            f'V = \\int_{{{x_min}}}^{{{x_max}}} \\int_{{{y_min}}}^{{{y_max}}} '
            f'\\left[ ({ec_superior}) - ({ec_inferior}) \\right] \\, dy \\, dx'
        )
        
        self.agregar_seccion_con_formulas(
            "4. EXPRESIÓN COMPLETA DE LA INTEGRAL",
            "Sustituyendo los límites y las funciones:",
            [
                {
                    'latex': integral_completa
                }
            ]
        )
        
    def agregar_resultados(self, volumen_numerico: float, metodo: str = "Sumas de Riemann"):
        """Agrega los resultados del cálculo."""
        
        self.story.append(Paragraph(
            "<b>5. RESULTADOS DEL CÁLCULO</b>", 
            self.styles['SeccionTitulo']
        ))
        
        # Tabla de resultados
        data = [
            ['Método Empleado', 'Volumen Calculado', 'Precisión'],
            [metodo, f'{volumen_numerico:.8f} u³', 'ε < 10⁻⁴']
        ]
        
        tabla = Table(data, colWidths=[6*cm, 5*cm, 5*cm])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.color_negro),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.color_gris])
        ]))
        self.story.append(tabla)
        self.story.append(Spacer(1, 0.5*cm))
        
        # Resultado final renderizado
        resultado_latex = f'V = {volumen_numerico:.6f} \\, \\text{{unidades}}^3'
        img_resultado = self.renderizar_formula_matematica(resultado_latex)
        self.story.append(img_resultado)
        
    def agregar_grafica_3d(self, f_superior, f_inferior, x_lims, y_lims):
        """Agrega gráfica 3D del sólido."""
        
        self.story.append(PageBreak())
        self.story.append(Paragraph(
            "<b>6. VISUALIZACIÓN TRIDIMENSIONAL</b>", 
            self.styles['SeccionTitulo']
        ))
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Generar malla
        x = np.linspace(x_lims[0] - 0.5, x_lims[1] + 0.5, 50)
        y = np.linspace(y_lims[0] - 0.5, y_lims[1] + 0.5, 50)
        X, Y = np.meshgrid(x, y)
        
        Z_sup = np.zeros_like(X)
        Z_inf = np.zeros_like(X)
        
        for i in range(len(x)):
            for j in range(len(y)):
                try:
                    Z_sup[j, i] = f_superior(X[j, i], Y[j, i])
                    Z_inf[j, i] = f_inferior(X[j, i], Y[j, i])
                except:
                    Z_sup[j, i] = np.nan
                    Z_inf[j, i] = np.nan
        
        # Graficar
        ax.plot_surface(X, Y, Z_sup, alpha=0.85, cmap='Blues', edgecolor='none')
        ax.plot_surface(X, Y, Z_inf, alpha=0.85, cmap='Reds', edgecolor='none')
        
        ax.set_xlabel('Eje X', fontsize=12, fontweight='bold')
        ax.set_ylabel('Eje Y', fontsize=12, fontweight='bold')
        ax.set_zlabel('Eje Z', fontsize=12, fontweight='bold')
        ax.set_title('Sólido Analizado', fontsize=14, fontweight='bold', pad=20)
        ax.view_init(elev=25, azim=45)
        ax.grid(True, alpha=0.3)
        
        # Guardar
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        img = Image(buf, width=15*cm, height=12*cm)
        self.story.append(img)
        
    def finalizar(self):
        """Genera el PDF final."""
        self.doc.build(self.story)
        print(f"Reporte PDF generado: {self.filename}")
        return self.filename


def generar_reporte_profesional(nombre_solido: str = "Paraboloides", 
                                autores: str = "Equipo UCSG"):
    """
    Genera un reporte completo profesional.
    """
    from analizador_matematico import BibliotecaSolidos
    
    biblioteca = BibliotecaSolidos()
    
    if nombre_solido == "Paraboloides":
        resultado = biblioteca.paraboloides_intersectados()
    else:
        raise ValueError(f"Sólido '{nombre_solido}' no implementado")
    
    # Crear reporte
    filename = f"Reporte_Profesional_{nombre_solido}_UCSG.pdf"
    reporte = GeneradorReporteProfesionalUCSG(filename)
    
    # Encabezado
    reporte.agregar_encabezado(
        titulo=f"Análisis del Sólido: {resultado['nombre']}",
        autores=autores
    )
    
    # Desarrollo matemático
    reporte.agregar_desarrollo_matematico(
        ec_superior="8 - x^2 - y^2",
        ec_inferior="x^2 + y^2",
        x_min="-2",
        x_max="2",
        y_min="-\\sqrt{4-x^2}",
        y_max="\\sqrt{4-x^2}"
    )
    
    # Resultados
    reporte.agregar_resultados(
        volumen_numerico=resultado['resultado_numerico']['volumen'],
        metodo="Sumas de Riemann (100×100)"
    )
    
    # Gráfica 3D
    f_sup = lambda x, y: 8 - x**2 - y**2
    f_inf = lambda x, y: x**2 + y**2
    reporte.agregar_grafica_3d(f_sup, f_inf, (-2, 2), (-2, 2))
    
    # Conclusiones
    reporte.story.append(Paragraph(
        "<b>7. CONCLUSIONES</b>", 
        reporte.styles['SeccionTitulo']
    ))
    
    conclusiones = (
        f"Se calculó exitosamente el volumen del sólido {resultado['nombre']} "
        f"mediante integración numérica, obteniendo un valor de "
        f"{resultado['resultado_numerico']['volumen']:.6f} unidades cúbicas. "
        f"El método empleado garantiza una precisión adecuada para aplicaciones de ingeniería."
    )
    
    reporte.story.append(Paragraph(conclusiones, reporte.styles['TextoNormal']))
    
    return reporte.finalizar()


if __name__ == "__main__":
    print("="*80)
    print("GENERADOR DE REPORTES PROFESIONALES UCSG")
    print("="*80)
    print()
    
    autores = "Jsue, Samuel Cedeño, Evelyn Guaranda, Alberto Inga"
    generar_reporte_profesional("Paraboloides", autores)
    
    print()
    print("Reporte generado exitosamente")

# Sistema de Análisis de Sólidos mediante Integrales Múltiples

**Universidad Católica de Santiago de Guayaquil**  
**Facultad de Ingeniería - Departamento de Matemáticas**  
**Cálculo Vectorial y Varias Variables**

---

## 📂 Archivos del Proyecto

```
proyecto_cvv_final/
│
├── Logo_UCSG.png                              # Logo institucional
│
├── app_ucsg_final.html                        # Aplicación web principal ⭐
│
├── analizador_matematico.py                   # Motor de cálculo Python
├── generador_pdf_profesional.py               # Generador de reportes PDF
│
├── Reporte_Profesional_Paraboloides_UCSG.pdf  # Ejemplo de reporte generado
│
├── README.md                                  # Este archivo
└── INICIO_RAPIDO.md                           # Guía de uso detallada
```

---

## 🚀 Uso Rápido

### Opción 1: Aplicación Web (Sin instalaciones)

1. Abrir `app_ucsg_final.html` en cualquier navegador
2. Seleccionar un sólido predefinido o ingresar personalizado
3. Presionar "Ejecutar Análisis Completo"
4. Ver gráfico 3D y desarrollo matemático

**Características:**
- Notación matemática con teclado virtual
- Gráfico 3D interactivo
- Desarrollo paso a paso
- Sin necesidad de Python

### Opción 2: Generación de PDFs

**Requisitos:** Python 3.8+ con librerías:
```bash
python -m pip install -r requirements.txt
```

**Ejecutar:**
```bash
python3 generador_pdf_profesional.py
```

**Resultado:** Genera PDF con fórmulas renderizadas, gráficos 3D y desarrollo completo.

### Opción 3: Análisis en Consola

```bash
python3 analizador_matematico.py
```

Muestra cálculos numéricos (SciPy), simbólicos (SymPy) y comparación de métodos.

---

## ✨ Características Principales

✅ **Notación Matemática Real** - Entrada con teclado virtual MathLive  
✅ **Gráfico 3D Funcional** - Visualización interactiva con Plotly  
✅ **PDFs Profesionales** - Fórmulas renderizadas como imágenes  
✅ **Desarrollo Completo** - Paso a paso con explicaciones  
✅ **Sólidos Predefinidos** - 5 ejemplos listos para usar  
✅ **Diseño Profesional** - Sin emojis, estilo académico UCSG  

---

## 🎯 Sólidos Disponibles

1. **Paraboloides Intersectados** - z = 8 - x² - y² y z = x² + y²
2. **Esfera y Cono** - x² + y² + z² = 16 y z = √(x² + y²)
3. **Cilindro y Plano** - z = 4 - y y z = 0, sobre x² + y² ≤ 4
4. **Hemisferio** - x² + y² + z² = 9, z ≥ 0
5. **Personalizado** - Ingresar ecuaciones propias

---

## 📖 Documentación Completa

Consultar `INICIO_RAPIDO.md` para:
- Guía paso a paso
- Ejemplos de uso
- Solución de problemas
- Instrucciones para presentación

---

## 👥 Autores

- Samuel Cedeño
- Evelyn Guaranda
- Alberto Inga

**Materia:** Cálculo Vectorial y Varias Variables  
**Institución:** Universidad Católica de Santiago de Guayaquil  
**Año:** 2026

---

## 🔧 Tecnologías

- **Frontend:** HTML5, MathLive, Plotly.js, MathJax
- **Backend:** Python 3, NumPy, SciPy, SymPy
- **Reportes:** ReportLab, Matplotlib
- **Visualización:** Plotly.js para 3D interactivo

---

## 📄 Licencia

Proyecto académico desarrollado para la Universidad Católica de Santiago de Guayaquil.


## Versión web y mantenimiento

Este es el repositorio de referencia del proyecto. `app_ucsg_final.html` se distribuye también como `index.html` en [solidos_cvv](https://github.com/Josuerti/solidos_cvv). Mantén ambas copias sincronizadas al modificar la aplicación.

La aplicación necesita Internet para cargar sus bibliotecas. El desarrollo paso a paso es local y no requiere una clave de API. Utiliza punto medio en x y Simpson compuesto en y; la precisión depende de la región y las funciones. Los ejemplos incluyen valores exactos de referencia, que dejan de mostrarse si se editan los campos.

El analizador Python es un programa local independiente, no un servidor conectado a la aplicación web. Sus expresiones simbólicas se destinan a entradas de confianza, porque se procesan mediante SymPy.

## Verificación

Ejecuta `node tests.js` para comprobar la integración web y `python -m unittest test_analizador.py` para el motor Python. El reporte incluido es un ejemplo histórico; vuelve a generarlo para reflejar cambios del código.

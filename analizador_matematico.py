"""
Calculador de Volúmenes de Sólidos mediante Integrales Múltiples
Proyecto: Análisis de Sólidos y Regiones - Cálculo Vectorial
Universidad Católica de Santiago de Guayaquil (UCSG)
"""

import numpy as np
from scipy import integrate
import sympy as sp
from typing import Dict, Tuple, Callable, Optional


class AnalizadorMatematico:
    """Motor de cálculo que combina integración simbólica y numérica."""
    
    def __init__(self):
        self.x, self.y = sp.symbols('x y', real=True)
        
    def calcular_exacto(self, f_sup_str: str, f_inf_str: str, 
                       x_lims: Tuple, y_lims: Tuple) -> Dict:
        """
        Calcula el volumen exacto utilizando SymPy.
        
        Args:
            f_sup_str: Expresión de superficie superior (string SymPy)
            f_inf_str: Expresión de superficie inferior (string SymPy)
            x_lims: Tupla (x_min, x_max)
            y_lims: Tupla (y_min_expr, y_max_expr) como strings
            
        Returns:
            Dict con valor exacto en LaTeX, valor numérico y estado
        """
        try:
            # Parse usando los símbolos locales
            fs = sp.sympify(f_sup_str, locals={'x': self.x, 'y': self.y})
            fi = sp.sympify(f_inf_str, locals={'x': self.x, 'y': self.y})
            h = fs - fi
            
            # Convertir límites de y a expresiones simbólicas
            y_min_expr = sp.sympify(y_lims[0], locals={'x': self.x, 'y': self.y})
            y_max_expr = sp.sympify(y_lims[1], locals={'x': self.x, 'y': self.y})
            
            # Integral interna (dy)
            print(f"Integrando respecto a y: de {y_min_expr} a {y_max_expr}")
            res_y = sp.integrate(h, (self.y, y_min_expr, y_max_expr))
            
            # Integral externa (dx)
            print(f"Integrando respecto a x: de {x_lims[0]} a {x_lims[1]}")
            volumen = sp.integrate(res_y, (self.x, x_lims[0], x_lims[1]))
            
            # Simplificar el resultado
            volumen_simplificado = sp.simplify(volumen)
            
            return {
                "valor_exacto": sp.latex(volumen_simplificado),
                "valor_exacto_sympy": str(volumen_simplificado),
                "valor_numerico": float(volumen_simplificado.evalf()),
                "expresion_intermedia_y": sp.latex(res_y),
                "exito": True,
                "metodo": "Integración Simbólica (SymPy)"
            }
        except Exception as e:
            return {
                "error": str(e),
                "exito": False,
                "mensaje": f"No se pudo resolver analíticamente: {str(e)}"
            }
    
    def calcular_numerico(self, f_sup_func: Callable, f_inf_func: Callable,
                         x_lims: Tuple, y_lims_func: Tuple) -> Dict:
        """
        Calcula el volumen utilizando integración numérica de SciPy.
        
        Args:
            f_sup_func: Función superior f(x,y)
            f_inf_func: Función inferior g(x,y)
            x_lims: Tupla (x_min, x_max)
            y_lims_func: Tupla (y_min_func(x), y_max_func(x))
            
        Returns:
            Dict con volumen, error estimado y método
        """
        def integrando(y, x):
            """Altura del sólido h(x,y) = f(x,y) - g(x,y)"""
            try:
                return f_sup_func(x, y) - f_inf_func(x, y)
            except:
                return 0.0
        
        # Integración doble con SciPy
        # dblquad(func, x_min, x_max, y_min_func, y_max_func)
        volumen, error = integrate.dblquad(
            integrando,
            x_lims[0], x_lims[1],
            y_lims_func[0], y_lims_func[1],
            epsabs=1e-8,
            epsrel=1e-8
        )
        
        return {
            "volumen": volumen,
            "error_estimado": error,
            "precision": f"±{error:.2e}",
            "metodo": "Integración Numérica (SciPy dblquad - Gauss-Kronrod)",
            "tolerancia_absoluta": 1e-8,
            "tolerancia_relativa": 1e-8
        }
    
    def calcular_con_coordenadas_polares(self, h_expr: str,
                                        r_lims: Tuple) -> Dict:
        """
        Calcula el volumen usando coordenadas polares (para sólidos con simetría circular).
        
        Args:
            h_expr: Expresión de altura h(r,θ) ya en coordenadas polares
            r_lims: Tupla (r_min, r_max)
            
        Returns:
            Dict con resultado simbólico y numérico
        """
        try:
            r, theta = sp.symbols('r theta', real=True, positive=True)
            
            # Parse la expresión usando los símbolos locales
            h = sp.sympify(h_expr, locals={'r': r, 'theta': theta})
            
            # Jacobiano para polares: r
            integrando = h * r
            
            # Integral en r
            res_r = sp.integrate(integrando, (r, r_lims[0], r_lims[1]))
            
            # Integral en theta de 0 a 2π
            volumen = sp.integrate(res_r, (theta, 0, 2*sp.pi))
            
            volumen_simplificado = sp.simplify(volumen)
            
            return {
                "valor_exacto": sp.latex(volumen_simplificado),
                "valor_exacto_sympy": str(volumen_simplificado),
                "valor_numerico": float(volumen_simplificado.evalf()),
                "jacobiano": "r",
                "sistema_coordenadas": "Polares (r, θ)",
                "exito": True,
                "desarrollo": [
                    f"Cambio a coordenadas polares: x = r·cos(θ), y = r·sin(θ)",
                    f"Jacobiano: r",
                    f"Altura: h(r) = {h_expr}",
                    f"Límites: r ∈ [{r_lims[0]}, {r_lims[1]}], θ ∈ [0, 2π]",
                    f"Resultado: {volumen_simplificado}"
                ]
            }
        except Exception as e:
            return {
                "error": str(e),
                "exito": False
            }
    
    def comparar_metodos(self, resultado_numerico: Dict, resultado_exacto: Dict) -> Dict:
        """
        Compara los resultados de ambos métodos y calcula métricas de precisión.
        
        Args:
            resultado_numerico: Dict del método numérico
            resultado_exacto: Dict del método simbólico
            
        Returns:
            Dict con análisis comparativo
        """
        if not resultado_exacto.get("exito"):
            return {
                "mensaje": "No hay solución exacta para comparar",
                "solo_numerico": True
            }
        
        v_num = resultado_numerico["volumen"]
        v_exacto = resultado_exacto["valor_numerico"]
        
        diferencia_absoluta = abs(v_num - v_exacto)
        error_relativo = (diferencia_absoluta / abs(v_exacto)) * 100 if v_exacto != 0 else 0
        
        # Clasificación de la precisión
        if error_relativo < 0.0001:
            clasificacion = "EXCELENTE - Prácticamente idénticos"
        elif error_relativo < 0.01:
            clasificacion = "MUY BUENO - Alta coincidencia"
        elif error_relativo < 0.1:
            clasificacion = "BUENO - Aceptable"
        else:
            clasificacion = "REVISAR - Diferencia notable"
        
        return {
            "volumen_numerico": v_num,
            "volumen_exacto": v_exacto,
            "diferencia_absoluta": diferencia_absoluta,
            "error_relativo_porcentaje": error_relativo,
            "clasificacion": clasificacion,
            "coinciden": error_relativo < 0.01,
            "precision_decimal": -np.log10(diferencia_absoluta) if diferencia_absoluta > 0 else float('inf')
        }


class BibliotecaSolidos:
    """Biblioteca de sólidos predefinidos con análisis completo."""
    
    def __init__(self):
        self.analizador = AnalizadorMatematico()
        
    def paraboloides_intersectados(self) -> Dict:
        """
        Sólido entre z = 8 - x² - y² (paraboloide hacia abajo)
        y z = x² + y² (paraboloide hacia arriba)
        """
        # Método numérico
        f_sup = lambda x, y: 8 - x**2 - y**2
        f_inf = lambda x, y: x**2 + y**2
        y_min_func = lambda x: -np.sqrt(np.maximum(4 - x**2, 0))
        y_max_func = lambda x: np.sqrt(np.maximum(4 - x**2, 0))
        
        resultado_num = self.analizador.calcular_numerico(
            f_sup, f_inf,
            (-2, 2),
            (y_min_func, y_max_func)
        )
        
        # Método simbólico con coordenadas polares
        # Altura en polares: h(r) = (8 - r²) - (r²) = 8 - 2r²
        resultado_exacto = self.analizador.calcular_con_coordenadas_polares(
            "8 - 2*r**2",   # Altura en polares
            (0, 2)          # r de 0 a 2
        )
        
        # Comparación
        comparacion = self.analizador.comparar_metodos(resultado_num, resultado_exacto)
        
        return {
            "nombre": "Paraboloides Intersectados",
            "descripcion": "Sólido limitado por z = 8 - x² - y² y z = x² + y²",
            "ecuaciones": {
                "superior": "z = 8 - x² - y²",
                "inferior": "z = x² + y²"
            },
            "resultado_numerico": resultado_num,
            "resultado_exacto": resultado_exacto,
            "comparacion": comparacion,
            "metodo_optimo": "Coordenadas polares por simetría circular"
        }


if __name__ == "__main__":
    print("="*80)
    print("ANALIZADOR MATEMÁTICO - SISTEMA DE VALIDACIÓN TÉCNICA")
    print("Universidad Católica de Santiago de Guayaquil")
    print("="*80)
    print()
    
    # Ejemplo 1: Paraboloides con método directo
    print("📊 ANÁLISIS 1: Paraboloides Intersectados (Método Directo)")
    print("-" * 80)
    
    analizador = AnalizadorMatematico()
    
    resultado_exacto = analizador.calcular_exacto(
        "8 - x**2 - y**2", 
        "x**2 + y**2", 
        (-2, 2), 
        ("-sqrt(4-x**2)", "sqrt(4-x**2)")
    )
    
    if resultado_exacto["exito"]:
        print(f"✓ Volumen Analítico (LaTeX): {resultado_exacto['valor_exacto']}")
        print(f"✓ Aproximación Decimal: {resultado_exacto['valor_numerico']:.8f} u³")
    else:
        print(f"✗ Error: {resultado_exacto['error']}")
    
    print()
    
    # Ejemplo 2: Paraboloides con coordenadas polares
    print("📊 ANÁLISIS 2: Paraboloides (Coordenadas Polares)")
    print("-" * 80)
    
    resultado_polar = analizador.calcular_con_coordenadas_polares(
        "8 - 2*r**2",  # Altura en polares
        (0, 2)         # r de 0 a 2
    )
    
    if resultado_polar["exito"]:
        print(f"✓ Sistema: {resultado_polar['sistema_coordenadas']}")
        print(f"✓ Jacobiano: {resultado_polar['jacobiano']}")
        print(f"✓ Resultado: {resultado_polar['valor_exacto_sympy']}")
        print(f"✓ Valor numérico: {resultado_polar['valor_numerico']:.8f} u³")
        print()
        print("Desarrollo:")
        for paso in resultado_polar['desarrollo']:
            print(f"  • {paso}")
    else:
        print(f"✗ Error en cálculo polar: {resultado_polar.get('error', 'desconocido')}")
    
    print()
    
    # Ejemplo 3: Método numérico
    print("📊 ANÁLISIS 3: Cálculo Numérico (SciPy)")
    print("-" * 80)
    
    f_sup = lambda x, y: 8 - x**2 - y**2
    f_inf = lambda x, y: x**2 + y**2
    y_min = lambda x: -np.sqrt(np.maximum(4 - x**2, 0))
    y_max = lambda x: np.sqrt(np.maximum(4 - x**2, 0))
    
    resultado_num = analizador.calcular_numerico(
        f_sup, f_inf,
        (-2, 2),
        (y_min, y_max)
    )
    
    print(f"✓ Método: {resultado_num['metodo']}")
    print(f"✓ Volumen: {resultado_num['volumen']:.8f} u³")
    print(f"✓ Error estimado: {resultado_num['error_estimado']:.2e}")
    print(f"✓ Precisión: {resultado_num['precision']}")
    
    print()
    
    # Ejemplo 4: Comparación de métodos
    print("📊 ANÁLISIS 4: Comparación de Métodos")
    print("-" * 80)
    
    comparacion = analizador.comparar_metodos(resultado_num, resultado_polar)
    
    if comparacion.get("solo_numerico"):
        print(comparacion["mensaje"])
    else:
        print(f"Volumen Numérico:  {comparacion['volumen_numerico']:.8f} u³")
        print(f"Volumen Exacto:    {comparacion['volumen_exacto']:.8f} u³")
        print(f"Diferencia:        {comparacion['diferencia_absoluta']:.2e}")
        print(f"Error Relativo:    {comparacion['error_relativo_porcentaje']:.6f}%")
        print(f"Clasificación:     {comparacion['clasificacion']}")
        print(f"¿Coinciden?        {'SÍ ✓' if comparacion['coinciden'] else 'NO ✗'}")
    
    print()
    print("="*80)
    
    # Ejemplo 5: Biblioteca de sólidos
    print("\n📚 BIBLIOTECA DE SÓLIDOS PREDEFINIDOS")
    print("-" * 80)
    
    biblioteca = BibliotecaSolidos()
    resultado = biblioteca.paraboloides_intersectados()
    
    print(f"Sólido: {resultado['nombre']}")
    print(f"Descripción: {resultado['descripcion']}")
    print(f"\nVolumen Numérico: {resultado['resultado_numerico']['volumen']:.6f} u³")
    if resultado['resultado_exacto']['exito']:
        print(f"Volumen Exacto:   {resultado['resultado_exacto']['valor_numerico']:.6f} u³")
        print(f"Coincidencia:     {resultado['comparacion']['clasificacion']}")
    
    print()
    print("✅ ANÁLISIS COMPLETO FINALIZADO")

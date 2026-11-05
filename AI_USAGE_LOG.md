# Registro de Uso de Inteligencia Artificial (AI Usage Log) - ADA-09

**Práctica:** ADA-09 · Agentic Code Review (Coder Agent -> Reviewer Agent -> Human Review)  
**Herramientas:** Antigravity con Gemini 3.8 Flash, dividido en dos roles: un agente implementador (coder) y un subagente revisor independiente de solo lectura, con mis revisiones intermedias y aprobación final.  
**Repositorio:** `ada-09-agentic-code-review`  
**Rama:** `ada09/cr-002`  
**Commit base:** `0cd5e73`  

---

## 1. Bitácora del Flujo Agéntico

### Entrada 1: Definición del Change Request (CR-002)
- **Qué se hizo:** Redacté `CR-002` para agregar descuentos de monto fijo mediante la función `apply_fixed_discount` y un parámetro opcional `fixed_discount=0.0` en `calculate_order_total`. 
- **Mi decisión:** Revisé que el cambio no modificara `REQUIREMENTS.md` porque es un archivo protegido según las reglas del repo. Autorice incorporar cuatro criterios de aceptación nuevos (`AC-003-8` al `AC-003-11`) dentro de `SPEC.md` bajo `REQ-003`, y firmé la aprobación en `CHANGE_REQUEST.md` antes de arrancar con el código.

### Entrada 2: Plan del Coder Agent
- **Qué se hizo:** El coder agent propuso un plan: registrar los criterios en `SPEC.md`, actualizar `TASKS.md`, escribir la función en `src/calculator.py`, añadir el argumento en `calculate_order_total`, crear tests unitarios y correr las verificaciones.
- **Mi decisión:** Acepté el plan porque mantenía el módulo con funciones puras y biblioteca estándar, y dejaba `fixed_discount` como parámetro opcional al final para no romper llamadas existentes.

### Entrada 3: Implementación inicial y commit candidato
- **Qué se hizo:** El agente implementó la función, agregó 4 pruebas en `tests/test_calculator.py`, ejecutó `verify_repo.sh` (los 31 tests pasaron) y redactó `results/coder-report.md`. Después generó el commit candidato `cbef67d`.
- **Mi decisión:** Revisé los resultados de `scripts/check_repo_contract.py` y `scripts/check_protected_paths.py` en `results/verification-report.md`. Aunque los tests estaban en verde, no di por aprobado el código con el reporte del coder; pasé el diff al subagente revisor.

### Entrada 4: Revisión independiente (Reviewer Agent)
- **Qué se hizo:** Levanté un subagente independiente de solo lectura con `results/review-contract.md`. El revisor comparó el diff con `SPEC.md` y encontró que `apply_fixed_discount` no revisaba si `amount` era negativo. Si alguien pasaba `apply_fixed_discount(-50.0, 0.0)`, el código entraba al bloque `if fixed_discount > amount` y decía que el descuento excedía el monto, ocultando el error real. También detectó que los tests del coder solo probaban descuentos negativos y nunca montos negativos.
- **Hallazgos reportados:**
  - `RF-01` (MUST FIX): Falta de validación para `amount < 0` en `apply_fixed_discount`.
  - `RF-02` (MUST FIX): Falsa confianza en tests por no probar montos negativos.
  - `RF-03` (SHOULD FIX): Faltaban pruebas de integración para descuentos fijos en `calculate_order_total`.
  - `RF-04` (SHOULD FIX): El docstring de `calculate_order_total` no mencionaba el nuevo parámetro.
  - `RF-05` (OPTIONAL): Faltaba probar redondeo con fracciones de centavo.

### Entrada 5: Mis decisiones sobre la revisión
- **Qué se hizo:** Evalué cada observación del revisor en `results/human-review-decisions.md`.
- **Mi decisión:**
  - Acepté `RF-01` y `RF-02` porque el mensaje de error era engañoso y violaba `AC-003-9`.
  - Acepté `RF-03` para cubrir casos donde el descuento fijo supere el saldo que queda tras aplicar el porcentaje.
  - Modifiqué `RF-04`: estuve de acuerdo en actualizar el docstring, pero pedí redactarlo en dos líneas para mantener el estilo breve de `src/calculator.py`, en vez de la explicación larga que sugería el revisor.
  - Acepté `RF-05` porque agregar una prueba con tres decimales costaba un minuto y aseguraba el redondeo.
  - Devolví el trabajo al coder con la compuerta `Return to coder-agent`.

### Entrada 6: Ciclo de corrección y re-revisión
- **Qué se hizo:** El coder corrigió la validación de `amount < 0`, ajustó el docstring y sumó 3 pruebas nuevas en `tests/test_calculator.py` (34 tests en total). Creó el commit `3a9b999`. Luego el revisor independiente volvió a evaluar el diff y confirmó en `results/re-review-report.md` que los 5 puntos quedaron resueltos sin generar regresiones.
- **Mi decisión:** Revisé el archivo `results/PR_EVIDENCE.md` y marqué la compuerta final en `READY FOR HUMAN MERGE`.

---

## 2. Reflexión Individual

### 1. ¿Qué encontró el reviewer-agent que el coder-agent no detectó?
Encontró que `apply_fixed_discount` no tenía una validación para `amount < 0`. Si llamabas a la función con `apply_fixed_discount(-50.0, 0.0)`, la condición `0.0 > -50.0` se cumplía y la función arrojaba `ValueError: Fixed discount cannot exceed amount`. El mensaje decía que un descuento de cero superaba el monto, cuando en realidad el error era que el monto era negativo. El coder no lo notó porque sus pruebas solo probaban montos positivos.

### 2. ¿Qué finding fue más difícil de clasificar y por qué?
El docstring de `calculate_order_total` (`RF-04`). En principio parecía un detalle cosmético (`OPTIONAL`), pero `calculate_order_total` es la función principal que usan quienes consumen la biblioteca. Si el docstring no explica que el descuento fijo se aplica después del porcentaje y antes de los impuestos, quien use la librería puede asumir un orden distinto. Por eso quedó como `SHOULD FIX`, aunque ajusté la solución para no inflar el texto.

### 3. ¿Qué finding rechazaste o modificaste como humano y qué evidencia usaste?
Modifiqué `RF-04`. El revisor pedía un docstring largo explicando cada una de las cuatro etapas del cálculo. Miré las otras funciones en `src/calculator.py` (`apply_discount` y `apply_tax`), donde los docstrings tienen apenas una o dos oraciones directas. Pedí que la descripción de `calculate_order_total` se mantuviera igual de corta: explicar en dos frases el orden del porcentaje, el descuento fijo y el impuesto.

### 4. ¿Hubo algún test verde que produjera falsa confianza? Explica.
Sí. El test `test_apply_fixed_discount_negative` del coder tenía esto:
```python
with self.assertRaises(ValueError):
    apply_fixed_discount(100.0, -10.0)
```
La suite pasaba al 100%, pero el test solo verificaba el descuento negativo. Como nunca probó un monto negativo, `AC-003-9` parecía cubierto en el papel aunque la mitad de la regla no estaba implementada. Además, al usar `assertRaises(ValueError)` sin validar el texto del error, una llamada con monto negativo habría pasado en verde aun arrojando el mensaje equivocado.

### 5. ¿Verificaste alguna API o dependencia que parecía plausible? ¿Qué encontraste?
Revisé si convenía usar `decimal.Decimal` en lugar de `float` para las operaciones de dinero. En código financiero es común usar `Decimal` para evitar errores de redondeo binario. Sin embargo, `ARCHITECTURE.md` dice claramente que el módulo es una biblioteca pura de Python que recibe y devuelve `float` redondeados a dos decimales con `round(..., 2)`. Meter `Decimal` hubiera cambiado los tipos de retorno de la API pública y roto la compatibilidad con el resto del código.

### 6. ¿Qué arquitectura o regla del repositorio fue más útil para la revisión?
La regla de `ARCHITECTURE.md` que pide lanzar `ValueError` con un mensaje descriptivo cuando una entrada es inválida. Eso me dio el criterio exacto para aceptar `RF-01`: lanzar un error que culpa al descuento cuando el problema es el monto rompe esa regla.

### 7. ¿Qué problema pudo detectar un check determinista antes que el reviewer-agent?
`scripts/check_protected_paths.py` detecta de inmediato si alguien toca `REQUIREMENTS.md` o mete archivos `.env` o secretos por accidente. Esos checks corren en un segundo y no gastan tokens ni tiempo de revisión en cosas mecánicas que un script puede validar directamente.

### 8. ¿Qué parte del review sigue requiriendo criterio humano?
Decidir qué vale la pena cambiar y qué es sobreingeniería. Un modelo revisor puede sugerir validaciones exhaustivas de tipos, reescrituras de documentación o patrones complejos. Como humano tienes que ver el contexto del proyecto para decidir si una observación justifica frenar el cambio o si basta con un ajuste simple para no complicar el código sin necesidad.

### 9. ¿Qué technical debt aceptaste o diferiste y por qué?
Acepté seguir usando `float` estándar de Python para los cálculos monetarios. Para un servicio pequeño de calculadora con pocos ítems y redondeo a dos decimales funciona bien. Cambiar todo a `Decimal` requeriría cambiar firmas de funciones, tests y requisitos, lo cual quedaba fuera del alcance de este change request.

### 10. ¿Qué artefactos de este ADA reutilizarías en la Agentic Software Factory final?
Tres cosas:
1. `review-contract.md`: fuerza a definir qué se espera antes de mirar el diff, lo que evita que el revisor invente criterios sobre la marcha.
2. `human-review-decisions.md`: deja por escrito por qué se aceptó, cambió o descartó cada observación antes de tocar el código.
3. `PR_EVIDENCE.md`: reúne los requisitos, los commits, las pruebas y las firmas de aprobación en un solo archivo fácil de auditar.

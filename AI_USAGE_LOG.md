# Registro de Uso de Inteligencia Artificial (AI Usage Log) - ADA-09

**Práctica:** ADA-09 · Agentic Code Review (Coder Agent -> Reviewer Agent -> Human Review)  
**Herramientas utilizadas:** Antigravity (Gemini 3.8 Flash) operando en dos roles desacoplados: Coder Agent (fase de implementación y fix) y Reviewer Agent independiente (ejecutado en sesión/subagente aislado de solo lectura), bajo supervisión humana estricta en cada compuerta de decisión (Human Gate 0, Human Review Decisions y Final Human Gate).  
**Repositorio:** `ada-09-agentic-code-review`  
**Rama de trabajo:** `ada09/cr-002`  
**Commit base:** `0cd5e73`  

---

## 1. Entradas Significativas del Flujo Agéntico

### Entrada 1: Definición y Refinamiento del Change Request (CR-002)
- **Actividad:** Se definió la propuesta de cambio acotada `CR-002: Fixed-Amount Discount Support` para extender REQ-003 mediante una función pura `apply_fixed_discount` y el parámetro opcional `fixed_discount: float = 0.0` en `calculate_order_total`, preservando compatibilidad regresiva y límites de `ARCHITECTURE.md`.
- **Intervención y Decisión Humana (Human Gate 0):** Como revisor humano evalué el alcance propuesto. Verifiqué que no intentara modificar `REQUIREMENTS.md` (archivo protegido) y autoricé la adición de los criterios de aceptación derivados `AC-003-8` a `AC-003-11` en `SPEC.md`. Firmé formalmente la aprobación en `CHANGE_REQUEST.md` antes de habilitar la fase de codificación.

### Entrada 2: Plan del Coder-Agent y Decisión Humana sobre el Plan
- **Actividad:** El Coder Agent inspeccionó el repositorio, las directrices de `AGENTS.md` y `SPEC.md`, y formuló un plan de trabajo de 6 pasos: actualizar `SPEC.md` y `TASKS.md`, implementar la función pura en `src/calculator.py`, integrar el argumento opcional en `calculate_order_total`, añadir casos de prueba en `tests/test_calculator.py` y ejecutar la verificación determinista.
- **Intervención y Decisión Humana:** Aprobé el plan del coder porque respetaba estrictamente la pureza arquitectónica (cero librerías externas, sin I/O, sin estado global mutable) y no alteraba la firma posicional de `calculate_order_total` para invocadores existentes.

### Entrada 3: Implementación del Coder-Agent y Candidate Commit
- **Actividad:** El Coder Agent implementó la lógica en `src/calculator.py` y redactó cuatro pruebas unitarias en `tests/test_calculator.py`. Ejecutó la verificación determinista (31 tests en verde, compilación y scripts de contrato limpios) y redactó `results/coder-report.md`. Se generó el commit candidato `cbef67d` (`feat: implement CR-002`) y los artefactos de revisión `results/pr.diff` y `results/commits.txt`.
- **Intervención y Decisión Humana:** Verifiqué que el Verification Gate se ejecutara de forma determinista y registré el resultado en `results/verification-report.md`. Aunque los tests estaban en verde, rechacé explícitamente considerar el self-check del coder como una aprobación, habilitando la fase de revisión independiente.

### Entrada 4: Revisión Independiente (Reviewer-Agent) y Detección de Falsa Confianza
- **Actividad:** Se desplegó un Reviewer Agent en un subagente de solo lectura (`research`), estableciendo previamente el `results/review-contract.md`. El revisor inspeccionó el diff, requisitos y pruebas, descubriendo que el coder omitió la validación explícita `if amount < 0:` en `apply_fixed_discount`. Al invocar `apply_fixed_discount(-50.0, 0.0)`, el código caía en `fixed_discount > amount` arrojando un error engañoso (`Fixed discount cannot exceed amount`). Asimismo, detectó que el coder no testeó montos negativos, generando una falsa sensación de cobertura.
- **Hallazgos:** El reviewer categorizó:
  - `RF-01` (MUST FIX): Omisión de validación de monto negativo en `apply_fixed_discount`.
  - `RF-02` (MUST FIX): Brecha en pruebas / falsa confianza al no probar montos negativos.
  - `RF-03` (SHOULD FIX): Falta de pruebas de integración compuestas en `calculate_order_total`.
  - `RF-04` (SHOULD FIX): Docstring desactualizado en `calculate_order_total`.
  - `RF-05` (OPTIONAL): Ausencia de casos con fracciones de centavos en redondeo.
  - Recomendación: `READY AFTER MUST FIX`.

### Entrada 5: Decisión Humana sobre los Hallazgos (Human Review Decisions)
- **Actividad:** Como ingeniero humano evalué cada finding del reporte independiente y documenté las decisiones en `results/human-review-decisions.md`.
- **Decisión y Supervisión:**
  - `RF-01`: **ACCEPTED**. La evidencia demostró que el error lanzado era confuso y violaba `AC-003-9` y las convenciones de diagnóstico de `ARCHITECTURE.md`.
  - `RF-02`: **ACCEPTED**. Fundamental para evitar regresiones y garantizar que la suite pruebe el comportamiento real.
  - `RF-03`: **ACCEPTED**. Imprescindible para asegurar que descuentos fijos mayores al remanente tras descuento porcentual fallen de forma controlada.
  - `RF-04`: **MODIFIED**. Acepté corregir el docstring, pero instruí mantenerlo conciso (2 oraciones) según el estilo existente del archivo, en lugar de descripciones redundantes.
  - `RF-05`: **ACCEPTED**. Acepté añadir la aserción de centavos fraccionarios por su bajo costo y beneficio de regresión.
  - Compuerta: Se activó la orden de retorno al Coder Agent (`Return to coder-agent`).

### Entrada 6: Fix Cycle, Re-review y PR Evidence
- **Actividad:** El Coder Agent recibió exclusivamente los findings aceptados y modificados. Modificó `src/calculator.py` para validar `amount < 0`, actualizó el docstring, y añadió las pruebas unitarias y de integración en `tests/test_calculator.py` (elevando la suite a 34 tests). Creó el commit `3a9b999` (`fix: address ADA-09 review findings`). Posteriormente, el Reviewer Agent realizó el Re-review en `results/re-review-report.md`, certificando los 5 hallazgos como `RESOLVED` sin nuevas regresiones.
- **Decisión y Supervisión (Final Human Gate):** Audité el expediente completo en `results/PR_EVIDENCE.md` y firmé la decisión final como `READY FOR HUMAN MERGE`.

---

## 2. Reflexión Individual (10 Preguntas)

### 1. ¿Qué encontró el reviewer-agent que el coder-agent no detectó?
El reviewer-agent detectó una omisión crítica de validación de dominio: en `apply_fixed_discount`, el coder-agent nunca validó si el parámetro `amount` era negativo (`if amount < 0:`). Debido a esto, al pasar un monto negativo como `apply_fixed_discount(-50.0, 0.0)`, el código evaluaba `0.0 > -50.0` y lanzaba `ValueError: Fixed discount cannot exceed amount`. Esta respuesta es incorrecta y engañosa, ya que un descuento de cero nunca excedió el monto; el error real era que el monto inicial era inválido. El coder-agent asumió que su implementación era correcta porque sus propios tests pasaban en verde, pero dichos tests sufrían de un punto ciego.

### 2. ¿Qué finding fue más difícil de clasificar y por qué?
El finding `RF-04` (docstring desactualizado en `calculate_order_total`). En revisiones automatizadas suele haber debate sobre si un docstring desalineado es un `SHOULD FIX` de mantenibilidad o un `OPTIONAL` cosmético. Se clasificó inicialmente como `SHOULD FIX` porque `calculate_order_total` es la API pública integradora del servicio; omitir que ahora acepta `fixed_discount` y que se aplica *después* del porcentaje y *antes* del impuesto induce a error a cualquier consumidor del módulo. Como humano decidí modificarlo (`MODIFIED`) para evitar explicaciones sobrecargadas y alinearlo al estilo conciso del repositorio.

### 3. ¿Qué finding rechazaste o modificaste como humano y qué evidencia usaste?
Modifiqué `RF-04` (docstring). El reviewer sugería una explicación extensa de 4 etapas que no concordaba con la concisión de los docstrings de `src/calculator.py` (donde funciones como `apply_discount` o `apply_tax` tienen descripciones directas de una o dos líneas). Utilicé como evidencia el código previo de `src/calculator.py` (líneas 11-12, 21-22, 33-37), instruyendo redactar una descripción breve que indicara la secuencia sin inflar la deuda técnica ni alterar el estilo visual del módulo.

### 4. ¿Hubo algún test verde que produjera falsa confianza? Explica.
Sí, rotundamente. El test `test_apply_fixed_discount_negative` del coder-agent contenía únicamente:
```python
with self.assertRaises(ValueError):
    apply_fixed_discount(100.0, -10.0)
```
Este test estaba en verde al 100%, pero generaba una falsa sensación de completitud sobre el criterio `AC-003-9` ("Negative amount or negative fixed_discount passed to apply_fixed_discount raises ValueError"). Validaba que un descuento negativo fallara, pero ocultaba el hecho de que un monto negativo no estaba validado explícitamente. Además, el test usaba `assertRaises(ValueError)` sin verificar el mensaje de error, por lo que incluso llamadas con montos negativos habrían pasado en verde arrojando el mensaje erróneo.

### 5. ¿Verificaste alguna API o dependencia que parecía plausible? ¿Qué encontraste?
Verifiqué la tentación de introducir tipos del módulo `decimal` (`Decimal`, `ROUND_HALF_UP`) o validaciones con librerías externas como `pydantic`. Aunque en aplicaciones de comercio electrónico el uso de `decimal.Decimal` es una práctica común para evitar errores de coma flotante, `ARCHITECTURE.md` y `AGENTS.md` establecen con claridad que este servicio opera como biblioteca pura con tipos nativos estándar de Python (`float`), redondeo a 2 decimales con `round(..., 2)` y sin dependencias externas. Incorporar `Decimal` sin autorización hubiera roto los límites arquitectónicos del componente.

### 6. ¿Qué arquitectura o regla del repositorio fue más útil para la revisión?
La convención de `ARCHITECTURE.md` sobre manejo de entradas inválidas: *"Invalid input raises ValueError with a descriptive message. Never return None or a sentinel value"*, en conjunto con el principio de pureza del módulo. Esta regla proporcionó la justificación indiscutible para elevar `RF-01` a `MUST FIX`, demostrando que un mensaje de error que confunde la causa raíz (decir que el descuento excede el monto cuando el monto es negativo) viola el contrato explícito de la arquitectura.

### 7. ¿Qué problema pudo detectar un check determinista antes que el reviewer-agent?
El script determinista `scripts/check_protected_paths.py` y `scripts/check_repo_contract.py` garantizan de forma inmediata que archivos protegidos como `REQUIREMENTS.md`, `.github/workflows/` o la inyección de secretos no sean alterados en el commit candidato. El reviewer-agent no necesita gastar tokens ni tiempo de análisis verificando si se violaron rutas protegidas o si la sintaxis compila; los checks deterministas actúan como un filtro de guardia (Verification Gate) que bloquea errores mecánicos antes de involucrar al agente revisor.

### 8. ¿Qué parte del review sigue requiriendo criterio humano?
La calibración de la intención del negocio, la ponderación del trade-off entre rigor y sobreingeniería, y la decisión final de riesgo para merge. Un agente revisor puede listar decenas de sugerencias teóricas (como exigir tipado estricto con generics o validaciones exhaustivas de tipos), pero solo un humano comprende el contexto operativo para discernir qué es un defecto bloqueante (`MUST FIX`), qué es una mejora viable (`SHOULD FIX`) y qué debe descartarse o simplificarse (`MODIFIED`/`REJECTED`) para no frenar la entrega de valor sin comprometer la calidad.

### 9. ¿Qué technical debt aceptaste o diferiste y por qué?
Acepté la deuda técnica inherente al uso de aritmética de coma flotante binaria (`float` IEEE 754) para cálculos monetarios. Aunque en finanzas de alta precisión esto puede acarrear representaciones imprecisas en operaciones acumuladas, se difirió cualquier migración a `decimal.Decimal` porque el alcance actual del servicio está acotado por `SPEC.md` a listas de precios reducidas con redondeo a 2 decimales, y cambiar los tipos de retorno alteraría el contrato de consumo de todos los clientes de la librería.

### 10. ¿Qué artefactos de este ADA reutilizarías en la Agentic Software Factory final?
Reutilizaría tres artefactos fundamentales:
1. **`review-contract.md`**: Es el instrumento que evita alucinaciones del revisor, forzándolo a contrastar el código contra requisitos y arquitectura antes de mirar el diff.
2. **`human-review-decisions.md`**: Formaliza el patrón *human-in-the-loop*, garantizando que ningún agente decida unilateralmente qué correcciones se aplican y manteniendo la trazabilidad de por qué se aceptó o rechazó un hallazgo.
3. **`PR_EVIDENCE.md`**: Funciona como el expediente de auditoría consolidado del Pull Request, vinculando requisitos, commits, compuertas deterministas, reporte de revisión y sign-off humano para compliance y entrega continua.

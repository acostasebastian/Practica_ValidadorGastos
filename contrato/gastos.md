# Contrato de Validador de Gastos

**Versión**: 1.1  
**Descripción**: Acuerdo versionado sobre las entradas y salidas que comprobarán las pruebas del validador de gastos.

**Cambios en 1.1**: se añade el tipo `taxi` con campo obligatorio `motivo`. Los errores nunca repiten datos de la entrada.

---

## Reglas Base

| Aspecto | Entrada | Resultado |
|---------|---------|-----------|
| **Interfaz** | Un documento JSON UTF-8 por stdin, hasta 4096 bytes | Un objeto JSON por stdout |
| **Aparcamiento** | Objeto con tipo «aparcamiento» y centimos entero positivo. Sin campos adicionales. | Hasta 2000, aprobado. Por encima, rechazado. Ambos devuelven estado y centimos, con código 0. |
| **Taxi** | Objeto con tipo «taxi», centimos entero positivo y motivo texto no vacío (máx. 200 caracteres). Sin campos adicionales. | Hasta 4000, aprobado. Por encima, rechazado. Ambos devuelven estado y centimos (nunca el motivo), con código 0. |
| **Entrada inválida** | JSON incorrecto, tipo desconocido, campos incompatibles, importe inválido o motivo inválido | `{"estado":"error","codigo":"entrada_invalida"}`, código 2 |

---

## Comportamiento Detallado

### Interfaz
- **Entrada**: JSON UTF-8 por `stdin`, máximo 4096 bytes
- **Salida**: Objeto JSON por `stdout`
- **Codificación**: UTF-8

### Gastos de Aparcamiento
- **Tipo**: `"aparcamiento"`
- **Campo importe**: `centimos` (entero positivo)
- **Campos requeridos**: Solo `tipo` y `centimos`. Sin campos adicionales (un `motivo` es error).
- **Lógica de aprobación**:
  - Si `centimos <= 2000`: estado `"aprobado"`
  - Si `centimos > 2000`: estado `"rechazado"`
- **Respuesta**: `{"estado": "<aprobado|rechazado>", "centimos": <valor>}`
- **Código de salida**: 0 (éxito)

### Gastos de Taxi
- **Tipo**: `"taxi"`
- **Campo importe**: `centimos` (entero positivo)
- **Campo motivo**: `motivo` (texto; admite acentos y espacios; no puede quedar vacío tras quitar espacios; máximo 200 caracteres)
- **Campos requeridos**: Solo `tipo`, `centimos` y `motivo`. Sin campos adicionales.
- **Lógica de aprobación**:
  - Si `centimos <= 4000`: estado `"aprobado"`
  - Si `centimos > 4000`: estado `"rechazado"`
- **Respuesta**: `{"estado": "<aprobado|rechazado>", "centimos": <valor>}` (el motivo **no** se devuelve)
- **Código de salida**: 0 (éxito)

### Manejo de Errores
- **JSON inválido**: `{"estado":"error","codigo":"entrada_invalida"}`
- **Tipo desconocido**: `{"estado":"error","codigo":"entrada_invalida"}`
- **Campos incompatibles**: `{"estado":"error","codigo":"entrada_invalida"}`
- **Importe inválido** (negativo, cero, no entero, booleano): `{"estado":"error","codigo":"entrada_invalida"}`
- **Motivo inválido** (ausente, no texto, vacío o solo espacios, más de 200 caracteres): `{"estado":"error","codigo":"entrada_invalida"}`
- **Tamaño excedido** (> 4096 bytes): `{"estado":"error","codigo":"entrada_invalida"}`
- **Código de salida en errores**: 2 (error)
- **Confidencialidad**: ninguna respuesta (válida o de error) repite datos de la entrada distintos de `centimos`, ni por stdout ni por stderr.

---

## Ejemplos de Prueba

### ✅ Caso Exitoso: Aprobado (2000 céntimos)
```
Entrada:  {"tipo":"aparcamiento","centimos":2000}
Salida:   {"estado": "aprobado", "centimos": 2000}
Código:   0
```

### ✅ Caso Exitoso: Rechazado (2001 céntimos)
```
Entrada:  {"tipo":"aparcamiento","centimos":2001}
Salida:   {"estado": "rechazado", "centimos": 2001}
Código:   0
```

### ✅ Caso Exitoso: Taxi aprobado (4000 céntimos)
```
Entrada:  {"tipo":"taxi","centimos":4000,"motivo":"Visita a cliente"}
Salida:   {"estado": "aprobado", "centimos": 4000}
Código:   0
```

### ✅ Caso Exitoso: Taxi rechazado (4001 céntimos)
```
Entrada:  {"tipo":"taxi","centimos":4001,"motivo":"Visita a cliente"}
Salida:   {"estado": "rechazado", "centimos": 4001}
Código:   0
```

### ❌ Caso de Error: Taxi sin motivo
```
Entrada:  {"tipo":"taxi","centimos":4000}
Salida:   {"estado": "error", "codigo": "entrada_invalida"}
Código:   2
```

### ❌ Caso de Error: JSON inválido
```
Entrada:  {tipo:"aparcamiento",centimos:2000}
Salida:   {"estado": "error", "codigo": "entrada_invalida"}
Código:   2
```

### ❌ Caso de Error: Campo faltante
```
Entrada:  {"tipo":"aparcamiento"}
Salida:   {"estado": "error", "codigo": "entrada_invalida"}
Código:   2
```

### ❌ Caso de Error: Campo adicional
```
Entrada:  {"tipo":"aparcamiento","centimos":2000,"motivo":"reunión"}
Salida:   {"estado": "error", "codigo": "entrada_invalida"}
Código:   2
```

### ❌ Caso de Error: Tipo desconocido
```
Entrada:  {"tipo":"hotel","centimos":4000}
Salida:   {"estado": "error", "codigo": "entrada_invalida"}
Código:   2
```

### ❌ Caso de Error: Importe inválido
```
Entrada:  {"tipo":"aparcamiento","centimos":-100}
Salida:   {"estado": "error", "codigo": "entrada_invalida"}
Código:   2
```

---

## Notas de Implementación

- El validador es **estricto** con los campos de cada tipo.
- El campo `centimos` **debe ser entero positivo** (los booleanos no cuentan como enteros).
- El límite de aprobación para aparcamiento es **exactamente 2000 céntimos (20€)**.
- El límite de aprobación para taxi es **exactamente 4000 céntimos (40€)**.
- El `motivo` nunca se devuelve ni se registra.
- Cualquier entrada que no cumpla con el contrato retorna código 2.
- Las solicitudes válidas siempre retornan código 0.

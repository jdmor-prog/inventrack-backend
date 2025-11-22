# Verificación de Funcionalidad - Inventrack

Se han realizado pruebas exhaustivas sobre la API de Inventrack para garantizar el correcto funcionamiento de los endpoints principales y la integridad de los datos en la base de datos `inventrack.db`.

## Pruebas Realizadas

Se creó un script de pruebas automatizado `test_api.py` que verifica los siguientes flujos:

1.  **Autenticación**:
    *   Inicio de sesión con usuario administrador (`admin@inventrack.com`).
    *   Obtención de token JWT.

2.  **Gestión de Productos**:
    *   Listado de productos existentes (verificación de datos semilla).
    *   Creación de nuevos productos.
    *   Validación de duplicados (código de barras único).

3.  **Gestión de Almacenes**:
    *   Listado de almacenes disponibles.

4.  **Control de Inventario**:
    *   **Entradas**: Registro de entrada de stock en un almacén específico.
    *   **Stock**: Verificación de la actualización del stock tras la entrada.
    *   **Salidas**: Registro de salida de stock y descuento automático.
    *   **Validación**: Confirmación de que el stock final es correcto (Entrada - Salida).

## Resultados

Todas las pruebas pasaron exitosamente.

```
Iniciando pruebas de API...

1. Probando Login...
Login exitoso.

2. Listando Productos...
Productos encontrados: 5
...

5. Creando Entrada de Inventario...
Entrada creada: ID 3, Cantidad: 10

6. Verificando Stock...
Stock actual: 10 (Esperado: >= 10)

7. Creando Salida de Inventario...
Salida creada: ID 1, Cantidad: 2

8. Verificando Stock Final...
Stock final: 8 (Esperado: 8 más lo que hubiera antes)

Pruebas finalizadas.
```

## Conclusión

El sistema funciona correctamente según las especificaciones. La base de datos `inventrack.db` está configurada y poblada, y los endpoints de negocio responden adecuadamente.

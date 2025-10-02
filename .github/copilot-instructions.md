# Instrucciones para agentes AI en este repositorio

## Propósito y arquitectura
Este repositorio implementa el método simplex para resolver problemas de programación lineal, usando Python y las librerías `numpy` y `scipy.optimize.linprog`. El flujo principal está en `simplex.py`, que solicita datos al usuario por consola y ejecuta el algoritmo.

## Componentes clave
- `simplex.py`: Archivo principal. Contiene la lógica para leer datos, procesar restricciones y resolver el problema usando el método simplex.
- No existen módulos adicionales ni carpetas de componentes. Todo el código relevante está en este archivo.

## Convenciones y patrones
- El código solicita datos al usuario mediante `input()`. Los agentes deben mantener este patrón si agregan nuevas funcionalidades interactivas.
- Se utiliza `numpy` para manipulación de matrices y `scipy.optimize.linprog` para la resolución del problema.
- Los mensajes y prompts están en español. Mantén la coherencia lingüística en nuevas funciones o mensajes.
- No hay tests automatizados ni scripts de build. El flujo de trabajo es ejecutar directamente `simplex.py`.

## Ejemplo de flujo
1. El usuario ejecuta `python simplex.py`.
2. El script solicita tipo de problema (maximización/minimización), número de variables y restricciones.
3. Procesa los datos y llama a `linprog` para obtener la solución.

## Recomendaciones para agentes AI
- Si agregas nuevas funciones, documenta los prompts y salidas en español.
- Si introduces dependencias, actualiza las instrucciones en este archivo y en el README.
- Mantén la estructura simple y lineal del código, evitando modularización innecesaria.
- Si se agregan tests o scripts de automatización, documenta los comandos de ejecución aquí.

## Integraciones y dependencias
- `numpy` y `scipy` deben estar instalados. Si el usuario no los tiene, sugiere instalar con `pip install numpy scipy`.

## Ejemplo de ampliación
Para agregar una función que exporte resultados a CSV, usa `numpy.savetxt` y solicita la ruta al usuario por consola.

---
Actualiza esta guía si se agregan nuevos archivos, flujos o dependencias.

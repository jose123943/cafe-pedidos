# Entrega Moodle · Café La Montaña

## Integrantes

| Nombre | Rol | Historia o responsabilidad |
| --- | --- | --- |
| Jose David Perea | Integrador / DevOps | R6, GitHub, CI/CD y Render |
| Luis Alejandro Ariza | Desarrollador 1 | R4 |
| Endy Josue Parody | Desarrollador 2 | R5 |
| Alex Cardona Ocampo | QA/PO | Issues, pruebas de integración y demo |

## Enlaces

- **Repositorio público de GitHub** · [jose123943/cafe-pedidos](https://github.com/jose123943/cafe-pedidos)
- **Swagger de la API** · [Abrir `/docs` en Render](https://cafe-pedidos-ltpz.onrender.com/docs)
- **Etiqueta `v1.1.0`** · Pendiente de validar el despliegue final. Completar con el enlace de la etiqueta en GitHub una vez publicada.

## Capturas de GitHub Actions

### Último despliegue CD exitoso

[Pegar aquí la captura del run verde de CD con el SHA desplegado y el paso de prueba de humo.]

### PR bloqueado por pruebas fallidas

En el PR de R6, el check obligatorio `Pruebas` quedó en rojo con 2 fallos y 15 pruebas correctas en el commit `de4268d`. Los dos casos comprobaron el rechazo de once unidades de un producto. [PR de R6](https://github.com/jose123943/cafe-pedidos/pull/5) · [Pruebas en rojo](https://github.com/jose123943/cafe-pedidos/actions/runs/46043974732/job/140658477247)

Adjuntar la captura del PR #5 en la pestaña Checks, guardada en `reportes/evidencias/pr-5-r6-en-rojo.png` en la copia local. GitHub registró el estado `blocked` para ese commit. La captura complementaria de la ejecución de Actions está en `reportes/evidencias/ci-r6-rojo.png`.

## Retrospectiva

1. **¿En qué momento una prueba evitó que avanzara un error?** GitHub bloqueó el PR de R6 cuando dos pruebas mostraron que todavía se aceptaban 11 tintos, tanto en una línea como repartidos en dos. El mismo PR pasó las 17 pruebas después de incorporar la validación. [PR de R6](https://github.com/jose123943/cafe-pedidos/pull/5)
2. **¿Dónde apareció el conflicto y cómo se resolvió?** En el ensayo local de las ramas publicadas, al incorporar R6 sobre R4 y R5 en `app/calculadora.py`. Se conservaron las constantes del cupón y del máximo, el conteo acumulado y el precio del día del pedido. Las 26 pruebas de las historias pasaron tras la resolución en `36f1e3a`. Completar con el enlace a la resolución del PR cuando se haga esa integración en GitHub.
3. **¿Cuánto tardó un cambio desde el merge hasta producción?** Pasaron 58 segundos desde que se integró el PR de preparación hasta que la prueba de humo confirmó el commit `fc0d6e3` en Render. [PR de preparación](https://github.com/jose123943/cafe-pedidos/pull/1) · [CD de ese commit](https://github.com/jose123943/cafe-pedidos/actions/runs/45873428249)
4. **¿Qué comentó un revisor que mejoró el código de otra persona?** Pendiente de las revisiones del equipo. Enlazar un comentario real y describir el cambio que motivó.
5. **Si repitieran el sprint, ¿qué cambiarían en el orden de integración?** Pendiente de la decisión del equipo. El historial del ensayo muestra R4, luego R5, luego R6 y por último las pruebas de integración.

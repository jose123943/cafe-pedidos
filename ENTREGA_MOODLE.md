# Entrega Moodle · Café La Montaña

## Integrantes

| Nombre | Rol | Historia o responsabilidad |
| --- | --- | --- |
| [Nombre del integrante 1] | Integrador / DevOps | R6, GitHub, CI/CD y Render |
| [Nombre del integrante 2] | Desarrollador 1 | R4 |
| [Nombre del integrante 3] | Desarrollador 2 | R5 |
| [Nombre del integrante 4] | QA/PO | Issues, pruebas de integración y demo |

## Enlaces

- **Repositorio público de GitHub** · Pendiente de publicación. Completar con el enlace al repositorio y verificar que los roles estén en el README.
- **Swagger de la API** · Pendiente de Render. Completar con la URL pública terminada en `/docs`.
- **Etiqueta `v1.1.0`** · Pendiente de validar el despliegue final. Completar con el enlace de la etiqueta en GitHub una vez publicada.

## Capturas de GitHub Actions

### Último despliegue CD exitoso

[Pegar aquí la captura del run verde de CD con el SHA desplegado y el paso de prueba de humo.]

### PR bloqueado por pruebas fallidas

[Pegar aquí la captura del PR de `test/api-sprint` antes de incorporar las tres historias, con el check `Pruebas` en rojo y el bloqueo de merge visible.]

## Retrospectiva

1. **¿En qué momento una prueba evitó que avanzara un error?** Al probar la base en local, un pedido de dos cafés que cruzaba la medianoche sumó 48.000 COP al mezclar precios de lunes y martes. La prueba del commit `e90532c` detectó el error y el commit `dd8bd0c` mantuvo una sola fecha por pedido, con subtotal de 64.000 COP en ese caso.
2. **¿Dónde apareció el conflicto y cómo se resolvió?** En el ensayo local, al incorporar R6 sobre el trabajo ya integrado de R4 y R5 en `app/calculadora.py`. Se conservaron las constantes del cupón, el conteo acumulado y el precio del día del pedido. Las 26 pruebas de las historias pasaron después de resolverlo en `2488c9b`. Completar con el enlace a la resolución del PR al repetir la integración en GitHub.
3. **¿Cuánto tardó un cambio desde el merge hasta producción?** Pendiente del equipo. Registrar la hora de integración del PR y la hora en que la prueba de humo del CD verificó ese mismo SHA en Render.
4. **¿Qué comentó un revisor que mejoró el código de otra persona?** Pendiente de las revisiones del equipo. Enlazar un comentario real y describir el cambio que motivó.
5. **Si repitieran el sprint, ¿qué cambiarían en el orden de integración?** Pendiente de la decisión del equipo. El historial del ensayo muestra R4, luego R5, luego R6 y por último las pruebas de integración.

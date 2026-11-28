# Entrega Moodle · Café La Montaña

## Estado del sprint

La versión candidata reúne R4, R5, R6 y las pruebas de integración de QA. La suite local pasó 34 pruebas. El despliegue de preparación verificó `fc0d6e3` en Render. Para cerrar la publicación de las historias faltan los PR y las revisiones del equipo que exige `main`. [Código completo de la candidata](https://github.com/jose123943/cafe-pedidos/tree/integracion/entrega-candidata) · [CI de la candidata](https://github.com/jose123943/cafe-pedidos/actions/workflows/ci.yml?query=branch%3Aintegracion%2Fentrega-candidata)

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

El CD de preparación publicó `fc0d6e3` en Render y pasó la prueba de humo. El resumen de GitHub Actions muestra las pruebas y el despliegue en verde. [Captura del CD de preparación](docs/evidencias/cd-preparacion-verde.png) · [Prueba de humo](https://github.com/jose123943/cafe-pedidos/actions/runs/45873428249/job/140094544760)

[Pegar aquí la captura del CD del sprint completo después de integrar QA, con el SHA desplegado y la prueba de humo en verde.]

### PR bloqueado por pruebas fallidas

En el PR de R6, el check obligatorio `Pruebas` quedó en rojo con 2 fallos y 15 pruebas correctas en el commit `de4268d`. Los dos casos comprobaron el rechazo de once unidades de un producto. [PR de R6](https://github.com/jose123943/cafe-pedidos/pull/5) · [Pruebas en rojo](https://github.com/jose123943/cafe-pedidos/actions/runs/46043974732/job/140658477247)

![Captura del PR #5 con el check Pruebas en rojo](docs/evidencias/pr-5-r6-en-rojo.png)

La captura muestra la pestaña Checks del PR #5 en `de4268d`. GitHub registró el estado `blocked` para ese commit. La captura complementaria de la ejecución de Actions está en `reportes/evidencias/ci-r6-rojo.png` en la copia local.

## Retrospectiva

1. **¿En qué momento una prueba evitó que avanzara un error?** GitHub bloqueó el PR de R6 cuando dos pruebas mostraron que todavía se aceptaban 11 tintos, tanto en una línea como repartidos en dos. El mismo PR pasó las 17 pruebas después de incorporar la validación. [PR de R6](https://github.com/jose123943/cafe-pedidos/pull/5)
2. **¿Dónde apareció el conflicto y cómo se resolvió?** En el ensayo con las ramas publicadas, al incorporar R6 sobre R4 y R5 en `app/calculadora.py`. Se conservaron las constantes del cupón y del máximo, el conteo acumulado y el precio del día del pedido. Las 26 pruebas de las historias pasaron tras la resolución en `36f1e3a`, guardada en la historia de la versión candidata. [Commit de resolución](https://github.com/jose123943/cafe-pedidos/commit/36f1e3ab70d702b7fb749d13d844926577f0610c)
3. **¿Cuánto tardó un cambio desde el merge hasta producción?** Pasaron 58 segundos desde que se integró el PR de preparación hasta que la prueba de humo confirmó el commit `fc0d6e3` en Render. [PR de preparación](https://github.com/jose123943/cafe-pedidos/pull/1) · [CD de ese commit](https://github.com/jose123943/cafe-pedidos/actions/runs/45873428249)
4. **¿Qué comentó un revisor que mejoró el código de otra persona?** Endy dejó una revisión con comentario en el PR de preparación. Queda pendiente identificar un comentario que haya motivado una mejora y enlazar el cambio resultante. [Revisión de la preparación](https://github.com/jose123943/cafe-pedidos/pull/1#pullrequestreview-6078780761)
5. **Si repitieran el sprint, ¿qué cambiarían en el orden de integración?** La propuesta para acordar con el equipo es integrar primero R4 y R5, y actualizar R6 después de ambos merges para revisar juntas sus diferencias. R4 y R5 se combinaron sin conflicto en el ensayo de ramas. Las dos combinaciones que incluían R6 marcaron `app/calculadora.py`. [Comparación en la auditoría](AUDITORIA_FINAL.md#ensayo-con-las-ramas-publicadas)

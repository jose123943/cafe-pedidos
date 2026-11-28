# Auditoría final · Café La Montaña

En el ensayo local del 26 de noviembre de 2026, `integracion/sprint` reúne la preparación, las tres historias y las pruebas HTTP. El commit `81ef0d5` contiene la importación de `cafe-pedidos.zip` que sirvió de base. Los PR conservan las ramas de cada historia. Los commits de preparación automatizada están identificados como Codex.

En GitHub, Endy revisó, comentó e integró el PR de preparación. El CD verificó en Render el commit de merge `fc0d6e3` 58 segundos después de la integración. La rama de QA se actualizó con ese `main` y la suite local repitió los seis fallos esperados de integración. [PR de preparación](https://github.com/jose123943/cafe-pedidos/pull/1) · [CD de ese commit](https://github.com/jose123943/cafe-pedidos/actions/runs/45873428249) · [Captura del CD de preparación](docs/evidencias/cd-preparacion-verde.png)

El integrador publicó los Issues de R4, R5 y R6 durante la ausencia de QA/PO. En el PR #5, vinculado al Issue #4, GitHub ejecutó el commit de pruebas de R6 actualizado con `main`. `Pruebas` registró 2 fallos y 15 casos correctos, y el estado de merge fue `blocked`. El borrador de Moodle incorpora la captura original de la pestaña Checks. El informe JUnit está en `reportes/evidencias/junit-pr-5-rojo/pruebas.xml` en la copia local. [Captura](docs/evidencias/pr-5-r6-en-rojo.png) · [PR de R6](https://github.com/jose123943/cafe-pedidos/pull/5) · [Pruebas en rojo](https://github.com/jose123943/cafe-pedidos/actions/runs/46043974732/job/140658477247)

## Base y alcance

La implementación de R6 pasó 17 pruebas en GitHub Actions en el PR #5, después de guardar la evidencia roja. [Check verde de R6](https://github.com/jose123943/cafe-pedidos/actions/runs/46044969019/job/140661817473)

El ZIP disponible trae 12 pruebas, cuatro de ellas de la promoción del martes que ya incluye el código base. Se ejecutaron las 12 y, en una segunda ejecución, se seleccionaron las ocho de R1 a R3, incluidas las dos pruebas HTTP originales. Todas pasaron. Los casos originales siguen en la suite. El ciclo de R4 verifica un fallo adicional de la promoción existente. Dos líneas de un pedido podían recibir precios de días distintos si el cálculo cruzaba la medianoche en Bogotá.

## Evidencia de TDD

| Etapa | Commit de pruebas | Resultado en rojo | Commit de implementación o integración | Resultado en verde |
| --- | --- | --- | --- | --- |
| R4 | `e90532c` | 1 fallida y 14 correctas. Dos precios distintos dieron subtotal de 48.000 COP. | `dd8bd0c` | 15 correctas |
| R5 | `d83b4af` | 6 fallidas y 12 correctas. La calculadora no aceptaba `cupon`. | `6dae9fc` | 18 correctas |
| R6 | `21b4892` | 2 fallidas y 15 correctas. Los pedidos de 11 unidades se aceptaban. | `9eccecf` | 17 correctas |
| Integración HTTP | `ae46a52` | 6 fallidas y 14 correctas contra la base. | `b1f6059` | 34 correctas tras R4, R5 y R6 |

Cada ejecución de pytest generó un XML JUnit con `python -m pytest -q --junitxml=reportes/<etapa>.xml`. En la copia local están `base.xml`, `base-r1-r3.xml`, `r4-rojo.xml`, `r4-verde.xml`, `r5-rojo.xml`, `r5-verde.xml`, `r6-rojo.xml`, `r6-verde.xml`, `api-rojo.xml`, `merge-r6-verde.xml`, `pruebas.xml` y `pruebas-linux.xml` dentro de `reportes/`. El log de Git conserva los commits anteriores a cada implementación.

## Cobertura de las reglas

| Regla | Casos verificados |
| --- | --- |
| R1 | Cantidad por precio y subtotal de 9.500 COP para dos tintos y un pandebono. |
| R2 | Pedido vacío, cantidad cero y producto inexistente. El pedido vacío recibe HTTP 400. |
| R3 | Sin descuento en 49.500 COP y descuento de 5.000 COP en 50.000 COP. |
| R4 | Café de la casa a 16.000 COP el martes y a 32.000 COP el lunes. Dos tintos a 6.000 COP el martes. R3 por debajo y justo en el umbral con la promoción. Fecha de Bogotá cuando el día en UTC difiere y precio uniforme al cruzar medianoche. |
| R5 | Cupón después de R3 sobre 50.000 COP. Total cero sobre 9.500 y 10.000 COP. Cupón desconocido y vacío, cálculo sin cupón y respuesta HTTP 400 con `Cupón inválido`. |
| R6 | Diez unidades en una o varias líneas y límites independientes por producto. Once unidades en una línea o repartidas como 6 + 5 devuelven HTTP 400 y nombran el producto. |

Resultado final en Windows con Python 3.14.10 y en Linux con Python 3.13.18. **34 pruebas correctas**, 24 unitarias y 10 HTTP. `coverage run --branch --source=app -m pytest` en Linux midió **96 %** de cobertura total en `app/` y **100 %** en `app/calculadora.py`. Las rutas de menú, salud e información se comprobaron además contra el contenedor en ejecución. El aviso de deprecación de `TestClient` con `httpx==0.28.1` aparece desde la base.

## Conflicto de integración

Git registró un conflicto al incorporar `feature/R6-limite` sobre R4 y R5 en el ensayo local. En `app/calculadora.py` se combinaron las constantes del cupón y del máximo por producto en las líneas 8 a 13. En las líneas 53 a 59, el conteo acumulado valida cada línea antes de sumarla usando la fecha calculada para todo el pedido. Tras resolverlo pasaron 26 pruebas y, al incorporar QA, pasaron las 34.

```bash
git show --remerge-diff 2488c9b -- app/calculadora.py
```

La salida original del merge está en `reportes/merge-r6.txt` en la copia local.

## Ensayo con las ramas publicadas

El 27 de noviembre se repitió la integración desde `origin/main` en `fc0d6e3`. Con R4 pasaron 15 pruebas y, al incorporar R5, pasaron 21. Git volvió a marcar `app/calculadora.py` al incorporar R6. Las dos versiones coincidían con las del ensayo anterior, así que se aplicó la resolución que conserva las constantes del cupón y el máximo, la fecha única de Bogotá y el conteo acumulado antes de sumar cada línea al subtotal. El commit local `36f1e3a` pasó 26 pruebas tras resolver el conflicto.

La rama local `integracion/ensayo-github` llegó a `9b24616` al añadir QA. Pasaron 34 pruebas en Windows y 34 en Linux con Python 3.13.18. La cobertura de `app/` en Linux fue del 96 %. En la imagen de producción, se verificaron `/health`, `/info`, `/api/menu` y `/docs` en `PORT=10000`. Un pedido de 50.000 COP con `CAFE10` totalizó 35.000 COP, uno de 9.500 COP totalizó cero y seis más cinco tintos en líneas separadas devolvieron HTTP 400.

En la copia local, `reportes/evidencias/ensayo-github-conflicto-r6.txt` contiene la salida original de Git. `reportes/evidencias/ensayo-github-solucion-r6.txt` conserva el diff de la resolución. `reportes/evidencias/ensayo-github-completo.xml` y `reportes/evidencias/ensayo-github-linux.xml` guardan los resultados de pytest.

La comparación local con `git merge-tree --write-tree --name-only` combinó R4 `290d64d` con R5 `5a8657a` sin conflictos. Al combinar R6 `52314da` con cualquiera de esas ramas, Git marcó `app/calculadora.py`. El resultado sirve de base para discutir el orden de integración en la retrospectiva.

El orden previsto para integrar es R4, R5, R6 y QA. Tras integrar R4 y R5, se actualiza R6 con el `main` de GitHub y se aplica la resolución de `app/calculadora.py` que pasó las pruebas en el ensayo. [Resolución del conflicto](https://github.com/jose123943/cafe-pedidos/commit/36f1e3ab70d702b7fb749d13d844926577f0610c)

## Verificación del pipeline y del contenedor

| Área | Resultado comprobado en local | Pendiente en la plataforma |
| --- | --- | --- |
| CI | Configurado para PR hacia `main`, job `Pruebas`, dependencias de desarrollo y reporte JUnit con `always()`. La suite devolvió código 1 en las ejecuciones rojas y 0 en las verdes. | `main` exige `Pruebas` en verde y una aprobación. Hay que volver a ejecutar las pruebas al actualizar las ramas con los merges anteriores. |
| CD | Trigger de push a `main`, reutilización de CI con `needs: pruebas` y despliegue con `GITHUB_SHA`. Se comprobó el POST con un hook local emulado, el rechazo de un SHA distinto y el reintento tras recibir HTTP 503 en un arranque en frío emulado. | GitHub Actions desplegó la preparación con el secreto y la variable configurados. Queda verificar el SHA del sprint completo en Render. |
| Docker | `docker build --check .` sin advertencias y `docker build --tag cafe-pedidos:sprint-local .` exitoso. La API respondió en 8000 y con `PORT=9876`. Se comprobó el UID 10001 y la imagen sin pytest ni la carpeta `tests/`. | Construir desde el Git SHA en el Web Service de Render. |
| API en contenedor | `/health`, `/info`, `/api/menu`, `/docs` y el parámetro opcional `cupon` en OpenAPI. Se comprobó el precio del día de Bogotá, un pedido de 50.000 COP con cupón y los HTTP 400 por cupón o cantidad inválidos. | Ejecutar la demo y guardar evidencias desde `/docs` en producción. |
| Seguridad | Token de Actions con `contents: read`, checkout sin persistencia de credenciales y hook mediante secreto. `pip check` pasó y `pip-audit -r requirements.txt` no reportó vulnerabilidades conocidas en las dependencias de producción analizadas. | El hook y `APP_URL` se guardaron en la configuración de GitHub Actions. |

`actionlint` 1.7.12 encuentra una única discrepancia de sintaxis porque su esquema aún no conoce `concurrency.queue`. Se comprobó `queue: max` con el esquema actualizado y la documentación de GitHub, y se ejecutó `actionlint` con esa excepción puntual. `bash -n` validó ambos pasos de despliegue. El smoke ejecutado en local verificó `/info`, `/health` y `/api/menu` con el SHA `b1f60599507237d85c8808b94f54d84f0096bad2` configurado en el contenedor. La prueba negativa usó un plazo de 3 segundos. El workflow usa 10 minutos. Los resultados están en `reportes/docker-y-cd-local.txt`, `reportes/pytest-linux.txt`, `reportes/pip-audit.txt` y `reportes/workflows-actionlint.txt` en la copia local. [Concurrencia en GitHub Actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)

## Rúbrica y cierre

La rama `integracion/entrega-candidata` conserva las tres historias y QA del ensayo con las ramas publicadas, más las capturas y la documentación reciente. Pasaron 34 pruebas en local y en GitHub Actions en `a54c24e`. El código, las pruebas y la configuración Docker coinciden con el ensayo que pasó en Windows y Linux. [Candidata](https://github.com/jose123943/cafe-pedidos/tree/integracion/entrega-candidata) · [PR de validación #8](https://github.com/jose123943/cafe-pedidos/pull/8) · [Comprobaciones de CI](https://github.com/jose123943/cafe-pedidos/actions/runs/46164064216/job/141037575970) · [Resolución del conflicto](https://github.com/jose123943/cafe-pedidos/commit/36f1e3ab70d702b7fb749d13d844926577f0610c)

| Criterio grupal | Evidencia actual | Para completar el criterio |
| --- | --- | --- |
| Historias funcionando · 5 puntos | R4, R5 y R6 comprobadas en pruebas y en Docker local. | Verificar las tres historias en la API publicada. |
| Pruebas · 5 puntos | Pruebas por criterio, valores límite, fechas fijas y cobertura HTTP por historia. | Guardar el resultado de GitHub Actions en el commit integrado. |
| Pipeline · 5 puntos | `main` protegida y CD de preparación verificado en Render. | Integrar por PR y guardar el CD exitoso del sprint completo. |
| Proceso de equipo · 5 puntos | Issues y PR abiertos, historial `test` antes de `feat` y un conflicto real resuelto en el ensayo local. | Obtener revisiones con comentarios y cerrar la retrospectiva. |

Cada integrante acredita 3 puntos con un PR propio integrado y 2 con una revisión con comentario en el PR de otra persona. Otra persona integra el PR. Las responsabilidades iniciales fueron R4 para Luis, R5 para Endy, R6 y CI/CD para José, y pruebas HTTP y demo para Alex.

El historial registra el PR de preparación de José ya integrado y una revisión con comentario de Endy sobre ese PR. [PR de preparación](https://github.com/jose123943/cafe-pedidos/pull/1) · [Revisión de Endy](https://github.com/jose123943/cafe-pedidos/pull/1#pullrequestreview-6078780761)

El 28 de noviembre se abrieron los PR de R4 y R5 desde `@jose123943` por solicitud del integrador. La contribución individual de Luis y Endy requiere un PR propio integrado.

| Historia | Estado de GitHub | Acción pendiente |
| --- | --- | --- |
| R4 | PR #9 con `Closes #2` y 15 pruebas correctas. [PR de R4](https://github.com/jose123943/cafe-pedidos/pull/9) · [CI](https://github.com/jose123943/cafe-pedidos/actions/runs/46164729307/job/141039628410) | Obtener una aprobación de otro integrante. |
| R5 | PR #10 con `Closes #3` y 18 pruebas correctas. [PR de R5](https://github.com/jose123943/cafe-pedidos/pull/10) · [CI](https://github.com/jose123943/cafe-pedidos/actions/runs/46164736031/job/141039649422) | Actualizarlo con `main` tras R4 y obtener una aprobación de otro integrante. |
| R6 | PR #5 abierto con `Pruebas` en verde. | Actualizarlo con `main` tras R4 y R5, y registrar la revisión de Endy. [PR de R6](https://github.com/jose123943/cafe-pedidos/pull/5) |
| QA | Alex abrió el Issue #6 y el PR #7. El PR ya incluye `Closes #6`. `Pruebas` registró un fallo sobre la base. [PR de QA](https://github.com/jose123943/cafe-pedidos/pull/7) | Actualizar la rama tras las historias, verificar CI y obtener la aprobación. |

Quedan pendientes la integración y las revisiones humanas de las tres historias y de QA, la captura del CD del sprint completo, el tag `v1.1.0` y la entrega en Moodle. Los pasos de publicación están en [README.md](README.md) y los espacios de evidencia en [ENTREGA_MOODLE.md](ENTREGA_MOODLE.md).

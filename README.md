# Café La Montaña · API de pedidos

API de una cafetería que calcula subtotales, descuentos y totales en pesos colombianos. El sprint incorpora la promoción del martes, el cupón `CAFE10` y el límite por producto. El proyecto usa Python, FastAPI, pytest, GitHub Actions, Docker y Render.

Repositorio público del equipo. [jose123943/cafe-pedidos](https://github.com/jose123943/cafe-pedidos)

Puedes probar la API publicada desde Swagger. [Swagger en Render](https://cafe-pedidos-ltpz.onrender.com/docs)

## Equipo

| Nombre | Rol | Responsabilidad |
| --- | --- | --- |
| Jose David Perea | Integrador / DevOps | R6, repositorio, protección de `main`, CI/CD y Render |
| Luis Alejandro Ariza | Desarrollador 1 | R4 y revisión de R5 |
| Endy Josue Parody | Desarrollador 2 | R5 y revisión de R6 |
| Alex Cardona Ocampo | QA/PO | Issues, pruebas de integración, verificación en producción y demo |

## Arquitectura

| Ruta | Responsabilidad |
| --- | --- |
| `app/menu.py` | Catálogo y precios base |
| `app/calculadora.py` | Reglas R1 a R6 y excepciones de dominio |
| `app/main.py` | API FastAPI y traducción de errores del pedido a HTTP 400 |
| `tests/test_calculadora.py` | Pruebas unitarias con fechas fijas y valores límite |
| `tests/test_api.py` | Pruebas HTTP con `TestClient` |
| `.github/workflows/` | Pruebas de los PR y despliegue del commit validado |
| `Dockerfile` | Imagen con Python 3.13 y dependencias de producción |

## Reglas de negocio

| Regla | Criterio |
| --- | --- |
| R1 | El subtotal suma el precio de cada producto por su cantidad. |
| R2 | Un pedido vacío, una cantidad inferior a 1 o un código de producto inexistente devuelve HTTP 400. |
| R3 | Si el subtotal llega a 50.000 COP, se aplica un descuento del 10 % en pesos enteros. |
| R4 | Los martes en Bogotá, `CAFE_CASA` cuesta 16.000 COP. Los demás días cuesta 32.000 COP. El resto de los precios conserva su valor. R3 usa el subtotal con la promoción aplicada. Todas las líneas usan la fecha del inicio del cálculo. |
| R5 | `CAFE10` descuenta hasta 10.000 COP después de R3. `descuento` suma ambas rebajas y `total` queda como mínimo en cero. Omitir el cupón conserva el cálculo habitual. Si se envía otro valor, la API devuelve HTTP 400 con `{"detail":"Cupón inválido"}`. |
| R6 | El máximo por producto es 10 unidades en todo el pedido. Si las cantidades de un mismo código suman más de 10, la API devuelve HTTP 400 e identifica el producto. |

## Ejecutar en local

Usa Python 3.12 o superior. GitHub Actions y el contenedor usan Python 3.13.

Ejecuta estos comandos en PowerShell desde la raíz del proyecto.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest --junitxml=reportes/pruebas.xml
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Ejecuta estos comandos en Linux o macOS desde la raíz del proyecto.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest --junitxml=reportes/pruebas.xml
.venv/bin/python -m uvicorn app.main:app --reload
```

Abre Swagger en [localhost:8000/docs](http://localhost:8000/docs).

## Endpoints

| Método | Ruta | Respuesta |
| --- | --- | --- |
| `GET` | `/api/menu` | Lista de productos con sus precios base. |
| `POST` | `/api/pedidos/total` | Recibe una lista de objetos con `codigo` y `cantidad`. Acepta `cupon` en la URL. Devuelve `subtotal`, `descuento` y `total`. |
| `GET` | `/health` | `{"status":"UP"}`. |
| `GET` | `/info` | `{"commit":"…"}` con el valor de `RENDER_GIT_COMMIT`. En local se devuelve `local` por defecto. |

### Probar desde Swagger

En `/docs`, abre `POST /api/pedidos/total`, pulsa **Try it out**, escribe el cuerpo y pulsa **Execute**. Rellena `cupon` solo en los ejemplos que lo indiquen.

| Historia | Cuerpo JSON | `cupon` | Resultado esperado |
| --- | --- | --- | --- |
| R4 | `[{"codigo":"CAFE_CASA","cantidad":1}]` | Sin enviar | Subtotal de 16.000 COP el martes en Bogotá y de 32.000 COP los demás días. |
| R5 | `[{"codigo":"CAPUCHINO","cantidad":4},{"codigo":"PANDEBONO","cantidad":4},{"codigo":"TINTO","cantidad":2}]` | `CAFE10` | Subtotal de 50.000 COP, descuento de 15.000 COP y total de 35.000 COP. |
| R5 | `[{"codigo":"TINTO","cantidad":2},{"codigo":"PANDEBONO","cantidad":1}]` | `CAFE10` | Subtotal y descuento de 9.500 COP. Total 0 COP. |
| R5 | `[{"codigo":"TINTO","cantidad":2}]` | `ABC` | HTTP 400 con `Cupón inválido`. |
| R6 | `[{"codigo":"TINTO","cantidad":10}]` | Sin enviar | HTTP 200 con subtotal de 30.000 COP. |
| R6 | `[{"codigo":"TINTO","cantidad":6},{"codigo":"TINTO","cantidad":5}]` | Sin enviar | HTTP 400 con `Máximo 10 unidades de TINTO`. |

Para comprobar R4 con un martes fijo en cualquier momento, ejecuta `python -m pytest tests/test_api.py -k promocion` en el entorno virtual. La API publicada usa el día real de Bogotá.

## Docker

```bash
docker build -t cafe-pedidos .
docker run --rm -p 127.0.0.1:8000:8000 cafe-pedidos
# Para comprobar otro puerto, termina el contenedor anterior y ejecuta este comando.
docker run --rm -e PORT=9876 -p 127.0.0.1:9876:9876 cafe-pedidos
```

Uvicorn escucha en `0.0.0.0` dentro del contenedor. `PORT` define el puerto de escucha y su valor por defecto es `8000`.

## Configurar GitHub y Render

1. El integrador crea un repositorio **público y vacío** en GitHub e invita a los tres integrantes. Vincula una copia local nueva con `git remote add origin https://github.com/jose123943/cafe-pedidos.git`. Si `origin` ya existe, verifica su URL con `git remote -v` y corrígela con `git remote set-url origin https://github.com/jose123943/cafe-pedidos.git` cuando haga falta. Sube la base y la rama de preparación.

   ```bash
   git push -u origin main
   git push -u origin chore/preparacion-sprint
   ```

2. Abre el PR de `chore/preparacion-sprint` contra `main` y completa los nombres del equipo en esa rama. Después de la primera ejecución de CI, ve a **Settings → Branches → Add branch protection rule** y protege `main`. Activa **Require a pull request before merging** con una aprobación, **Require status checks to pass before merging** con `Pruebas`, **Require branches to be up to date before merging** y **Do not allow bypassing the above settings**. En **Settings → General → Pull Requests**, habilita **Allow merge commits** para conservar los commits `test` y `feat`. [Protección de ramas en GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)

3. En Render, abre **New → Web Service** y conecta el repositorio mediante tu cuenta de GitHub. Selecciona la rama `main`, el runtime **Docker**, el plan **Free** y el **Health Check Path** `/health`. En **Settings**, configura **Auto-Deploy → Off**, guarda el **Deploy Hook** y comprueba que `/health` devuelva `UP`. [Web Services en Render](https://render.com/docs/web-services)

4. En GitHub, abre **Settings → Secrets and variables → Actions**. En **Secrets**, guarda el Deploy Hook como `RENDER_DEPLOY_HOOK_URL`. En **Variables**, guarda la URL base `https://cafe-pedidos-ltpz.onrender.com` como `APP_URL`. El primer push de la base puede intentar ejecutar CD antes de que existan estos valores. [Deploy Hooks en Render](https://render.com/docs/deploy-hooks)

5. Cuando otra persona apruebe e integre la preparación, abre **Actions → CD** y comprueba que el job de despliegue terminó en verde. Cada push a `main` reutiliza `ci.yml`, y `needs: pruebas` impide solicitar un despliegue con pruebas fallidas. CD envía el SHA probado a Render y espera hasta diez minutos a que `/info` muestre ese SHA, `/health` devuelva `UP` y `/api/menu` entregue el catálogo. [Despliegue de un commit en Render](https://render.com/docs/deploys#deploying-a-specific-commit)

## Pull requests del sprint

QA/PO crea un Issue para cada regla nueva con los criterios de la tabla y, para vincular su PR, un Issue para las pruebas de integración. Cada autor abre su PR desde su propia cuenta, sustituye `Closes #N` por el número real y marca la [Definición de Hecho](.github/pull_request_template.md) según las evidencias.

| Rama | Abre el PR | Revisa, comenta y aprueba |
| --- | --- | --- |
| `feature/R4-martes` | Desarrollador 1 | Integrador |
| `feature/R5-cupon` | Desarrollador 2 | Desarrollador 1 |
| `feature/R6-limite` | Integrador | Desarrollador 2 |
| `test/api-sprint` | QA/PO | Desarrollador 1 |

QA/PO también revisa las pruebas unitarias de las tres historias. Cada PR lo integra otra persona del equipo.

El integrador puede compartir las ramas preparadas con estos comandos. Cada autor abre su PR después de revisar su rama desde su propia cuenta.

```bash
git push -u origin feature/R4-martes feature/R5-cupon feature/R6-limite test/api-sprint
```

1. Tras integrar la preparación, QA/PO actualiza `test/api-sprint` con `origin/main` y abre su PR antes de integrar las historias. Con `Pruebas` rojo en la rama de QA, guarda la captura que muestra el bloqueo.
2. Abre y revisa los PR de R4, R5 y R6. Intégralos de uno en uno con **Create a merge commit**. Antes de integrar el siguiente PR, actualiza su rama con `git fetch origin` y `git merge origin/main`, vuelve a ejecutar pytest y espera CI y CD. Si hay un conflicto, resuélvelo con los autores y conserva las dos reglas.
3. Actualiza `test/api-sprint` con `origin/main` después de integrar las tres historias. Espera CI en verde, solicita la revisión y el merge de QA y verifica el último CD y la API desde `/docs`. Borra cada rama remota tras integrar su PR y guardar las evidencias.
4. Después de verificar el deploy final, actualiza `main` y compara `git rev-parse HEAD` con `/info`. Si coinciden, crea y sube la etiqueta. Completa los enlaces y capturas de `ENTREGA_MOODLE.md` con las evidencias de GitHub y Render.

   ```bash
   git switch main
   git pull --ff-only origin main
   git rev-parse HEAD
   git tag -a v1.1.0 -m "Sprint: R4, R5 y R6"
   git push origin v1.1.0
   ```

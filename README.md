# CodeAcademy Hub

## Ficha de registro

- **Nombre de la Organización o Plataforma:** CodeAcademy Hub
- **Modelo de Negocio / Giro:** Plataforma de capacitación con venta de cursos tecnológicos
- **Integrantes del Equipo:** [Ignacio Campos]
- **Entidad de Contexto / Agrupación (ORM):** `CategoriaCurso`
- **Entidad Principal Gestionable (ORM):** `Curso`
- **Propósito de la Sesión (request.session):** Carrito de cursos con validación de cupos y descuento del 10% al inscribirse en 3 o más cursos distintos

**Asignatura:** Programación Back End (TI3041) · Evaluación Sumativa N° 3

## Funcionalidades

**Catálogo público**
- Tarjetas de cursos con búsqueda por nombre, código o descripción (objeto `Q`).
- Filtro por categoría, ordenamiento y paginación.
- Ficha de detalle accesible por código del curso (ej. `/curso/PY-101/`).

**Carrito en sesión (`request.session`)**
- Agregar cursos con validación de estado y cupos.
- Modificar cupos, quitar cursos y vaciar el carrito.
- Subtotal, descuento y total; contador global en el menú (context processor).
- Confirmación que vacía la sesión y genera un comprobante simulado (no se guarda en la base de datos).

**Panel operativo protegido**
- CRUD de cursos en el frontend con baja lógica y pantalla de confirmación.
- Django Admin personalizado.
- Acceso solo para personal (`@login_required` y `@user_passes_test`).

**Usuarios**
- Registro, login y logout, con perfil (RUT validado, teléfono y rol institucional).

## Tecnologías

Python · Django · SQLite · Pillow · python-dotenv · Bootstrap 5

## Instalación paso a paso

1. Clonar el repositorio y entrar a la carpeta:

   ```
   git clone [URL-DEL-REPOSITORIO]
   cd [NOMBRE-DE-LA-CARPETA]
   ```

2. Crear y activar el entorno virtual:

   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```

   En macOS o Linux: `source .venv/bin/activate`

3. Instalar las dependencias:

   ```
   pip install -r requirements.txt
   ```

4. Crear el archivo de variables de entorno a partir del ejemplo:

   ```
   copy .env.example .env
   ```

   En macOS o Linux: `cp .env.example .env`

5. Crear la base de datos:

   ```
   python manage.py migrate
   ```

6. Cargar los datos de prueba (4 categorías, 8 cursos y 2 usuarios):

   ```
   python manage.py poblar_datos
   ```

7. Iniciar el servidor y abrir http://127.0.0.1:8000/

   ```
   python manage.py runserver
   ```

## Credenciales de prueba

| Rol | Usuario | Contraseña | Acceso |
|---|---|---|---|
| Administrador | `admin` | `Admin12345` | Panel de gestión y Django Admin (`/admin/`) |
| Estudiante | `estudiante` | `Estudiante12345` | Catálogo y carrito |

## Notas

- Las imágenes de los cursos se suben desde `/gestion/` o desde `/admin/`. La carpeta `media/` no se incluye en el repositorio.
- El descuento se configura en `apps/carrito/carrito.py`.

## Estructura del proyecto

```
config/            Configuración del proyecto (settings, urls)
apps/cursos/       Catálogo, CRUD, admin y comando poblar_datos
apps/carrito/      Carrito en sesión y context processor
apps/usuarios/     Registro, login, perfil y validador de RUT
templates/         Plantillas (base.html y una carpeta por app)
```

## Bitácora de Prompts de IA

### Caso 1: Arquitectura del proyecto

**Prompt:** "Debo hacer un proyecto Django con lo que pide la evaluación. Elegí una
plataforma de cursos tecnológicos. ¿Me puedes ayudar paso a paso?" Después le indiqué
que quería las apps dentro de una carpeta `apps/` y no en la raíz.

**Respuesta técnica:** La IA propuso separar el proyecto en `config/` (configuración)
y `apps/` (cursos, carrito, usuarios), crear cada app con
`startapp <nombre> apps/<nombre>` y cambiar `name` en `apps.py` y en
`INSTALLED_APPS` por la ruta completa (`apps.cursos`).

**Adaptación aplicada:** La IA agregó `label = 'cursos'` en `apps.py` pensando que
evitaría que las tablas se llamaran `apps_cursos`. Revisé y vi que Django usa por
defecto la última parte de `name`, así que esa línea era redundante y la quité.
Agregué `verbose_name` para que el panel muestre "Cursos".

### Caso 2: Modelado con Django ORM

**Prompt:** "Necesito los modelos CategoriaCurso y Curso con ForeignKey con PROTECT,
validadores numéricos, estado con opciones cerradas, imagen y baja lógica."

**Respuesta técnica:** Se generaron los dos modelos con `on_delete=PROTECT`,
`MinValueValidator(0)` en precio y cupos, `TextChoices` para el estado,
`ImageField` y el campo `vigente` para la baja lógica, junto con `select_related`
en las consultas del catálogo.

**Adaptación aplicada:** Comprendí que `MinValueValidator` solo actúa al validar
formularios, no a nivel de base de datos. Por eso lo reforcé con `clean_precio()` y
`clean_cupos()` en el formulario. Usé `IntegerField` para el precio porque el CLP no
lleva decimales. Cambié el borrado físico por baja lógica con pantalla de
confirmación, para no perder datos.

### Caso 3: Carrito en sesión y seguridad

**Prompt:** "Quiero un carrito en request.session para agregar, quitar, ver subtotal,
descuento y total, con validación de cupos."

**Respuesta técnica:** La IA propuso guardar en la sesión solo `{codigo: cantidad}` y
recalcular precios desde la base de datos, validar cupos y estado al agregar, usar
formularios POST con `{% csrf_token %}` y el decorador `@require_POST`, y un
context processor para el contador del menú.

**Adaptación aplicada:** Comparé con un proyecto de referencia que agregaba y quitaba
productos con enlaces GET. Descarté esa idea porque un GET no debe modificar el
estado y queda fuera de la protección CSRF. Definí la regla de negocio del descuento
(10% desde 3 cursos distintos) y la dejé en constantes para poder cambiarla en un solo lugar.
Protegí la confirmación con `@login_required`.
# 🏨 Hotel Pacific Reef

Sistema de Reserva Hotelera — PRY3211 Ingeniería de Software | Duoc UC
**Sprint: Semanas 7-8 | Framework: Django 5.x + PostgreSQL + Bootstrap 5**

## Requisitos

- Python 3.12+
- PostgreSQL 15+

## Instalación

```bash
# 1. Clonar repositorio
git clone <url-repo>
cd hotel_pacific_reef

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de PostgreSQL

# 5. Crear base de datos en PostgreSQL
# createdb hotel_pacific_reef

# 6. Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# 7. Crear superusuario
python manage.py createsuperuser

# 8. Cargar datos de prueba
python manage.py loaddata apps/habitaciones/fixtures/habitaciones_fixture.json

# 9. Iniciar servidor
python manage.py runserver
```

## URLs del sistema

| URL | Descripción |
|-----|-------------|
| `http://localhost:8000/` | Página de inicio |
| `http://localhost:8000/habitaciones/` | Catálogo de habitaciones |
| `http://localhost:8000/accounts/login/` | Iniciar sesión |
| `http://localhost:8000/accounts/registro/` | Crear cuenta |
| `http://localhost:8000/reservas/` | Mis reservas |
| `http://localhost:8000/panel/` | Dashboard admin |
| `http://localhost:8000/admin/` | Admin Django |

## Épicas del Sprint

| Épica | Descripción |
|-------|-------------|
| Épica 1 | Gestión de Acceso y Perfiles (`apps/accounts`) |
| Épica 2 | Motor de Reservas y Catálogo (`apps/habitaciones`, `apps/reservas`) |
| Épica 3 | Pagos y Confirmaciones con QR (`apps/pagos`) |
| Épica 4 | Administración y Reportes (`apps/panel`) |

## Decisión Técnica

El equipo Scrum optó por **Django 5.x** en lugar de Node.js/Express + React.js, dado que Django provee autenticación, ORM y panel admin integrados, reduciendo el tiempo de desarrollo significativamente.

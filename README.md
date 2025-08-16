# 🚀 Sistema de Gestión de Ventas - Django

Una plantilla robusta de Django preparada para desarrollo, testing y producción con arquitectura escalable y buenas prácticas.

## ✨ Características

- ✅ **Configuración por entornos** (desarrollo, testing, producción)
- ✅ **Sistema de templates** con herencia y componentes reutilizables
- ✅ **Archivos estáticos organizados** (CSS, JS, imágenes)
- ✅ **Testing integrado** con pytest y pytest-django
- ✅ **Logging configurado** para diferentes niveles
- ✅ **Variables de entorno** seguras por ambiente
- ✅ **CI/CD con GitHub Actions**
- ✅ **Estructura modular** para escalabilidad

## 🚀 Instalación y Configuración

### 1. **Clonar el repositorio:**
```bash
git clone https://github.com/bialyLT/boilerplate-django.git
cd project-gestion-ventas-django
```

### 2. **Crear y activar entorno virtual:**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

### 3. **Instalar dependencias:**
```bash
# Para desarrollo (incluye herramientas de debug y testing)
pip install -r requirements/dev.txt

# Para producción (optimizado)
pip install -r requirements/prod.txt

# Solo para testing
pip install -r requirements/test.txt
```

### 4. **Configurar variables de entorno:**
```bash
# Windows
copy .env.development .env

# Linux/Mac
cp .env.development .env
```

### 5. **Configurar base de datos:**
```bash
python manage.py migrate
python manage.py createsuperuser  # Opcional: crear admin
```

### 6. **Ejecutar servidor de desarrollo:**
```bash
python manage.py runserver
```

🎉 **¡Listo!** Tu aplicación estará disponible en `http://127.0.0.1:8000`

## 📁 Estructura del Proyecto

```
project-gestion-ventas-django/
├── 📁 .github/                # GitHub Actions y templates
│   ├── workflows/            # CI/CD automatizado
│   └── pull_request_template.md
├── 📁 config/                 # Configuración principal
│   ├── settings.py           # Configuración Django
│   ├── urls.py               # URLs principales
│   ├── wsgi.py               # WSGI para producción
│   └── asgi.py               # ASGI para async
├── 📁 core/                   # Aplicación principal
│   ├── views.py              # Vistas del sistema
│   ├── urls.py               # URLs de core
│   ├── models.py             # Modelos de datos
│   └── apps.py               # Configuración de app
├── 📁 apps/                   # Aplicaciones adicionales
├── 📁 templates/              # Templates HTML
│   ├── base.html             # Template base
│   └── core/                 # Templates de core
│       └── home.html         # Página de inicio
├── 📁 static/                 # Archivos estáticos
│   └── css/                  # Hojas de estilo
│       └── base.css          # Estilos principales
├── 📁 media/                  # Archivos subidos por usuarios
├── 📁 logs/                   # Archivos de logging
├── 📁 tests/                  # Tests del proyecto
│   ├── __init__.py
│   └── test_basic.py         # Tests básicos
├── 📁 requirements/           # Dependencias por entorno
│   ├── base.txt              # Dependencias base
│   ├── dev.txt               # Herramientas desarrollo
│   ├── prod.txt              # Optimizado producción
│   └── test.txt              # Solo testing
├── 🔐 .env.development        # Variables desarrollo
├── 🔐 .env.production         # Variables producción
├── 🔐 .env.test              # Variables testing
├── ⚙️ pytest.ini             # Configuración pytest
├── 🚫 .gitignore             # Archivos ignorados
└── 🐍 manage.py              # Comando Django
```

## 🌍 Configuración de Entornos

| Entorno | Variable | Descripción |
|---------|----------|-------------|
| **Desarrollo** | `DJANGO_ENV=development` | Debug activado, SQLite |
| **Producción** | `DJANGO_ENV=production` | Optimizado, PostgreSQL |
| **Testing** | `DJANGO_ENV=test` | Base de datos temporal |

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Tests con cobertura
pytest --cov

# Tests específicos
pytest tests/test_basic.py

# Tests con output detallado
pytest -v
```

## 📊 Características de Producción

- 🔒 **Configuración de seguridad** habilitada
- 🗄️ **Soporte PostgreSQL** configurado
- 📝 **Logging robusto** por niveles
- 🔄 **CI/CD con GitHub Actions**
- 📦 **Colección automática** de archivos estáticos
- 🛡️ **Middleware de seguridad** activado

## 🤝 Contribución

1. Fork el proyecto
2. Crea tu rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📜 Comandos Útiles

```bash
# Crear nueva aplicación
python manage.py startapp nombre_app

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Colectar archivos estáticos
python manage.py collectstatic

# Verificar configuración
python manage.py check

# Shell interactivo
python manage.py shell
```

## 🔧 Tecnologías

- **Django 4.2+** - Framework web
- **Python 3.11+** - Lenguaje
- **pytest** - Testing
- **python-dotenv** - Variables de entorno
- **PostgreSQL** - Base de datos (prod)
- **SQLite** - Base de datos (dev)

---

> 💡 **Tip**: Revisa los archivos `.env.*` y ajusta las configuraciones según tus necesidades antes de desplegar en producción.

📧 **Soporte**: Abre un issue en GitHub para reportar bugs o solicitar features.

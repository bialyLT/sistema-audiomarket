# 🎵 Marketplace de Audios - Django

Una plataforma robusta para la compra y venta de audios desarrollada con Django, Tailwind CSS y DaisyUI. Preparada para desarrollo, testing y producción con arquitectura escalable y buenas prácticas.

## ✨ Características Principales

- 🎵 **Marketplace de audios** completo para compradores y vendedores
- 👥 **Sistema de usuarios** con roles (Compradores, Vendedores, Administradores)
- 🎨 **UI moderna** con Tailwind CSS + DaisyUI
- 🔐 **Autenticación personalizada** usando email como identificador
- 📱 **Diseño responsive** adaptado a móviles y desktop
- ⚙️ **Configuración por entornos** (desarrollo, testing, producción)
- 🧪 **Testing integrado** con pytest y pytest-django
- 📊 **Logging configurado** para diferentes niveles
- 🔒 **Variables de entorno** seguras por ambiente
- 🏗️ **Estructura modular** para escalabilidad

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
.\.venv\Scripts\activate

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
python manage.py createsuperuser  # Crear usuario administrador
```

### 6. **Instalar y compilar Tailwind CSS:**
```bash
npm install
npm run build-css
```

### 7. **Ejecutar servidor de desarrollo:**
```bash
python manage.py runserver
```

🎉 **¡Listo!** Tu marketplace estará disponible en `http://127.0.0.1:8000`

## 👥 Sistema de Usuarios

### Tipos de Usuario:
- 🛒 **Compradores**: Pueden buscar, comprar y descargar audios
- 🎵 **Vendedores/Creadores**: Pueden subir, vender y gestionar sus audios
- 👤 **Administradores**: Control total del sistema

### Características de Autenticación:
- ✅ Registro con email como identificador único
- ✅ Login usando email y contraseña
- ✅ Perfiles personalizables con avatar
- ✅ Dashboards específicos por tipo de usuario
- ✅ Redirección automática según rol
- ✅ Protección de rutas por rol

## 🎨 Frontend y UI

- **Tailwind CSS**: Framework CSS utilitario para diseño rápido
- **DaisyUI**: Componentes predefinidos elegantes
- **Diseño responsive**: Adaptado para móviles y desktop
- **Navbar dinámico**: Cambia según el tipo de usuario
- **Componentes reutilizables**: Templates modulares

### Comandos CSS:
```bash
# Compilar CSS en modo desarrollo
npm run build-css

# Modo watch (recompila automáticamente)
npm run watch-css
```

## 📁 Estructura del Proyecto

```
project-gestion-ventas-django/
├── 📁 config/                 # Configuración principal Django
│   ├── settings.py           # Configuración por entornos
│   ├── urls.py               # URLs principales
│   ├── wsgi.py               # WSGI para producción
│   └── asgi.py               # ASGI para async
├── 📁 core/                   # Aplicación principal
│   ├── views.py              # Vista home y básicas
│   ├── urls.py               # URLs de core
│   └── apps.py               # Configuración de app
├── 📁 apps/                   # Aplicaciones modulares
│   └── users/                # Sistema de usuarios
│       ├── models.py         # User y Profile models
│       ├── views.py          # Login, registro, dashboards
│       ├── forms.py          # Formularios personalizados
│       ├── urls.py           # URLs de autenticación
│       └── migrations/       # Migraciones de BD
├── 📁 templates/              # Templates HTML
│   ├── base.html             # Template base con Tailwind
│   ├── layouts/              # Layouts reutilizables
│   │   └── navbar.html       # Navbar dinámico
│   ├── core/                 # Templates de core
│   │   └── home.html         # Página de inicio
│   └── users/                # Templates de usuarios
│       ├── register.html     # Formulario de registro
│       ├── login.html        # Formulario de login
│       └── dashboard_*.html  # Dashboards por rol
├── 📁 static/                 # Archivos estáticos
│   ├── css/                  # CSS compilado por Tailwind
│   │   └── output.css        # CSS final optimizado
│   ├── js/                   # JavaScript personalizado
│   └── images/               # Imágenes del sitio
├── 📁 media/                  # Archivos subidos (avatars, audios)
├── 📁 requirements/           # Dependencias por entorno
│   ├── base.txt              # Django, Pillow, etc.
│   ├── dev.txt               # pytest, debug tools
│   └── prod.txt              # Optimizado para producción
├── � tailwind.config.js     # Configuración Tailwind
├── � package.json           # Dependencias Node.js
├── 🔐 .env.development        # Variables desarrollo
├── ⚙️ pytest.ini             # Configuración testing
└── 🐍 manage.py              # Comandos Django
```

## 🌍 Configuración de Entornos

| Entorno | Variable | Descripción | Base de Datos |
|---------|----------|-------------|---------------|
| **Desarrollo** | `DJANGO_ENV=development` | Debug activado, recarga automática | SQLite |
| **Producción** | `DJANGO_ENV=production` | Optimizado, cache, minificado | PostgreSQL |
| **Testing** | `DJANGO_ENV=test` | Base de datos temporal | SQLite (memoria) |

### Variables de Entorno Importantes:
```bash
# Obligatorias
SECRET_KEY=tu-clave-secreta-super-segura
DJANGO_ENV=development

# Base de datos (producción)
DATABASE_URL=postgres://user:password@host:port/dbname

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password

# Media y Static files (producción)
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
AWS_STORAGE_BUCKET_NAME=tu-bucket
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Tests con cobertura
pytest --cov

# Tests específicos
pytest apps/users/tests.py

# Tests con output detallado
pytest -v

# Tests y generar reporte HTML de cobertura
pytest --cov --cov-report=html
```

### Estructura de Tests:
- `apps/users/tests.py` - Tests del sistema de usuarios
- `core/tests.py` - Tests de vistas principales
- `tests/` - Tests de integración y end-to-end

## 📊 Características Avanzadas

- � **Autenticación segura** con email como identificador
- 👤 **Perfiles personalizables** con avatar y biografía
- 🎵 **Sistema de archivos** preparado para audios
- 📱 **UI responsive** con Tailwind CSS y DaisyUI
- 🛡️ **Middleware de seguridad** activado
- 📝 **Logging estructurado** por niveles
- 🔄 **Signals automáticos** para creación de perfiles
- 🎯 **Dashboards específicos** por tipo de usuario
- � **Protección de rutas** basada en roles

## 🎵 Funcionalidades del Marketplace

### Para Compradores:
- 🔍 Buscar y filtrar audios
- 🛒 Carrito de compras
- 💳 Proceso de pago integrado
- 📥 Descarga de audios comprados
- ❤️ Lista de favoritos
- 📊 Historial de compras

### Para Vendedores:
- 📤 Subir audios con metadata
- 🏷️ Categorización y etiquetado
- 💰 Gestión de precios
- � Estadísticas de ventas
- 💵 Dashboard de ganancias
- 🎨 Perfil público de artista

### Para Administradores:
- 👥 Gestión de usuarios
- 🎵 Moderación de contenido
- 📊 Analytics completos
- 💳 Gestión de transacciones
- 🛠️ Configuración del sistema

## 🤝 Contribución

1. Fork el proyecto
2. Crea tu rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📜 Comandos Útiles

### Django:
```bash
# Crear nueva aplicación
python manage.py startapp nombre_app

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Verificar configuración
python manage.py check

# Shell interactivo
python manage.py shell

# Servidor de desarrollo
python manage.py runserver
```

### Tailwind CSS:
```bash
# Instalar dependencias
npm install

# Compilar CSS para desarrollo
npm run build-css

# Compilar y vigilar cambios
npm run watch-css

# Compilar para producción (minificado)
npm run build-css-prod
```

### Git:
```bash
# Crear rama para nueva feature
git checkout -b feature/nueva-funcionalidad

# Commits siguiendo convenciones
git commit -m "feat: agregar sistema de pagos"
git commit -m "fix: corregir error en login"
git commit -m "docs: actualizar README"
```

## 🔧 Stack Tecnológico

### Backend:
- **Django 4.2+** - Framework web principal
- **Python 3.11+** - Lenguaje de programación
- **SQLite** - Base de datos (desarrollo)
- **PostgreSQL** - Base de datos (producción)
- **Pillow** - Procesamiento de imágenes

### Frontend:
- **Tailwind CSS 3.x** - Framework CSS utilitario
- **DaisyUI 4.x** - Componentes predefinidos
- **JavaScript Vanilla** - Interactividad básica
- **HTML5** - Markup semántico

### Desarrollo y Testing:
- **pytest-django** - Framework de testing
- **pytest-cov** - Cobertura de código
- **python-dotenv** - Variables de entorno
- **Node.js & npm** - Gestión de assets frontend

### Herramientas:
- **Git** - Control de versiones
- **VS Code** - Editor recomendado
- **GitHub** - Repositorio y CI/CD
- **Vercel/Heroku** - Despliegue (recomendado)

## 🚀 Roadmap de Desarrollo

### Fase 1: ✅ Completada
- [x] Sistema de usuarios y autenticación
- [x] UI base con Tailwind CSS + DaisyUI
- [x] Dashboards por tipo de usuario
- [x] Estructura modular del proyecto

### Fase 2: 🚧 En progreso
- [ ] Sistema de carga y gestión de audios
- [ ] Reproductor de audio integrado
- [ ] Categorización y búsqueda avanzada
- [ ] Sistema de etiquetas

### Fase 3: 📋 Planificada
- [ ] Carrito de compras y checkout
- [ ] Integración de pagos (Stripe/PayPal)
- [ ] Sistema de reviews y ratings
- [ ] Estadísticas y analytics

### Fase 4: 🔮 Futuras
- [ ] API REST con DRF
- [ ] App móvil con React Native
- [ ] Sistema de suscripciones
- [ ] Inteligencia artificial para recomendaciones

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Para contribuir:

1. **Fork** el proyecto
2. **Crea** tu rama feature (`git checkout -b feature/NuevaFuncionalidad`)
3. **Commit** tus cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/NuevaFuncionalidad`)
5. **Abre** un Pull Request

### Guías de Contribución:
- Sigue las convenciones de código de Django
- Escribe tests para nuevas funcionalidades
- Actualiza la documentación cuando sea necesario
- Usa commits semánticos (feat:, fix:, docs:, etc.)

## 📧 Soporte y Contacto

- 🐛 **Reportar bugs**: Abre un [issue](https://github.com/bialyLT/boilerplate-django/issues)
- 💡 **Solicitar features**: Usa la plantilla de feature request
- 📖 **Documentación**: Revisa la [wiki](https://github.com/bialyLT/boilerplate-django/wiki)
- 💬 **Discusiones**: Únete a [Discussions](https://github.com/bialyLT/boilerplate-django/discussions)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## � Agradecimientos

- [Django](https://djangoproject.com/) por el excelente framework
- [Tailwind CSS](https://tailwindcss.com/) por el sistema de diseño
- [DaisyUI](https://daisyui.com/) por los componentes hermosos
- La comunidad open source por las herramientas increíbles

---

### 📊 Estado del Proyecto

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Django](https://img.shields.io/badge/django-v4.2+-green.svg)
![Tailwind](https://img.shields.io/badge/tailwind-v3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-En%20Desarrollo-yellow.svg)

> 💡 **Tip**: Revisa los archivos `.env.*` y ajusta las configuraciones según tus necesidades antes de desplegar en producción.

**¡Construyamos juntos el mejor marketplace de audios!** 🎵✨

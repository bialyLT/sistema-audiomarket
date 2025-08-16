# 🎵 Sistema de Gestión de Ventas de Audios - Desarrollo Modular

## 📋 Contexto del Proyecto
Necesito transformar mi plantilla base de Django en un **sistema de marketplace de audios** donde se puedan comprar y vender contenido de audio digital.

## 🎯 Objetivo Principal
Crear una plataforma de e-commerce especializada en audios (música, podcasts, audiolibros, efectos de sonido, etc.) con arquitectura modular y escalable.

## 👥 Tipos de Usuarios Requeridos
1. **Compradores** - Usuarios que adquieren audios
2. **Vendedores/Creadores** - Usuarios que publican y venden sus audios
3. **Administradores** - Gestión completa de la plataforma

## 🚀 Fase 1: Sistema de Autenticación (PRIORIDAD)
**Implementar primero:**
- ✅ Sistema de registro de usuarios con roles
- ✅ Login/logout con validaciones
- ✅ Perfiles diferenciados por tipo de usuario
- ✅ Middleware de permisos básico

**Estructura modular requerida:**
```
apps/
├── users/              # Gestión de usuarios
│   ├── models.py       # User, Profile, UserType
│   ├── views.py        # Login, Register, Profile
│   ├── forms.py        # Formularios de auth
│   └── templates/users/ # Templates de autenticación
└── core/               # Funcionalidades base
```

## 📁 Arquitectura Modular Esperada
- **Separación clara** de funcionalidades en apps Django
- **Templates organizados** por módulo
- **URLs modulares** con namespaces
- **Modelos relacionales** bien definidos
- **Permisos granulares** por tipo de usuario

## 🎵 Futuras Fases (Referencia)
- **Fase 2:** Gestión de productos de audio (upload/API)
- **Fase 3:** Sistema de compras y pagos
- **Fase 4:** Reproductor de audio integrado
- **Fase 5:** Dashboard de analytics

## 🛠️ Tecnologías Base Actuales
- Django 4.2+
- Tailwind CSS + DaisyUI
- SQLite (desarrollo) / PostgreSQL (producción)
- Sistema de templates modular

## 📝 Requerimientos Específicos
1. **Código limpio y comentado**
2. **Formularios con validaciones robustas**
3. **Responsive design con DaisyUI**
4. **Manejo de errores apropiado**
5. **Migraciones incrementales**
6. **Tests básicos incluidos**

## ❓ Preguntas Técnicas a Resolver
- ¿Usar Django User extendido o modelo Profile separado?
- ¿Implementar roles con Groups o sistema custom?
- ¿Validaciones en frontend y backend?

---

**NOTA:** Empezar SOLO con el sistema de usuarios. Una vez funcionando correctamente, avanzaremos con las siguientes fases del marketplace de audios.

¿Puedes implementar la Fase 1 completa con la estructura modular solicitada?

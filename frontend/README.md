# Frontend Dulpromax

Aplicación web para Dulpromax construida con Vue.js 3 (CDN) y Bootstrap 5, lista para producción en Netlify.

## Características

- Sin dependencias locales (todo desde CDN)
- Diseño responsivo
- Integración con la API de backend
- Fácil de desplegar

## Estructura del Proyecto

```
frontend/
├── index.html          # Aplicación principal
├── css/
│   └── styles.css      # Estilos personalizados
└── netlify.toml        # Configuración de Netlify
```

## Configuración de la API

Por defecto, la aplicación está configurada para conectarse a:
```
https://dulpromax-backend.onrender.com
```

Puedes cambiar esta URL en el archivo `index.html`, buscando la constante `API_BASE_URL`.

## Despliegue en Netlify

Sigue estos pasos para desplegar en Netlify:

1. **Preparar el repositorio**
   - Asegúrate de que tu código esté en un repositorio de GitHub, GitLab o Bitbucket

2. **Crear una cuenta en Netlify**
   - Ve a [Netlify](https://www.netlify.com/) y crea una cuenta si no tienes una

3. **Conectar el repositorio**
   - Haz clic en "Sites" y luego en "Import an existing project"
   - Conecta tu proveedor de Git (GitHub, GitLab o Bitbucket)
   - Selecciona el repositorio de tu proyecto

4. **Configurar el despliegue**
   - Directorio de construcción: `frontend`
   - Comando de construcción: (deja este campo vacío)
   - Directorio de publicación: `frontend`

5. **Variables de entorno (opcional)**
   - Si necesitas configurar variables de entorno, ve a:
     - Site settings > Build & deploy > Environment
     - Agrega cualquier variable que necesites

6. **Desplegar**
   - Haz clic en "Deploy site"
   - Netlify construirá y desplegará tu sitio

## Configuración de Dominio Personalizado (Opcional)

1. Ve a "Domain settings" en el panel de Netlify
2. Haz clic en "Add custom domain"
3. Sigue las instrucciones para configurar tu dominio

## Soporte

Si tienes problemas con el despliegue, verifica:
- Que la URL de la API sea correcta
- Que no haya errores en la consola del navegador
- Los logs de despliegue en el panel de Netlify

## Licencia

Este proyecto está bajo la licencia MIT.

# 🏥 Sistema Médico Completo 🩺

✨ *Descripción*  

¡Bienvenido al sistema médico completo! Este proyecto ha sido desarrollado en Django para gestionar de forma eficiente la información de pacientes, doctores, tipos de sangre, especialidades y más, brindando un entorno seguro y funcional para la administración de datos médicos. 🚀
Con este sistema, he puesto en práctica mis conocimientos en desarrollo web con Python, gestionando bases de datos complejas y creando interfaces intuitivas para los usuarios. El sistema utiliza PostgreSQL como base de datos, asegurando un almacenamiento de datos escalable y confiable.

🚀 *Características Principales*

* *Gestión Integral:* Agrega y administra información de pacientes, doctores, tipos de sangre, y especialidades.
* *Interfaces Amigables::* Diseño claro y fácil de navegar, pensado para usuarios administrativos.
* *Seguridad:* Control de acceso y administración mediante el sistema de autenticación de Django.
* *Tecnologías Web:* Desarrollado con Django (backend) y HTML, CSS, JavaScript (frontend).

🛠️ *Tecnologías Utilizadas*

* *Backend:*
    * *Django:* El sólido framework web de Python que impulsa la aplicación.
    * *PostgreSQL:* Base de datos SQL avanzada para un manejo eficiente y seguro de los datos médicos.
* *Frontend:*
    * *HTML, CSS, JavaScript:* Lenguajes esenciales para crear la interfaz de usuario.
    * *Bootstrap:* Para un diseño responsive y profesional.
    * *Font Awesome:* Biblioteca de iconos para añadir elementos visuales atractivos.  

## ⚙️ Cómo Ejecutar la Aplicación  

1. *Clonar el repositorio:*
   ```bash
   git clone https://github.com/SnayderCJ/Proy_Medical_System.git 
   cd Proy_Medical_System
   ```
    
2. *Crear (o activar) un entorno virtual::*   
    ```bash
    py -m venv venv  # Windows
    venv\Scripts\activate 

    python3 -m venv venv #Linux/Mac
    source venv/bin/activate
    ```

3. *Instalar las dependencias:*
    ```bash
    pip install -r requirements.txt
    ```

4. *Configurar la base de datos:*
    Asegúrate de tener PostgreSQL instalado y crea una base de datos para el sistema. Configura las credenciales de la base de datos en el archivo settings.py:
    ```bash
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_de_base_de_datos',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
    }
    ```

5. *Aplicar las migraciones:*
    ```bash
    py manage.py makemigrations
    py manage.py migrate
    ```

6. *Crear un superusuario:*
    ```bash
    py manage.py createsuperuser
    ```

7. *Ejecutar el servidor de desarrollo:*
    ```bash
    py manage.py runserver
    ```

8. *Acceder a la aplicación en tu navegador:*
    
    *   Abre tu navegador web y visita: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) (para la interfaz principal)
    

9. *Iniciar sesión en el panel de administración:*
    
    *   Accede al panel de administración: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) (utiliza las credenciales del superusuario). que creaste en el paso 6.
    

## 🚀 Explora el sistema médico y gestiona de forma efectiva los datos médicos. Si tienes alguna duda o sugerencia, ¡no dudes en contactarme! 😊
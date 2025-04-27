<a id="readme-top"></a>

<p align="center">
  <img src="https://img.shields.io/github/stars/dffdez/rodeoserver" alt="Stars" />
  <img src="https://img.shields.io/github/forks/dffdez/rodeoserver" alt="Forks" />
  <img src="https://img.shields.io/github/watchers/dffdez/rodeoserver" alt="Watchers" />
  <img src="https://img.shields.io/github/contributors/dffdez/rodeoserver" alt="Contributors" />
  <img src="https://img.shields.io/github/last-commit/dffdez/rodeoserver" alt="Last Commit" />
</p>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/dffdez/rodeoserver">
    <img src="https://github.com/user-attachments/assets/354504cd-dc6d-48a3-90d0-d79ba0c4e87b" alt="Logo" width="350" height="350">
  </a>


  <h3 align="center">Rodeo Server</h3>

   <p align="center">
    Desarrollo de una aplicación móvil para la formación y seguimiento del mercado bursátil
    <br />
    <br />
    <a href="https://github.com/dffdez/rodeoserver"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/dffdez/rodeoserver">View Demo</a>
    &middot;
    <a href="https://github.com/dffdez/rodeoserver/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/dffdez/rodeoserver/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
    
</div>


<!-- TABLE OF CONTENTS -->

  <summary>Contenidos</summary>
  <br />
  <ol>
    <li>
      <a href="#sobre-el-proyecto">Sobre el proyecto</a>
      <ul>
        <li><a href="#tecnologías-utilizadas">Tecnologías utilizadas</a></li>
      </ul>
    </li>
    <li><a href="#estructura">Estructura</a></li>
    <li>
      <a href="#primeros-pasos">Primeros pasos</a>
      <ul>
        <li><a href="#prerrequisitos">Prerrequisitos</a></li>
        <li><a href="#instalación">Instalación</a></li>
      </ul>
    </li>
  </ol>
    <br />



<!-- ABOUT THE PROJECT -->
## Sobre el proyecto

Este proyecto consiste en el desarrollo de una aplicación móvil, que ofrece a los usuarios la posibilidad de hacer seguimiento del mercado de valores en tiempo real. Identifica mediante un algoritmo el momento óptimo de realizar inversiones
y permite suscribirse a valores específicos, recibiendo alertas personalizadas sobre el momento de inversión de dicho activo.

Además, la aplicación incorpora un apartado de formación, que permite la publicación de artículos, videos y documentos de temática financiera. Incluye también un apartado de consultas, donde los usuarios pueden
plantear preguntas a los administradores mediante un chat en línea.

En este repositorio se encuentra el _backend_ de la aplicación, que consta de tres servicios que se despliegan utilizando <b>Docker</b>:
   <li><a><b>Servidor Python Flask</b>: Este servicio actúa como punto central de comunicaciones, manejando los _endpoints_ con los que interactúa 
       la aplicación y gestionando las peticiones.</a></li>
   <li><a><b>Base de Datos PostgreSQL</b>: Base de datos relacional que almacena los datos de la aplicación, incluyendo información sobre
       los usuarios, suscripciones, contenidos de formación y configuraciones de notificación.</a></li>
   <li><a><b>Motor de Cálculo o "Engine"</b>: Este servicio recopila datos de los valores bursátiles de la API de <b>TwelveData</b> y calcula el momento de inversión. Además, 
       se encarga de enviar notificaciones al dispositivo del usuario utilizando <b>Expo Push Notifications</b>.</a></li>
   <br />

El _frontend_ de esta aplicación se encuentra en https://github.com/dffdez/rodeo


### Tecnologías utilizadas

Las principales tecnologías que se han utilizado en este proyecto son:

* [![Python][PythonBadge]][Python-url]
* [![Flask][FlaskBadge]][Flask-url]
* [![PostgreSQL][PostgresBadge]][Postgres-url]
* [![Docker][DockerBadge]][Docker-url]
* [![TwelveData][TwelveDataBadge]][TwelveData-url]
* [![Expo Push Notifications][ExpoPushBadge]][ExpoPush-url]

<!-- Badges -->
[PythonBadge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/

[FlaskBadge]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/

[PostgresBadge]: https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-url]: https://www.postgresql.org/

[DockerBadge]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/

[TwelveDataBadge]: https://img.shields.io/badge/Twelve%20Data-0099FF?style=for-the-badge&logo=data:image/svg+xml;base64,...&logoColor=white
[TwelveData-url]: https://twelvedata.com/

[ExpoPushBadge]: https://img.shields.io/badge/Expo%20Push%20Notifications-000020?style=for-the-badge&logo=expo&logoColor=white
[ExpoPush-url]: https://docs.expo.dev/push-notifications/overview/


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Estructura

 El directorio _code_ contiene el código del servidor. Está a su vez dividido en:

 <ol>
      <ul>
        <li><a>Server:</a></li>
          <ul>
            <li><a>server.py --> Código del servidor con endpoints para peticiones</a></li>
            <li><a>database_api.py --> Comunicación con la base de datos</a></li>
            <li><a>Certificados</a></li>
          </ul>
        <li><a>Engine:</a></li>
          <ul>
            <li><a>engine.py --> Recopila datos del mercado de valores y calcula el momento de inversión</a></li>
            <li><a>notificationManager --> Gestión de peticiones por valor y cliente</a></li>
            <li><a>pushNotification --> Función para el envío de notificaciones push</a></li>
            <li><a>database_api.py --> Comunicación con la base de datos</a></li>
          </ul>
        <li><a>Database:</a></li>
          <ul>
            <li><a>basedatos_esquema.sql --> Órdenes SQL para la creación de tablas e incialización de valores.</a></li>
          </ul>
      </ul>
    </li>
  </ol>
    <br />    

El directorio _make_ contiene los archivos Dockerfile, el archivo docker-compose.yml y los scripts para la compilación y despliegue.
 <ol>
      <ul>
        <li><a><i>make.sh</i> crea las imágenes de Docker y las guarda en el directorio <i>exports</i> con los archivos para la instalación, que a su vez es comprimido dentro del directorio <i>install</i>.</a></li>
        <li><a><i>install.sh</i> carga las imágenes de Docker y levanta los contenedores.</a></li>
      </ul>
    </li>
  </ol>




<!-- GETTING STARTED -->
## Primeros pasos

En esta sección se detallan los pasos a seguir para la instalación del _backend_ localmente.
### Prerrequisitos

Antes de comenzar es necesario:
<ul>
   <li><a>Disponer de un equipo de trabajo con sistema operativo Ubuntu (recomendado)</a></li>
   <li><a>Instalar Docker Engine</a></li>
   <li><a>Instalar Visual Studio Code (recomendado)</a></li>
</ul>
<br />


  Podrá encontrar más información sobre Ubuntu en https://ubuntu.com/download

  Para la instalación de Docker Engine puede seguir los pasos que se indican en https://docs.docker.com/engine/install/

  Se recomienda tener instalado Visual Studio Code, que se puede instalar siguiendo los pasos que se indican en https://code.visualstudio.com/



### Instalación

Los pasos a seguir para utilizar este proyecto son:

1. Clonar el repositorio
 ```sh
   git clone https://github.com/dffdez/rodeoserver.git
   ```
2. Ejecutar el script _make.sh_, ubicado dentro del directorio _make_:
```sh
   ./make.sh
   ```
3. Ejecutar el script _install.sh_, ubicado dentro del directorio _exports_:
```sh
   ./install.sh
   ```

 Si han seguido estos pasos el _backend_ estará desplegado localmente.
 

 Puede comprobar el estado de los contenedores ejecutado: 
 ```sh
   docker ps
   ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>

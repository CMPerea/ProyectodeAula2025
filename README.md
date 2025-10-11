# 🧫 Sistema de Protocolos EM&B  
**Proyecto de aula – Tecnológico de Antioquia (2025)**  
**Autores:** Carlos Perea · Rosa Ramírez · Sura Rueda  
**Asesor:** Jhon Anderson Hernández Arango  

---

## 📘 Descripción del Proyecto  
El **Sistema de Protocolos EM&B** es una plataforma digital desarrollada en **Django** para el **Grupo de Ecología Microbiana y Bioprospección (EM&B)** de la **Universidad de Antioquia**.  
Su objetivo es **centralizar, validar y asegurar** los flujos de información científica del laboratorio, mejorando la trazabilidad, colaboración y eficiencia en los procesos de bioprospección.

El sistema permite la gestión integral de:
- Protocolos de investigación.  
- Organismos asociados (actinobacterias, levaduras, hongos filamentosos).  
- Equipos de laboratorio.  
- Archivos adjuntos, comentarios y registros de auditoría.  

---

## 🎯 Objetivo General  
Implementar un sistema integral de gestión de protocolos, organismos, equipos, usuarios y archivos adjuntos que garantice:
- Seguridad de la información.  
- Validación de procedimientos.  
- Colaboración efectiva y trazabilidad mediante auditoría.  

---

## ⚙️ Módulos Principales  
### 👥 Gestión de Usuarios  
- Registro, edición, desactivación y roles (Administrador / Estudiante).  
- Inicio y cierre de sesión con contraseñas encriptadas.  
- Notificaciones por correo al crear o editar usuarios.  

### 📄 Gestión de Protocolos  
- CRUD completo con historial de versiones.  
- Búsqueda, filtrado, descarga (PDF/Word) y validación de procedimientos.  
- Asociación con organismos y equipos.  

### 🔬 Gestión de Organismos  
- Información taxonómica y de cultivo.  
- Imágenes y documentos adjuntos.  

### ⚙️ Gestión de Equipos  
- Catálogo de equipos con estado, mantenimiento y alertas programadas.  

### 📎 Archivos Adjuntos  
- Subida segura de documentos, imágenes y datasets.  
- Filtros por tipo, entidad y proyecto.  

### 💬 Comentarios y Notificaciones  
- Retroalimentación colaborativa con hilos y control de permisos.  

### 🧾 Módulo de Auditoría  
- Registro inmutable de acciones (creación, edición, eliminación, login).  
- Exportación en CSV/PDF para análisis externo.  

---

## 🧠 Tecnologías Utilizadas  
- **Python 3.12+**  
- **Django 5.x**  
- **MySQL 8.x**  
- **HTML + CSS (Django Templates)**  
- **Git y GitHub**  
- **Microsoft Azure** (opcional para despliegue en nube)  

---

## 💻 Requisitos Previos  

Asegúrate de tener instalado:
- [Python](https://www.python.org/downloads/)  
- [MySQL](https://dev.mysql.com/downloads/installer/)  
- [Git](https://git-scm.com/downloads)  
- [Virtualenv](https://pypi.org/project/virtualenv/)  

---

## 🚀 Guía de Instalación y Ejecución  

### Clonar el repositorio  
```bash
git clone https://github.com/tu_usuario/GestionEMB.git
cd GestionEMB

---

### Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\Activate.ps1

---

### Instalar Dependencias
```bash
pip install -r requirements.txt

---




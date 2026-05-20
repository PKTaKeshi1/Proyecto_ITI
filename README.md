El presente proyecto consiste en el desarrollo de un sistema web de facturación orientado a pequeñas 
y medianas empresas, que permite gestionar de manera eficiente las operaciones relacionadas con la 
venta de productos, emisión de facturas, control de stock y registro de cobranzas. Implementado utilizando 
Python con Flask, MySQL, HTML5, CSS y tecnologías complementarias como WeasyPrint para la generación de 
comprobantes en PDF, el sistema sigue una arquitectura basada en el patrón Modelo-Vista-Controlador (MVC). 
Se han implementado módulos para la gestión de usuarios, productos, vendedores, clientes, ventas, facturación 
y cobranzas. Este sistema busca automatizar tareas administrativas, mejorar la trazabilidad de las operaciones 
y ofrecer un entorno amigable y funcional al usuario final. 

La automatización de procesos administrativos es un factor clave para el crecimiento y competitividad de 
las empresas modernas. En ese contexto, el presente proyecto tiene como finalidad desarrollar un sistema 
de facturación web, accesible desde cualquier navegador, que facilite la gestión de ventas, clientes, 
productos, emisión de facturas y seguimiento de cobranzas. A través del uso de tecnologías modernas como 
Flask (framework web ligero para Python), MySQL como gestor de base de datos y herramientas como WeasyPrint 
para la generación de documentos en formato PDF, se ha construido una solución robusta y escalable. 
El sistema implementa funcionalidades completas de CRUD (crear, leer, actualizar y eliminar) en los módulos 
principales, así como control de acceso por sesión y validaciones internas para garantizar la integridad de 
los datos. Esta aplicación busca reducir errores humanos, agilizar el proceso de facturación y brindar reportes
precisos para la toma de decisiones empresariales. 

Pasos para utilizar el sistema:
1. Abrir el programa de XAMPP (en puerto 5506 de mysql)
    1.1 Presionar Start en el apartado de Actions para Apache y MySQL
    1.2 Si se quiere hacer cambios en la base de datos visitar la pagina: 
    http://localhost/phpmyadmin/index.php?route=/database/structure&db=db_factura
    o presionar el boton de Admin en el apartado de MySQL
2. Una vez inicializado XAMPP
    2.1 Acceder a app.py que esta situado a la izquierda de esta pantalla en VSCode
    2.2 Luego presionar en el boton de play que esta ubicado en la esquina superior derecha (Ejecutar archivo 
    de Python)
    2.3 Acceder a la pagina web http://127.0.0.1:5000 en donde se mostrara el sistema de faturacion
        lanzado de manera local, este link tambien podra visualizarce en la parte inferior en la terminal
         * Running on http://127.0.0.1:5000
    2.4 Finalmente podra visualizar la pagina de inicio de sesion asegurese de registrarse correctamente
        y colocar la clave secreta de admin: clave_secreta_admin
        como caracter especial utilizar @
        

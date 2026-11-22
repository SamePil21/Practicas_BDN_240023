================================================================================

PRACTICA 04: PROCESOS DE SIMULACION DE COMPRA

================================================================================



Asignatura: Base de Datos en la Nube

Carrera: Ingenieria en Tecnologias de la Informacion e Innovacion Digital

Base de Datos: db_test (MySQL)

Repositorio: Practicas_BDN_240023

Autor: SamePil21



--------------------------------------------------------------------------------

ENLACES DE DOCUMENTACION INTERACTIVA (GITHUB PAGES)

--------------------------------------------------------------------------------



- Portal Principal (Inicio):

  https://samepil21.github.io/Practicas_BDN_240023/Practica04/index.html



- Diccionario de Datos:

  https://samepil21.github.io/Practicas_BDN_240023/Practica04/diccionario_datos.html



- Modelo Entidad-Relacion (EER):

  https://samepil21.github.io/Practicas_BDN_240023/Practica04/modelo_eer.html



- Repositorio en GitHub (Rama Practica04):

  https://github.com/SamePil21/Practicas_BDN_240023/tree/Practica04



--------------------------------------------------------------------------------

RESUMEN DEL RESPALDO (db_test)

--------------------------------------------------------------------------------



El portal de documentacion fue generado a partir del respaldo SQL ubicado en

Bakups/sql21noche.sql, integrando las estructuras y evidencias de los 5 casos

de prueba:



- Columnas documentadas: 227

- Vistas: 31 (incluye vw_practica04_caso_1 a vw_practica04_caso_5)

- Funciones: 6

- Procedimientos almacenados: 3

- Eventos programados: 2

- Evidencia transaccional destacada: 5 carritos (tb_carts), 5 direcciones

  (tb_user_addresses), 5 tipos y metodos de pago (tbc_payment_methods_types y

  tbd_user_payment_methods), 4 envios (tb_shipments), 2 cancelaciones y

  reembolsos (tb_cancellations y tb_refunds) y 1 devolucion (tb_returns).



--------------------------------------------------------------------------------

CASOS DE PRUEBA IMPLEMENTADOS

--------------------------------------------------------------------------------



CASO DE PRUEBA 1: "Compra Exitosa, sin modificaciones"

Vista asociada: vw_practica04_caso_1



1. Un usuario nuevo se registra en la plataforma (rol: user_not_registered,

   usuario de conexion a la BD: AppWeb o AppMobile) con sus datos personales

   y de cuenta de usuario.

2. El usuario creado realiza la seleccion de 5 productos disponibles (de

   aproximadamente 10,000 productos disponibles) verificando su estatus.

3. El usuario crea 1 carrito de compra.

4. El usuario agrega 5 productos con diferentes cantidades al carrito.

5. El usuario realiza la orden de compra.

6. El usuario registra su domicilio para envio.

7. El usuario registra su metodo de pago con tarjeta de debito, mediante una

   cuenta simulada de 16 digitos (vinculado a su tabla dependiente).

8. El usuario registra un pago unico (al pagar, el usuario de conexion activa

   el rol de "buyer").

9. El sistema registra la transaccion bancaria y la autoriza.

10. El sistema procesa la orden marcandola como atendida.

11. El usuario recibe el producto en casa.





CASO DE PRUEBA 2: "Compra con detalles en el ultimo pago, reclamacion y reenvio"

Vista asociada: vw_practica04_caso_2



1. Un usuario ya registrado (de los 10k disponibles) crea 1 carrito de compra

   de 10 productos aleatorios con cantidades de 1 a 5 unidades.

2. El usuario realiza la orden de compra.

3. El usuario registra un domicilio para envio distinto a su hogar (por

   ejemplo, direccion de trabajo).

4. El usuario registra su metodo de pago con tarjeta de credito, mediante una

   cuenta simulada de 16 digitos (vinculado a su tabla dependiente).

5. El usuario registra 6 pagos mensuales (al pagar, el usuario de conexion

   activa el rol de "buyer").

6. El sistema registra las transacciones bancarias: autoriza las primeras 5 y

   rechaza la ultima por "limite excedido de credito".

7. El sistema procesa la orden marcandola como atendida.

8. El usuario recibe el pedido en el domicilio registrado.

9. El usuario reclama la devolucion de un producto que llego danado.

10. El sistema realiza el reenvio del producto en buenas condiciones.





CASO DE PRUEBA 3: "Compra exitosa con cancelacion parcial, ajuste y reembolso parcial"

Vista asociada: vw_practica04_caso_3



1. Un usuario ya registrado (de los 10k disponibles) crea 1 carrito de compra

   de 3 productos de la misma categoria con cantidades de 1 a 10 unidades.

2. El usuario realiza la orden de compra.

3. El usuario registra un domicilio para envio distinto a su hogar (por

   ejemplo, con la etiqueta "Casa Papas").

4. El usuario registra su metodo de pago con tarjeta digital (Spin), mediante

   una cuenta simulada de 16 digitos (vinculado a su tabla dependiente).

5. El usuario registra un solo pago en efectivo por el costo total de la compra.

6. El sistema procesa la orden marcandola como atendida.

7. El usuario cancela un producto del pedido.

8. El sistema realiza la actualizacion y ajuste de la orden de compra.

9. El sistema realiza el reembolso parcial correspondiente al monto de los

   productos cancelados.

10. El sistema realiza el envio del pedido restante.

11. El cliente recibe el pedido en el domicilio indicado.





CASO DE PRUEBA 4: "Compra exitosa del mismo proveedor con entrega en el punto de recoleccion"

Vista asociada: vw_practica04_caso_4



1. Un usuario ya registrado (de los 10k disponibles) crea 1 carrito de compra

   de 3 productos del mismo proveedor con cantidades de 1 a 3 unidades.

2. El usuario realiza la orden de compra.

3. El usuario registra su domicilio de hogar para envio.

4. El usuario registra su metodo de pago con transferencia SPEI, mediante una

   cuenta simulada de 16 digitos (vinculado a su tabla dependiente).

5. El usuario registra un solo pago en efectivo por el costo total de la compra.

6. El sistema procesa la orden marcandola como atendida.

7. El sistema realiza el envio.

8. El cliente recoge el pedido en el punto de recoleccion dado que no hubo

   quien recibiera el pedido en el domicilio.





CASO DE PRUEBA 5: "Compra fallida por falta de inventario"

Vista asociada: vw_practica04_caso_5



1. Un usuario ya registrado (de los 10k disponibles) crea 1 carrito de compra

   de 1 producto del mismo proveedor con cantidades de 1 a 5 unidades.

2. El usuario realiza la orden de compra.

3. El usuario registra su domicilio de hogar para envio.

4. El usuario registra su metodo de pago utilizando un cupon de regalo.

5. El sistema procesa la orden marcandola como no atendida por falta de

   inventario.

6. El sistema cancela la orden y reasigna el cupon utilizado.



--------------------------------------------------------------------------------

ESTRUCTURA DEL PROYECTO (Practica04)

--------------------------------------------------------------------------------



Practica04/

|-- Bakups/                  Respaldo SQL (sql21noche.sql) y graficos (KULA.gif)

|-- quiries/                 Consultas y vistas SQL de los casos de prueba

|-- scrips/                  Scripts de ejecucion y logica de simulacion

|-- seeds/                   Datos semilla para poblar la base de datos

|-- index.html               Portal principal de documentacion

|-- diccionario_datos.html   Diccionario de datos interactivo

|-- modelo_eer.html          Modelo Entidad-Relacion (EER) interactivo

|-- app.js                   Logica de renderizado y navegacion web

|-- datos_bd.js              Metadatos extraidos del respaldo SQL

|-- estilos.css              Hoja de estilos (tema KOF / Kula)

|-- parse_dump.py            Script para procesar el respaldo SQL

|-- verify_dictionary.cjs    Verificador de integridad del diccionario

|-- README.md                Documentacion de la practica

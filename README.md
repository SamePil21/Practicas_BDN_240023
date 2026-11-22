<div align="center">

# Práctica 04: Procesos de Simulación de Compra

**Base de Datos en la Nube** · Ingeniería en Tecnologías de la Información e Innovación Digital

![Motor](https://img.shields.io/badge/Motor-MySQL-0284C7?style=for-the-badge)
![Base de Datos](https://img.shields.io/badge/Base_de_Datos-db__test-7C3AED?style=for-the-badge)
![Casos de Prueba](https://img.shields.io/badge/Casos_de_Prueba-5_Escenarios-4F46E5?style=for-the-badge)
![Estado](https://img.shields.io/badge/Documentación-Activa-0EA5E9?style=for-the-badge)

<br>

[![Portal Principal](https://img.shields.io/badge/Abrir_Portal_Principal-0284C7?style=for-the-badge)](https://samepil21.github.io/Practicas_BDN_240023/Practica04/index.html)
[![Modelo EER](https://img.shields.io/badge/Ver_Modelo_EER-7C3AED?style=for-the-badge)](https://samepil21.github.io/Practicas_BDN_240023/Practica04/modelo_eer.html)
[![Diccionario de Datos](https://img.shields.io/badge/Ver_Diccionario_de_Datos-4F46E5?style=for-the-badge)](https://samepil21.github.io/Practicas_BDN_240023/Practica04/diccionario_datos.html)

</div>

---

## Documentación Interactiva (GitHub Pages)

| Recurso | Descripción | Enlace Directo |
| :--- | :--- | :--- |
| **Portal Principal (Inicio)** | Resumen general del respaldo, métricas y vistas de los 5 casos. | [Abrir `index.html`](https://samepil21.github.io/Practicas_BDN_240023/Practica04/index.html) |
| **Modelo Entidad-Relación (EER)** | Diagrama interactivo de tablas, llaves primarias y relaciones FK. | [Abrir `modelo_eer.html`](https://samepil21.github.io/Practicas_BDN_240023/Practica04/modelo_eer.html) |
| **Diccionario de Datos** | Detalle de columnas, tipos de datos, restricciones, llaves y vistas. | [Abrir `diccionario_datos.html`](https://samepil21.github.io/Practicas_BDN_240023/Practica04/diccionario_datos.html) |

---

## Resumen Técnico de la Base de Datos

| Propiedad | Detalle |
| :--- | :--- |
| **Base de Datos** | `db_test` (MySQL) |
| **Respaldo SQL** | `Practica04/Bakups/sql21noche.sql` |
| **Columnas Totales** | 227 columnas |
| **Objetos Programables** | 31 vistas (incluyendo `vw_practica04_caso_1` a `vw_practica04_caso_5`), 6 funciones, 3 procedimientos almacenados y 2 eventos |
| **Repositorio** | `SamePil21/Practicas_BDN_240023` (Rama `Practica04`) |

---

## Matriz de Casos de Prueba

| Caso | Escenario | Tipo de Usuario | Método de Pago | Resultado Final |
| :---: | :--- | :--- | :--- | :--- |
| **01** | Compra exitosa, sin modificaciones | Usuario nuevo | Tarjeta de débito (pago único) | Entregada en domicilio |
| **02** | Detalle en último pago, reclamación y reenvío | Usuario registrado | Tarjeta de crédito (6 meses) | 5 pagos autorizados, 1 rechazado; reenvío por daño |
| **03** | Cancelación parcial, ajuste y reembolso parcial | Usuario registrado | Tarjeta digital Spin (pago único) | Orden ajustada, reembolso parcial y entrega |
| **04** | Mismo proveedor y punto de recolección | Usuario registrado | Transferencia SPEI (pago único) | Recogida en punto de recolección |
| **05** | Compra fallida por falta de inventario | Usuario registrado | Cupón de regalo | Orden cancelada y cupón reasignado |

---

## Detalle de los Casos de Prueba

### Caso de Prueba 1: Compra exitosa, sin modificaciones
> Flujo completo de registro de cliente nuevo, selección de productos, pago único con tarjeta de débito y entrega exitosa.

1. Un usuario nuevo se registra en la plataforma (rol: `user_not_registered`, usuario de conexión a la BD: `AppWeb` o `AppMobile`) con sus datos personales y de cuenta de usuario.
2. El usuario creado realiza la selección de 5 productos disponibles (de aproximadamente 10,000 productos disponibles) verificando su estatus.
3. El usuario crea 1 carrito de compra.
4. El usuario agrega los 5 productos con diferentes cantidades al carrito.
5. El usuario realiza la orden de compra.
6. El usuario registra su domicilio para envío.
7. El usuario registra su método de pago con tarjeta de débito mediante una cuenta simulada de 16 dígitos (vinculado a su tabla dependiente).
8. El usuario registra un pago único (al pagar, el usuario de conexión activa el rol `buyer`).
9. El sistema registra la transacción bancaria y la autoriza.
10. El sistema procesa la orden marcándola como atendida.
11. El usuario recibe el producto en casa.

---

### Caso de Prueba 2: Compra con detalles en el último pago, reclamación y reenvío
> Simulación de compra a meses con rechazo en el último cargo por límite de crédito, seguida de reclamación por daño y reposición.

1. Un usuario ya registrado (de los 10,000 disponibles) crea 1 carrito de compra con 10 productos aleatorios en cantidades de 1 a 5 unidades.
2. El usuario realiza la orden de compra.
3. El usuario registra su domicilio para envío a un lugar distinto a su hogar (por ejemplo, dirección de trabajo).
4. El usuario registra su método de pago con tarjeta de crédito mediante una cuenta simulada de 16 dígitos (vinculado a su tabla dependiente).
5. El usuario registra 6 pagos mensuales (al pagar, el usuario de conexión activa el rol `buyer`).
6. El sistema registra las transacciones bancarias: autoriza 5 pagos y rechaza el último por *"límite excedido de crédito"*.
7. El sistema procesa la orden marcándola como atendida.
8. El usuario recibe el producto en el domicilio indicado.
9. El usuario reclama la devolución de un producto que llegó dañado.
10. El sistema realiza el reenvío del producto en buenas condiciones.

---

### Caso de Prueba 3: Compra exitosa con cancelación parcial, ajuste y reembolso parcial
> Pedido de productos de una misma categoría con ajuste posterior por cancelación de un artículo y devolución parcial del monto.

1. Un usuario ya registrado (de los 10,000 disponibles) crea 1 carrito de compra con 3 productos de la misma categoría en cantidades de 1 a 10 unidades.
2. El usuario realiza la orden de compra.
3. El usuario registra un domicilio de envío distinto a su hogar (por ejemplo, dirección con la etiqueta `"Casa Papás"`).
4. El usuario registra su método de pago con tarjeta digital (Spin) mediante una cuenta simulada de 16 dígitos (vinculado a su tabla dependiente).
5. El usuario registra un solo pago en efectivo por el costo total de la compra.
6. El sistema procesa la orden marcándola como atendida.
7. El usuario cancela un producto del pedido.
8. El sistema realiza la actualización de la orden de compra.
9. El sistema realiza el reembolso del monto correspondiente a los productos cancelados.
10. El sistema realiza el envío.
11. El cliente recibe el pedido en el domicilio indicado.

---

### Caso de Prueba 4: Compra exitosa del mismo proveedor con entrega en punto de recolección
> Orden concentrada en un solo proveedor con pago vía SPEI y entrega alternativa en punto de recolección por ausencia en el domicilio.

1. Un usuario ya registrado (de los 10,000 disponibles) crea 1 carrito de compra con 3 productos del mismo proveedor en cantidades de 1 a 3 unidades.
2. El usuario realiza la orden de compra.
3. El usuario registra su domicilio de hogar para el envío.
4. El usuario registra su método de pago mediante transferencia SPEI con una cuenta simulada de 16 dígitos (vinculado a su tabla dependiente).
5. El usuario registra un solo pago en efectivo por el costo total de la compra.
6. El sistema procesa la orden marcándola como atendida.
7. El sistema realiza el envío.
8. El cliente recoge el pedido en el punto de recolección, dado que no hubo quien recibiera el paquete en el domicilio.

---

### Caso de Prueba 5: Compra fallida por falta de inventario
> Validación de control de existencias que detiene el procesamiento de una orden y restituye el cupón de regalo al usuario.

1. Un usuario ya registrado (de los 10,000 disponibles) crea 1 carrito de compra con 1 producto del mismo proveedor en una cantidad de 1 a 5 unidades.
2. El usuario realiza la orden de compra.
3. El usuario registra su domicilio de hogar para el envío.
4. El usuario registra su método de pago utilizando un cupón de regalo.
5. El sistema procesa la orden marcándola como no atendida por falta de inventario.
6. El sistema cancela la orden y reasigna el cupón utilizado.

---

## Estructura del Proyecto

```text
Practica04/
├── Bakups/
│   ├── sql21noche.sql
│   └── KULA.gif
├── quiries/
├── scripts/
├── seeds/
├── index.html
├── modelo_eer.html
├── diccionario_datos.html
├── app.js
├── datos_bd.js
├── estilos.css
├── parse_dump.py
├── verify_dictionary.cjs
└── README.md
```

---

<div align="center">
  <sub>Desarrollado por <strong>SamePil21</strong> · Prácticas de Base de Datos en la Nube</sub>
</div>

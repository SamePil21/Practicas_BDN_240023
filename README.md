# Practicas_BDN_240023

## Prácticas de la Asignatura de Base de Datos en la Nube

### Ingeniería en Tecnologías de la Información e Innovación Digital
**Universidad Tecnológica de Xicotepec de Juárez (UTXJ)**  
**Alumno:** Carlos Samuel Vargas Diego  
**Matrícula:** 240023  
**Docente:** M.T.I. Marco A. Ramírez Hernández  
**Periodo:** Septiembre - Diciembre 2026  

---

## Tabla de Prácticas de la Materia

| No. | Nombre | Descripción | Porcentaje | Estado |
| :-: | :--- | :--- | :-: | :-: |
| 1. | Metodología de Evaluación de la Materia | Transcribir en libreta y comprender la metodología y formas de evaluación de la asignatura | 5 | ⚪ Concluido |
| 2. | Conexiones Remotas para Bases de Datos SQL | Crear y administrar usuarios y privilegios para conexiones desde Internet o redes locales | 4 | ⚪ Concluido |
| 3. | Manipulación de Datos, Relaciones, Procedimientos, Funciones y Eventos en Conexiones Remotas | Implementación y operación remota de una BD de E-Commerce (25 tablas, 72 triggers, 25 vistas, 7 roles, rutinas SQL, simulación masiva de 7,500 usuarios, +7,000 productos y documentación interactiva) | 10 | ⚪ Concluido |

---

## 🌐 Documentación Técnica Interactiva — Práctica 03 (GitHub Pages)

Accede en tiempo real a la visualización interactiva de la base de datos **`db_test`** generada a partir del respaldo final:

| Recurso Interactivo | Descripción | Enlace Directo |
| :--- | :--- | :---: |
| **🏠 Portal Principal (Data Atlas)** | Resumen ejecutivo, KPIs del esquema y navegación general de `db_test`. | [Abrir Portal Principal](https://samepil21.github.io/Practicas_BDN_240023/Practica03/index.html) |
| **🕸️ Modelo Entidad-Relación Extendido (MERE)** | Diagrama interactivo de las **25 tablas**, relaciones *Crow's Foot*, animaciones de flujo, filtros por los 6 módulos y conteo real de registros. | [Ver Modelo EER](https://samepil21.github.io/Practicas_BDN_240023/Practica03/modelo_eer.html) |
| **📖 Diccionario de Datos Técnico** | Documentación detallada de atributos, tipos de datos, llaves (`PK`, `FK`, `UK`), restricciones, vistas, funciones, procedimientos, eventos y triggers. | [Ver Diccionario de Datos](https://samepil21.github.io/Practicas_BDN_240023/Practica03/diccionario_datos.html) |

---

## 📌 Detalle de la Práctica 03: Base de Datos de E-Commerce (`db_test`)

### 1. Objetivo
Implementar, manipular y administrar una base de datos relacional de E-Commerce en un entorno de nube mediante conexiones remotas e instrucciones SQL, aplicando relaciones, restricciones de integridad, roles y privilegios, así como procedimientos almacenados, funciones, triggers, vistas y eventos para automatizar operaciones, ejecutar simulaciones de población masiva, verificar la consistencia y trazabilidad de la información, y documentar la estructura y evolución de la base de datos.

---

### 2. Arquitectura del Esquema Relacional (25 Tablas)
El esquema **`db_test`** está organizado en **6 módulos funcionales** con integridad referencial completa:

1. **Usuarios y Direcciones:** `tb_users`, `tb_people`, `tb_user_addresses`, `tbd_address_components`.
2. **Catálogo y Productos:** `tb_products`, `tbc_categories`, `tbd_products_categories`, `tbd_products_users_providers`, `tbd_users_wishlist_products`.
3. **Carrito y Pedidos:** `tb_carts`, `tbd_carts_items`, `tb_buyer_orders`, `tbd_order_items`, `tb_shipments`.
4. **Pagos y Transacciones:** `tbc_payment_methods_types`, `tbd_user_payment_methods`, `tb_payment_methods`, `tb_payments`, `tb_payment_transactions`.
5. **Cancelaciones, Devoluciones y Reembolsos:** `tb_cancellations`, `tbd_cancellation_items`, `tb_returns`, `tbd_return_items`, `tb_refunds`.
6. **Auditoría y Bitácora:** `tb_logs`.

---

### 3. Mecanismos de Auditoría y Trazabilidad (72 Triggers y 25 Vistas)
* **72 Triggers de Auditoría:** Distribuidos en las **24 tablas operativas** (excluyendo `tb_logs`), cubriendo los eventos `AFTER INSERT`, `AFTER UPDATE` y `AFTER DELETE` para registrar automáticamente en `tb_logs` la tabla afectada, operación (`Create`, `Update`, `Delete`), usuario remoto (`USER()`), fecha/hora, estado y detalle del cambio.
* **25 Vistas SQL:**
  * **24 Vistas de Trazabilidad (`vw_trazabilidad_*`):** Relacionan las operaciones de cada tabla operativa con la bitácora `tb_logs` y los usuarios conectados.
  * **1 Vista Jerárquica (`vw_total_products_by_category`):** Consulta recursiva (`WITH RECURSIVE`) que contabiliza el total de productos, activos e inactivos a través del árbol de categorías, subcategorías y productos sin categoría.

---

### 4. Administración de Roles y Privilegios Remotos (7 Roles)
Se implementó el esquema de control de acceso basado en roles (RBAC) sobre las 24 tablas operativas:

| Rol | Alcance y Responsabilidades en el Sistema |
| :--- | :--- |
| **`superadmin`** | Control total del esquema, ejecución de simulaciones masivas, mantenimiento y auditoría global. |
| **`admin`** | Administración operativa de catálogos, usuarios, pedidos, pagos, devoluciones y vistas de control. |
| **`support`** | Consulta de seguimiento de pedidos, envíos, devoluciones, cancelaciones y atención a incidencias. |
| **`seller`** | Registro y actualización de inventario en `tb_products`, categorización (`tbd_products_categories`), proveedores y gestión de órdenes. |
| **`buyer`** | Gestión de carrito de compras, lista de deseos, direcciones de envío, métodos de pago, órdenes y solicitudes de devolución/cancelación. |
| **`common_user`** | Consulta de catálogo de productos, categorías y gestión básica de perfil personal. |
| **`user_not_registered`** | Acceso exclusivo de lectura (`SELECT`) al catálogo público de productos y categorías activas. |

---

### 5. Rutinas SQL, Eventos y Simulación Masiva de Datos

#### Funciones Auxiliares y de Reglas de Negocio (6 Funciones)
* `fn_entero_aleatorio(p_min, p_max)`: Generación controlada de números enteros aleatorios.
* `fn_generar_fecha_nacimiento(p_edad_min, p_edad_max)`: Cálculo de fechas de nacimiento coherentes con el rango de edad solicitado.
* `fn_estatus_probabilistico(p_prob_activo)`: Asignación probabilística del estado `b'1'` (activo) o `b'0'` (inactivo).
* `fn_elemento_aleatorio(p_lista, p_total_elementos)`: Extracción aleatoria de elementos desde catálogos en cadena.
* `fn_calcular_edad(p_fecha_nac)`: Cálculo determinístico de edad en años cumplidos.
* `fn_verificar_stock(p_product_id, p_cantidad)`: Validación de disponibilidad y existencias de un producto.

#### Procedimientos Almacenados (2 Procedimientos)
* `sp_simular_usuarios_masivo(p_cantidad, p_genero, p_pais, p_edad_min, p_edad_max, p_prob_activo)`: Procedimiento general parametrizable con soporte de comodines (`'*'` / `NULL`) y transacciones para poblar simultáneamente `tb_users` y `tb_people`.
* `sp_registrar_producto_categoria(...)`: Registro transaccional de productos con validación de precio y asignación inmediata a `tbd_products_categories`.

#### Eventos Programados (2 Eventos)
* `evt_desactivar_productos_sin_stock`: Se ejecuta cada hora para cambiar automáticamente a `status = b'0'` los productos cuyo `current_stock` llega a `0`.
* `evt_depurar_logs_antiguos`: Se ejecuta diariamente para depurar registros en `tb_logs` con antigüedad mayor a 90 días.

#### Escenarios de Simulación Ejecutados (7,500 Usuarios + Productos)
* **Escenario 1 (Test 1):** `CALL sp_simular_usuarios_masivo(500, 'Hombre', 'US', NULL, NULL, 100);` → 500 usuarios masculinos de Estados Unidos.
* **Escenario 2 (Test 2):** `CALL sp_simular_usuarios_masivo(2000, '*', '*', 19, 35, 100);` → 2,000 usuarios de diversos países entre 19 y 35 años.
* **Escenario 3 (Test 3):** `CALL sp_simular_usuarios_masivo(5000, '*', '*', NULL, NULL, 80);` → 5,000 usuarios con distribución probabilística del 80% activos (`b'1'`) y 20% inactivos (`b'0'`).
* **Población de Productos:** Más de 7,000 productos distribuidos entre vendedores remotos (`seller1` y `seller2`), asignados a categorías y subcategorías garantizando el mínimo de 5 productos por categoría e incluyendo productos activos e inactivos (`status = b'0'`).

---

### 6. Estructura del Repositorio (`Practica03`)

```text
Practica03/
├── Bakups/                  # Respaldos progresivos y dump final (.sql) de db_test
├── quiries/                 # Consultas SQL de verificación, validación, conteos y trazabilidad
├── scrips/                  # Scripts DDL de las 25 tablas, 72 triggers, 25 vistas, roles, funciones, SPs y eventos
├── seeds/                   # Scripts de población masiva de los 7,500 usuarios y +7,000 productos
├── index.html               # Portal principal interactivo Data Atlas
├── modelo_eer.html          # Visualizador interactivo del Modelo Entidad-Relación Extendido (MERE)
├── diccionario_datos.html   # Diccionario de Datos técnico interactivo
├── datos_bd.js              # Metadatos estructurados extraídos del respaldo SQL
├── app.js                   # Lógica de interacción, filtros, canvas EER y renderizado
└── estilos.css              # Hoja de estilos con diseño Glassmorphism

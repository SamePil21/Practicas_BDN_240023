/* 1. Limpieza previa de usuarios y roles */
DROP USER IF EXISTS 'marco.ramirez'@'%';
DROP USER IF EXISTS 'aaron.carballo'@'%';
DROP USER IF EXISTS 'mario.Banda'@'%';
DROP USER IF EXISTS 'Samuel.Vargas'@'%';
DROP USER IF EXISTS 'Dara.Gomez'@'%';
DROP USER IF EXISTS 'Jorge.Eloy'@'%';
DROP USER IF EXISTS 'Rene.David'@'%'; 
DROP USER IF EXISTS 'Rene'@'192.168.1.118';

DROP ROLE IF EXISTS 'super_admin', 'admin', 'seller', 'buyer', 'guest', 'support', 'user_not_registered', 'common';

/* ============================================================
   2. CREACIÓN DE TUS USUARIOS
   ============================================================ */
CREATE USER IF NOT EXISTS 'marco.ramirez'@'%' IDENTIFIED BY '1234';
CREATE USER IF NOT EXISTS 'aaron.carballo'@'%' IDENTIFIED BY '240045';
CREATE USER IF NOT EXISTS 'mario.Banda'@'%' IDENTIFIED BY '240597';
CREATE USER IF NOT EXISTS 'Samuel.Vargas'@'%' IDENTIFIED BY '240023';
CREATE USER IF NOT EXISTS 'Dara.Gomez'@'%' IDENTIFIED BY '240765';
CREATE USER IF NOT EXISTS 'Jorge.Eloy'@'%' IDENTIFIED BY '240456';
CREATE USER IF NOT EXISTS 'Rene.David'@'%' IDENTIFIED BY '240080';
CREATE USER IF NOT EXISTS 'Rene'@'192.168.1.118' IDENTIFIED BY '240080'; 

/* Asignar privilegios globales de super usuario a Samuel */
GRANT ALL PRIVILEGES ON *.* TO 'Samuel.Vargas'@'%';

/* ============================================================
   3. CREACIÓN DE ROLES
   ============================================================ */
CREATE ROLE IF NOT EXISTS 'super_admin';
CREATE ROLE IF NOT EXISTS 'admin';
CREATE ROLE IF NOT EXISTS 'seller';
CREATE ROLE IF NOT EXISTS 'buyer';
CREATE ROLE IF NOT EXISTS 'guest';
CREATE ROLE IF NOT EXISTS 'support';
CREATE ROLE IF NOT EXISTS 'user_not_registered';
CREATE ROLE IF NOT EXISTS 'common'; 

/* ============================================================
   4. ASIGNAR ROLES A LOS USUARIOS
   ============================================================ */
GRANT 'super_admin' TO 'Samuel.Vargas'@'%';
GRANT 'support' TO 'Jorge.Eloy'@'%';
GRANT 'seller' TO 'Dara.Gomez'@'%';
GRANT 'admin' TO 'marco.ramirez'@'%';
GRANT 'seller' TO 'aaron.carballo'@'%';
GRANT 'seller' TO 'Rene.David'@'%';
GRANT 'seller' TO 'Rene'@'192.168.1.118';
GRANT 'seller' TO 'mario.Banda'@'%'; 
-- SE ELIMINÓ: GRANT 'super_admin' TO 'root'@'localhost';

/* ============================================================
   5. ASIGNAR PRIVILEGIOS A LOS ROLES EN LA BASE DE DATOS db_test
   ============================================================ */

/* SUPER ADMIN & ADMIN */
GRANT ALL PRIVILEGES ON db_test.* TO 'super_admin';
GRANT ALL PRIVILEGES ON db_test.* TO 'admin';
GRANT CREATE ,SELECT, UPDATE, INSERT ON db_test_7b.tbd_products_categories TO 'support';

/* SELLER */
GRANT SELECT, INSERT, UPDATE, DELETE ON db_test.* TO 'seller';

/* BUYER */
GRANT SELECT, INSERT ON db_test.* TO 'buyer';

/* SUPPORT */
GRANT SELECT, INSERT, UPDATE ON db_test.* TO 'support';

/* COMMON & USER NOT REGISTERED */
GRANT SELECT ON db_test.* TO 'common';
GRANT SELECT ON db_test.* TO 'user_not_registered';

/* ============================================================
   6. DEFINIR ROL POR DEFECTO 
   ============================================================ */
SET DEFAULT ROLE 'super_admin' TO 'Samuel.Vargas'@'%';
SET DEFAULT ROLE 'support' TO 'Jorge.Eloy'@'%';
SET DEFAULT ROLE 'seller' TO 'Dara.Gomez'@'%';
SET DEFAULT ROLE 'admin' TO 'marco.ramirez'@'%';
SET DEFAULT ROLE 'seller' TO 'aaron.carballo'@'%';
SET DEFAULT ROLE 'seller' TO 'mario.Banda'@'%';
SET DEFAULT ROLE 'seller' TO 'Rene.David'@'%';
SET DEFAULT ROLE 'seller' TO 'Rene'@'192.168.1.118';

-- SE ELIMINÓ: SET DEFAULT ROLE 'super_admin' TO 'root'@'localhost';
/* ============================================================
   7. APLICAR LOS CAMBIOS
   ============================================================ */
FLUSH PRIVILEGES;

SELECT "Usuarios y roles creados correctamente" AS mensaje;
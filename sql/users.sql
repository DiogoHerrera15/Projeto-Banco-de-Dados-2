USE ecommerce_deferente;

DROP USER IF EXISTS 'admin_deferente'@'localhost';
DROP USER IF EXISTS 'gerente_deferente'@'localhost';
DROP USER IF EXISTS 'funcionario_deferente'@'localhost';

CREATE USER 'admin_deferente'@'localhost' IDENTIFIED BY 'Admin@123';
CREATE USER 'gerente_deferente'@'localhost' IDENTIFIED BY 'Gerente@123';
CREATE USER 'funcionario_deferente'@'localhost' IDENTIFIED BY 'Funcionario@123';

GRANT ALL PRIVILEGES
ON ecommerce_deferente.*
TO 'admin_deferente'@'localhost'
WITH GRANT OPTION;

GRANT SELECT, UPDATE, DELETE
ON ecommerce_deferente.*
TO 'gerente_deferente'@'localhost';

GRANT SELECT
ON ecommerce_deferente.vendas
TO 'funcionario_deferente'@'localhost';

GRANT SELECT
ON ecommerce_deferente.itens_venda
TO 'funcionario_deferente'@'localhost';

GRANT INSERT
ON ecommerce_deferente.vendas
TO 'funcionario_deferente'@'localhost';

GRANT INSERT
ON ecommerce_deferente.itens_venda
TO 'funcionario_deferente'@'localhost';

GRANT SELECT
ON ecommerce_deferente.clientes
TO 'funcionario_deferente'@'localhost';

GRANT SELECT
ON ecommerce_deferente.produtos
TO 'funcionario_deferente'@'localhost';

GRANT SELECT
ON ecommerce_deferente.transportadoras
TO 'funcionario_deferente'@'localhost';

GRANT EXECUTE
ON PROCEDURE ecommerce_deferente.sp_venda
TO 'funcionario_deferente'@'localhost';

FLUSH PRIVILEGES;
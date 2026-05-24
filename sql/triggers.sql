USE ecommerce_deferente;

DROP TRIGGER IF EXISTS trg_cliente_especial_cashback;

DELIMITER $$

CREATE TRIGGER trg_cliente_especial_cashback
AFTER INSERT ON vendas
FOR EACH ROW
BEGIN
    DECLARE valor_cashback DECIMAL(10,2);
    DECLARE total_cashback DECIMAL(10,2);

    IF NEW.valor_total > 500 THEN

        SET valor_cashback = NEW.valor_total * 0.02;

        INSERT INTO clientes_especiais (id_cliente, cashback)
        VALUES (NEW.id_cliente, valor_cashback)
        ON DUPLICATE KEY UPDATE cashback = cashback + valor_cashback;

        SELECT COALESCE(SUM(cashback), 0)
        INTO total_cashback
        FROM clientes_especiais;

        INSERT INTO avisos_sistema (mensagem)
        VALUES (
            CONCAT(
                'Valor total necessario para lidar com todo cashback: R$ ',
                FORMAT(total_cashback, 2)
            )
        );

    END IF;
END$$

DELIMITER ;

DROP TRIGGER IF EXISTS trg_remover_cliente_cashback_zerado;

DELIMITER $$

CREATE TRIGGER trg_remover_cliente_cashback_zerado
AFTER INSERT ON uso_cashback
FOR EACH ROW
BEGIN
    DECLARE saldo_atual DECIMAL(10,2);

    SELECT cashback
    INTO saldo_atual
    FROM clientes_especiais
    WHERE id_cliente = NEW.id_cliente;

    IF saldo_atual IS NOT NULL THEN

        UPDATE clientes_especiais
        SET cashback = GREATEST(cashback - NEW.valor_usado, 0)
        WHERE id_cliente = NEW.id_cliente;

        SELECT cashback
        INTO saldo_atual
        FROM clientes_especiais
        WHERE id_cliente = NEW.id_cliente;

        IF saldo_atual <= 0 THEN

            DELETE FROM clientes_especiais
            WHERE id_cliente = NEW.id_cliente;

            INSERT INTO avisos_sistema (mensagem)
            VALUES (
                CONCAT(
                    'Cliente ',
                    NEW.id_cliente,
                    ' removido dos clientes especiais por estar com cashback zerado.'
                )
            );

        END IF;

    END IF;
END$$

DELIMITER ;

DROP TRIGGER IF EXISTS trg_vendedor_especial_bonus;

DELIMITER $$

CREATE TRIGGER trg_vendedor_especial_bonus
AFTER INSERT ON itens_venda
FOR EACH ROW
BEGIN
    DECLARE vendedor_produto INT;
    DECLARE total_vendido DECIMAL(10,2);
    DECLARE valor_bonus DECIMAL(10,2);
    DECLARE total_bonus DECIMAL(10,2);

    SELECT id_vendedor
    INTO vendedor_produto
    FROM produtos
    WHERE id_produto = NEW.id_produto;

    SELECT COALESCE(SUM(iv.subtotal), 0)
    INTO total_vendido
    FROM itens_venda iv
    INNER JOIN produtos p ON iv.id_produto = p.id_produto
    WHERE p.id_vendedor = vendedor_produto;

    IF total_vendido > 1000 THEN

        SET valor_bonus = total_vendido * 0.05;

        INSERT INTO funcionarios_especiais (
            id_vendedor,
            valor_total_vendido,
            bonus
        )
        VALUES (
            vendedor_produto,
            total_vendido,
            valor_bonus
        )
        ON DUPLICATE KEY UPDATE
            valor_total_vendido = total_vendido,
            bonus = valor_bonus,
            data_registro = CURRENT_TIMESTAMP;

        SELECT COALESCE(SUM(bonus), 0)
        INTO total_bonus
        FROM funcionarios_especiais;

        INSERT INTO avisos_sistema (mensagem)
        VALUES (
            CONCAT(
                'Valor total necessario para custear bonus salarial: R$ ',
                FORMAT(total_bonus, 2)
            )
        );

    END IF;
END$$

DELIMITER ;
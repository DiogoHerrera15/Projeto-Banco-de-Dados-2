USE ecommerce_deferente;

DROP PROCEDURE IF EXISTS sp_reajuste;
DELIMITER $$
CREATE PROCEDURE sp_reajuste(
    IN percentual_reajuste DECIMAL(5,2),
    IN categoria_cargo VARCHAR(100)
)
BEGIN
    UPDATE vendedores v
    INNER JOIN cargos c
        ON v.id_cargo = c.id_cargo
    SET v.salario = v.salario + (v.salario * percentual_reajuste / 100)
    WHERE c.nome = categoria_cargo;

    SELECT
        v.id_vendedor,
        v.nome AS nome_vendedor,
        c.nome AS cargo,
        v.salario AS novo_salario
    FROM vendedores v
    INNER JOIN cargos c
        ON v.id_cargo = c.id_cargo
    WHERE c.nome = categoria_cargo;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_sorteio;
DELIMITER $$
CREATE PROCEDURE sp_sorteio()
BEGIN
    DECLARE cliente_sorteado INT;
    DECLARE nome_sorteado VARCHAR(100);
    DECLARE valor_voucher DECIMAL(10,2);

    SELECT id_cliente, nome
    INTO cliente_sorteado, nome_sorteado
    FROM clientes
    ORDER BY RAND()
    LIMIT 1;

    IF EXISTS (
        SELECT 1
        FROM clientes_especiais
        WHERE id_cliente = cliente_sorteado
    ) THEN
        SET valor_voucher = 200.00;
    ELSE
        SET valor_voucher = 100.00;
    END IF;

    INSERT INTO avisos_sistema (mensagem)
    VALUES (
        CONCAT(
            'Cliente sorteado: ',
            nome_sorteado,
            ' - Voucher recebido: R$ ',
            FORMAT(valor_voucher, 2)
        )
    );

    SELECT
        cliente_sorteado AS id_cliente,
        nome_sorteado AS nome_cliente,
        valor_voucher AS valor_voucher;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_venda;
DELIMITER $$
CREATE PROCEDURE sp_venda(
    IN p_id_cliente INT,
    IN p_id_transportadora INT,
    IN p_id_produto INT,
    IN p_endereco_destino TEXT,
    IN p_valor_transporte DECIMAL(10,2)
)
BEGIN
    DECLARE cliente_existe INT DEFAULT 0;
    DECLARE transportadora_existe INT DEFAULT 0;
    DECLARE produto_existe INT DEFAULT 0;
    DECLARE estoque_atual INT DEFAULT 0;
    DECLARE valor_produto DECIMAL(10,2);
    DECLARE nova_venda_id INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    SELECT COUNT(*) INTO cliente_existe
    FROM clientes
    WHERE id_cliente = p_id_cliente;
    IF cliente_existe = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cliente nao encontrado.';
    END IF;

    SELECT COUNT(*) INTO transportadora_existe
    FROM transportadoras
    WHERE id_transportadora = p_id_transportadora;
    IF transportadora_existe = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Transportadora nao encontrada.';
    END IF;

    SELECT COUNT(*) INTO produto_existe
    FROM produtos
    WHERE id_produto = p_id_produto;
    IF produto_existe = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Produto nao encontrado.';
    END IF;

    SELECT quantidade_estoque, valor
    INTO estoque_atual, valor_produto
    FROM produtos
    WHERE id_produto = p_id_produto;
    IF estoque_atual <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Produto sem estoque.';
    END IF;

    START TRANSACTION;

    INSERT INTO vendas (
        id_cliente,
        id_transportadora,
        endereco_destino,
        valor_transporte,
        valor_total
    )
    VALUES (
        p_id_cliente,
        p_id_transportadora,
        p_endereco_destino,
        p_valor_transporte,
        valor_produto + p_valor_transporte
    );

    SET nova_venda_id = LAST_INSERT_ID();

    INSERT INTO itens_venda (
        id_venda,
        id_produto,
        quantidade,
        valor_unitario,
        subtotal
    )
    VALUES (
        nova_venda_id,
        p_id_produto,
        1,
        valor_produto,
        valor_produto
    );

    UPDATE produtos
    SET quantidade_estoque = quantidade_estoque - 1
    WHERE id_produto = p_id_produto;

    COMMIT;

    SELECT
        nova_venda_id AS id_venda,
        p_id_cliente AS id_cliente,
        p_id_produto AS id_produto,
        valor_produto AS valor_produto,
        p_valor_transporte AS valor_transporte,
        'Venda realizada com sucesso' AS mensagem;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_estatisticas;
DELIMITER $$
CREATE PROCEDURE sp_estatisticas()
BEGIN
    DECLARE total_itens INT DEFAULT 0;
    DECLARE id_produto_mais INT;
    DECLARE nome_produto_mais VARCHAR(100);
    DECLARE vendedor_produto_mais VARCHAR(100);
    DECLARE qtd_produto_mais INT;
    DECLARE valor_produto_mais DECIMAL(10,2);
    DECLARE mes_maior_produto_mais VARCHAR(20);
    DECLARE mes_menor_produto_mais VARCHAR(20);
    DECLARE id_produto_menos INT;
    DECLARE nome_produto_menos VARCHAR(100);
    DECLARE vendedor_produto_menos VARCHAR(100);
    DECLARE qtd_produto_menos INT;
    DECLARE valor_produto_menos DECIMAL(10,2);
    DECLARE mes_maior_produto_menos VARCHAR(20);
    DECLARE mes_menor_produto_menos VARCHAR(20);

    SELECT COUNT(*)
    INTO total_itens
    FROM itens_venda;

    IF total_itens = 0 THEN
        SELECT 'Ainda nao existem vendas com produtos cadastrados.' AS mensagem;
    ELSE
        SELECT
            p.id_produto,
            p.nome,
            v.nome,
            SUM(iv.quantidade),
            SUM(iv.subtotal)
        INTO
            id_produto_mais,
            nome_produto_mais,
            vendedor_produto_mais,
            qtd_produto_mais,
            valor_produto_mais
        FROM produtos p
        INNER JOIN vendedores v
            ON p.id_vendedor = v.id_vendedor
        INNER JOIN itens_venda iv
            ON p.id_produto = iv.id_produto
        GROUP BY
            p.id_produto,
            p.nome,
            v.nome
        ORDER BY
            SUM(iv.quantidade) DESC,
            SUM(iv.subtotal) DESC
        LIMIT 1;

        SELECT
            p.id_produto,
            p.nome,
            v.nome,
            SUM(iv.quantidade),
            SUM(iv.subtotal)
        INTO
            id_produto_menos,
            nome_produto_menos,
            vendedor_produto_menos,
            qtd_produto_menos,
            valor_produto_menos
        FROM produtos p
        INNER JOIN vendedores v
            ON p.id_vendedor = v.id_vendedor
        INNER JOIN itens_venda iv
            ON p.id_produto = iv.id_produto
        GROUP BY
            p.id_produto,
            p.nome,
            v.nome
        ORDER BY
            SUM(iv.quantidade) ASC,
            SUM(iv.subtotal) ASC
        LIMIT 1;

        SELECT DATE_FORMAT(ve.data_venda, '%m/%Y')
        INTO mes_maior_produto_mais
        FROM vendas ve
        INNER JOIN itens_venda iv
            ON ve.id_venda = iv.id_venda
        WHERE iv.id_produto = id_produto_mais
        GROUP BY
            YEAR(ve.data_venda),
            MONTH(ve.data_venda)
        ORDER BY
            SUM(iv.quantidade) DESC,
            SUM(iv.subtotal) DESC
        LIMIT 1;

        SELECT DATE_FORMAT(ve.data_venda, '%m/%Y')
        INTO mes_menor_produto_mais
        FROM vendas ve
        INNER JOIN itens_venda iv
            ON ve.id_venda = iv.id_venda
        WHERE iv.id_produto = id_produto_mais
        GROUP BY
            YEAR(ve.data_venda),
            MONTH(ve.data_venda)
        ORDER BY
            SUM(iv.quantidade) ASC,
            SUM(iv.subtotal) ASC
        LIMIT 1;

        SELECT DATE_FORMAT(ve.data_venda, '%m/%Y')
        INTO mes_maior_produto_menos
        FROM vendas ve
        INNER JOIN itens_venda iv
            ON ve.id_venda = iv.id_venda
        WHERE iv.id_produto = id_produto_menos
        GROUP BY
            YEAR(ve.data_venda),
            MONTH(ve.data_venda)
        ORDER BY
            SUM(iv.quantidade) DESC,
            SUM(iv.subtotal) DESC
        LIMIT 1;

        SELECT DATE_FORMAT(ve.data_venda, '%m/%Y')
        INTO mes_menor_produto_menos
        FROM vendas ve
        INNER JOIN itens_venda iv
            ON ve.id_venda = iv.id_venda
        WHERE iv.id_produto = id_produto_menos
        GROUP BY
            YEAR(ve.data_venda),
            MONTH(ve.data_venda)
        ORDER BY
            SUM(iv.quantidade) ASC,
            SUM(iv.subtotal) ASC
        LIMIT 1;

        SELECT
            'Produto mais vendido' AS estatistica,
            id_produto_mais AS id_produto,
            nome_produto_mais AS produto,
            vendedor_produto_mais AS vendedor,
            qtd_produto_mais AS quantidade_vendida,
            valor_produto_mais AS valor_ganho,
            mes_maior_produto_mais AS mes_maior_venda,
            mes_menor_produto_mais AS mes_menor_venda
        UNION ALL
        SELECT
            'Produto menos vendido' AS estatistica,
            id_produto_menos AS id_produto,
            nome_produto_menos AS produto,
            vendedor_produto_menos AS vendedor,
            qtd_produto_menos AS quantidade_vendida,
            valor_produto_menos AS valor_ganho,
            mes_maior_produto_menos AS mes_maior_venda,
            mes_menor_produto_menos AS mes_menor_venda;
    END IF;
END$$
DELIMITER ;
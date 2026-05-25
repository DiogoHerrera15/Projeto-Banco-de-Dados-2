USE ecommerce_deferente;

DROP VIEW IF EXISTS vw_vendas_por_vendedor;
CREATE VIEW vw_vendas_por_vendedor AS
SELECT
    v.id_vendedor,
    v.nome AS nome_vendedor,
    v.causa_social,
    COUNT(DISTINCT ve.id_venda) AS quantidade_vendas,
    SUM(iv.quantidade) AS quantidade_produtos_vendidos,
    SUM(iv.subtotal) AS valor_total_vendido
FROM vendedores v
INNER JOIN produtos p
    ON v.id_vendedor = p.id_vendedor
INNER JOIN itens_venda iv
    ON p.id_produto = iv.id_produto
INNER JOIN vendas ve
    ON iv.id_venda = ve.id_venda
GROUP BY
    v.id_vendedor,
    v.nome,
    v.causa_social;


DROP VIEW IF EXISTS vw_compras_por_cliente;
CREATE VIEW vw_compras_por_cliente AS
SELECT
    c.id_cliente,
    c.nome AS nome_cliente,
    COUNT(DISTINCT v.id_venda) AS quantidade_compras,
    SUM(iv.quantidade) AS quantidade_produtos_comprados,
    SUM(iv.subtotal) AS valor_total_comprado
FROM clientes c
INNER JOIN vendas v
    ON c.id_cliente = v.id_cliente
INNER JOIN itens_venda iv
    ON v.id_venda = iv.id_venda
GROUP BY
    c.id_cliente,
    c.nome;



DROP VIEW IF EXISTS vw_vendas_por_transportadora;
CREATE VIEW vw_vendas_por_transportadora AS
SELECT
    t.id_transportadora,
    t.nome AS nome_transportadora,
    t.cidade,
    COUNT(DISTINCT v.id_venda) AS quantidade_vendas,
    (SELECT SUM(v2.valor_transporte) 
     FROM vendas v2 
     WHERE v2.id_transportadora = t.id_transportadora) AS valor_total_frete,
    SUM(iv.subtotal) AS valor_total_produtos
FROM transportadoras t
INNER JOIN vendas v
    ON t.id_transportadora = v.id_transportadora
INNER JOIN itens_venda iv
    ON v.id_venda = iv.id_venda
GROUP BY
    t.id_transportadora,
    t.nome,
    t.cidade;
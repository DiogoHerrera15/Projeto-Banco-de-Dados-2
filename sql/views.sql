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
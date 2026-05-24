-- E-commerce DEFERENTE
-- Arquivo responsável pela criação das tabelas principais

DROP TABLE IF EXISTS itens_venda CASCADE;
DROP TABLE IF EXISTS vendas CASCADE;
DROP TABLE IF EXISTS produtos CASCADE;
DROP TABLE IF EXISTS transportadoras CASCADE;
DROP TABLE IF EXISTS funcionarios_especiais CASCADE;
DROP TABLE IF EXISTS vendedores CASCADE;
DROP TABLE IF EXISTS clientes_especiais CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;
DROP TABLE IF EXISTS cargos CASCADE;

CREATE TABLE cargos (
    id_cargo SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);

CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INT NOT NULL CHECK (idade >= 0),
    sexo VARCHAR(20) NOT NULL,
    data_nascimento DATE NOT NULL
);

CREATE TABLE clientes_especiais (
    id_cliente INT PRIMARY KEY,
    cashback NUMERIC(10,2) NOT NULL DEFAULT 0.00,

    CONSTRAINT fk_cliente_especial
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON DELETE CASCADE
);

CREATE TABLE vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    causa_social VARCHAR(150) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    nota_media NUMERIC(3,2) DEFAULT 0.00 CHECK (nota_media >= 0 AND nota_media <= 5),
    salario NUMERIC(10,2) NOT NULL,
    id_cargo INT NOT NULL,

    CONSTRAINT fk_vendedor_cargo
        FOREIGN KEY (id_cargo)
        REFERENCES cargos(id_cargo)
);

CREATE TABLE funcionarios_especiais (
    id_vendedor INT PRIMARY KEY,
    valor_total_vendido NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    bonus NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_funcionario_especial
        FOREIGN KEY (id_vendedor)
        REFERENCES vendedores(id_vendedor)
        ON DELETE CASCADE
);

CREATE TABLE transportadoras (
    id_transportadora SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL
);

CREATE TABLE produtos (
    id_produto SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    quantidade_estoque INT NOT NULL CHECK (quantidade_estoque >= 0),
    valor NUMERIC(10,2) NOT NULL CHECK (valor >= 0),
    observacoes TEXT,
    id_vendedor INT NOT NULL,

    CONSTRAINT fk_produto_vendedor
        FOREIGN KEY (id_vendedor)
        REFERENCES vendedores(id_vendedor)
);

CREATE TABLE vendas (
    id_venda SERIAL PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_transportadora INT NOT NULL,
    data_venda DATE NOT NULL DEFAULT CURRENT_DATE,
    hora_venda TIME NOT NULL DEFAULT CURRENT_TIME,
    endereco_destino TEXT NOT NULL,
    valor_transporte NUMERIC(10,2) NOT NULL CHECK (valor_transporte >= 0),
    valor_total NUMERIC(10,2) NOT NULL DEFAULT 0.00,

    CONSTRAINT fk_venda_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),

    CONSTRAINT fk_venda_transportadora
        FOREIGN KEY (id_transportadora)
        REFERENCES transportadoras(id_transportadora)
);

CREATE TABLE itens_venda (
    id_item SERIAL PRIMARY KEY,
    id_venda INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    valor_unitario NUMERIC(10,2) NOT NULL CHECK (valor_unitario >= 0),
    subtotal NUMERIC(10,2) NOT NULL CHECK (subtotal >= 0),

    CONSTRAINT fk_item_venda
        FOREIGN KEY (id_venda)
        REFERENCES vendas(id_venda)
        ON DELETE CASCADE,

    CONSTRAINT fk_item_produto
        FOREIGN KEY (id_produto)
        REFERENCES produtos(id_produto)
);
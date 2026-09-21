# ⚡ Data Warehouse & Pipeline de Telemetria de Energia (Medallion Architecture)

## 🎯 Objetivo do Projeto
Este projeto simula o ambiente de dados de uma **Comercializadora de Energia** que atua no Ambiente de Contratação Livre (ACL) e em soluções de Geração Distribuída (GD). O pipeline automatiza a coleta de dados brutos de telemetria horária de medidores industriais (Smart Meters) e contratos comerciais, realizando processos de limpeza, tratamento de anomalias, conversão cambial e modelagem dimensional para fins de faturamento e business intelligence.

---

## 🏗️ Arquitetura de Dados e Infraestrutura
O projeto foi construído utilizando conceitos modernos de engenharia de dados e infraestrutura como código:

*   **Infraestrutura:** `Docker` e `Docker Compose` para orquestração de contêineres locais isolados.
*   **Armazenamento e SGBD:** `Postgres (v15)` estruturado seguindo a **Arquitetura de Medalhas (Medallion Architecture)**.
*   **Ingestão de Dados:** Script em `Python` utilizando drivers de conexão em lote (`psycopg2-binary`) para simular a carga massiva de fontes externas.
*   **Transformação de Dados:** Queries otimizadas em `SQL (ANSI)` para auditoria, limpeza e modelagem analítica.

---

## 📊 Estrutura das Camadas (Medallion Architecture)

### 1. 🥉 Camada Bronze (Raw Data)
*   **Tabelas:** `bronze.raw_telemetria_energia` e `bronze.raw_contratos_parcerias`.
*   **Conceito:** Armazenamento dos dados exatamente no formato de origem (texto/VARCHAR). Nesta camada foram injetadas propositalmente as anomalias comuns do setor elétrico: falhas de hardware do medidor (`'ERR'`), perdas de pacotes de rede celular (`'NULL'`) e desalinhamento de moedas contratuais (Reais e Dólares misturados).
*   **Volumetria:** +32.000 registros históricos abrangendo 90 dias de medições horárias para 15 indústrias parceiras.

### 2. 🥈 Camada Silver (Clean & Trusted)
*   **Tabelas:** `silver.telemetria_energia` e `silver.vendas_contratos`.
*   **Transformações Aplicadas:**
    *   **Data Quality:** Tratamento de strings nulas e erros textuais convertidos para `0.00` por regras de segurança.
    *   **Casting Dinâmico:** Conversão de strings de texto para tipos nativos de alta precisão (`NUMERIC` e `TIMESTAMP`).
    *   **Tratamento Cambial:** Uso de lógica condicional (`CASE WHEN`) para detectar contratos em USD e multiplicá-los dinamicamente pela taxa de câmbio, unificando a receita comercial em BRL.
    *   **Manipulação de Strings:** Aplicação de `TO_TIMESTAMP`, `TRIM` e `SPLIT_PART` para higienização de strings sujas.

### 3. 🥇 Camada Gold (Business & Dimensional)
*   **Tabelas:** `gold.dim_contratos_parcerias` (Dimensão de Contexto) e `gold.fato_consumo_faturamento` (Tabela Fato).
*   **Modelagem:** Implementação do modelo **Star Schema (Esquema Estrela)** focado em performance analítica.
*   **Regra de Negócio Implementada:** Cálculo automatizado hora a hora do Faturamento Bruto e Faturamento Líquido, convertendo as leituras físicas de consumo (`kWh`) para a unidade comercial de faturamento elétrico (`MWh`), aplicando descontos escalonados via `COALESCE`.

---

## 📈 Camada de Consumo (Analytics / View)
Para o consumo direto de ferramentas de Business Intelligence (como **Power BI**), foi disponibilizada a View analítica `gold.v_relatorio_faturamento_empresas`. Ela consolida o consumo mensal e o ranking de receita líquida de forma pré-computada, blindando e abstraindo a complexidade dos JOINS para a ponta de negócios.

---

## 🛠️ Como Executar o Projeto Localmente

1. Certifique-se de ter o `Docker` e o `Python` instalados.
2. Clone o repositório e navegue até a pasta:
   ```bash
   cd pipeline-telemetria-energia
   ```
3. Suba a infraestrutura do Data Warehouse em segundo plano:
   ```bash
   docker compose up -d
   ```
4. Execute o pipeline de ingestão em massa via Python:
   ```bash
   python gerador_dados.py
   ```
5. Conecte ao pgAdmin em `localhost:8080` para auditar os resultados.

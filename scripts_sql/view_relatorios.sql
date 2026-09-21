-- VIEW DE PRODUTO FINAL PARA O TIME DE BUSINESS INTELLIGENCE (BI)
CREATE OR REPLACE VIEW gold.v_relatorio_faturamento_empresas AS
SELECT 
    c.nome_empresa_parceira AS empresa,
    c.tipo_tarifa AS modalidade_tarifaria,
    TO_CHAR(f.data_hora_leitura, 'MM/YYYY') AS mes_ano,
    ROUND(SUM(f.consumo_kwh), 2) AS consumo_total_kwh,
    ROUND(SUM(f.faturamento_bruto_reais), 2) AS faturamento_bruto_total_rs,
    ROUND(SUM(f.faturamento_liquido_reais), 2) AS faturamento_liquido_total_rs
FROM gold.fato_consumo_faturamento f
INNER JOIN gold.dim_contratos_parcerias c ON f.id_medidor = c.id_medidor
GROUP BY c.nome_empresa_parceira, c.tipo_tarifa, TO_CHAR(f.data_hora_leitura, 'MM/YYYY');

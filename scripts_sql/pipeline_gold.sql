-- PIPELINE DE TRANSFORMAÇÃO GOLD - MERCADO DE ENERGIA
INSERT INTO gold.fato_consumo_faturamento (id_medidor, data_hora_leitura, consumo_kwh, faturamento_bruto_reais, faturamento_liquido_reais)
SELECT 
    t.id_medidor,
    t.data_hora_leitura,
    t.consumo_kwh,
    ROUND(((t.consumo_kwh / 1000.0) * c.preco_mwh_reais), 2),
    ROUND(((t.consumo_kwh / 1000.0) * c.preco_mwh_reais) * (1 - COALESCE(c.porcentagem_desconto, 0) / 100.0), 2)
FROM silver.telemetria_energia t
INNER JOIN gold.dim_contratos_parcerias c ON t.id_medidor = c.id_medidor;

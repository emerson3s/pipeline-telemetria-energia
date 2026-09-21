import psycopg2
from datetime import datetime, timedelta
import random

DB_CONFIG = {
    "host": "localhost",
    "database": "data_warehouse",
    "user": "engenheiro",
    "password": "SENHA_SEGURA_123",
    "port": "5432"
}

def conectar_banco():
    return psycopg2.connect(**DB_CONFIG)

def gerar_dados_energia_em_massa():
    conn = conectar_banco()
    cursor = conn.cursor()
    
    # Limpando registros antigos caso existam para não duplicar na Bronze
    cursor.execute("TRUNCATE TABLE bronze.raw_telemetria_energia;")
    cursor.execute("TRUNCATE TABLE bronze.raw_contratos_parcerias;")
    
    print("🚀 Iniciando carga massiva de dados na Camada Bronze...")

    # Simulando 15 grandes clientes industriais/comerciais (Parceiros de Energia)
    medidores = [f"MED-IND-{i:03d}" for i in range(1, 16)]
    
    # Período de 90 dias atrás até hoje
    data_fim = datetime.now()
    data_inicio = data_fim - timedelta(days=90)
    
    registros_telemetria = []
    data_atual = data_inicio
    
    print("⏳ Fabricando registros históricos de telemetria (90 dias de leituras horárias)...")
    
    # Loop que passa dia por dia, hora por hora, para cada medidor industrial
    while data_atual <= data_fim:
        for medidor in medidores:
            data_leitura_str = data_atual.strftime("%d/%m/%Y %H:%M")
            
            # Lógica probabilística de defeitos e comportamento de consumo por horário
            rand = random.random()
            if rand < 0.02:
                consumo = "ERR"  # Falha crítica no hardware do medidor
            elif rand < 0.03:
                consumo = "NULL" # Perda de pacote na rede celular (GPRS/LTE)
            else:
                # Consumo industrial simulado baseado no horário (indústrias gastam mais de dia)
                base_consumo = 500.0 if 8 <= data_atual.hour <= 18 else 150.0
                consumo = f"{random.uniform(base_consumo, base_consumo * 1.5):.2f}"
            
            # Simulando flutuações de tensão na rede elétrica
            rand_tensao = random.random()
            if rand_tensao < 0.01:
                tensao = "0V"
                status = "BLACKOUT"
            elif rand_tensao < 0.05:
                tensao = f"{random.choice(['180V', '190V'])} (SUBTENSÃO)"
                status = "WARNING"
            else:
                tensao = f"{random.choice(['218V', '220V', '222V'])}"
                status = "OPERATIONAL"
                
            registros_telemetria.append((medidor, data_leitura_str, consumo, tensao, status))
            
        data_atual += timedelta(hours=1)
        
        # Envio em lote (Batch) a cada 5000 registros para otimizar performance de memória do Python
        if len(registros_telemetria) >= 5000:
            cursor.executemany("""
                INSERT INTO bronze.raw_telemetria_energia (id_medidor, data_hora_leitura, consumo_kwh, tensao_fase, status_equipamento)
                VALUES (%s, %s, %s, %s, %s);
            """, registros_telemetria)
            registros_telemetria = []

    # Envia o restante dos registros acumulados
    if registros_telemetria:
        cursor.executemany("""
            INSERT INTO bronze.raw_telemetria_energia (id_medidor, data_hora_leitura, consumo_kwh, tensao_fase, status_equipamento)
            VALUES (%s, %s, %s, %s, %s);
        """, registros_telemetria)

    print("📝 Criando carteira comercial de Contratos de Parcerias...")
    # Simulando 15 contratos comerciais atrelados aos medidoresindustriais
    modalidades = ["Azul", "Verde", "Convencional", "GD_Solar_Assinatura"]
    
    for i, medidor in enumerate(medidores):
        id_contrato = f"CTR-2026-ENG-{i+1:03d}"
        empresa = f"Grupo Industrial Parceiro {i+1} Ltda"
        tarifa = random.choice(modalidades)
        
        # Injetando sujeira de moedas mistas, textos e símbolos
        if tarifa == "GD_Solar_Assinatura":
            preco_mwh = f"$ {random.uniform(42, 58):.2f} USD"
            desconto = f"{random.choice(['12%', '15%', '18.5%'])}"
        else:
            preco_mwh = f"R$ {random.uniform(240, 320):.2f}"
            desconto = f"{random.choice(['5%', '10%', 'NULL'])}"
            
        data_ini = (datetime.now() - timedelta(days=random.randint(60, 500))).strftime("%Y-%m-%d")
        
        cursor.execute("""
            INSERT INTO bronze.raw_contratos_parcerias (id_contrato, nome_empresa_parceira, tipo_tarifa, preco_mwh, data_inicio_vigencia, porcentagem_desconto)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (id_contrato, empresa, tarifa, preco_mwh, data_ini, desconto))
        
    conn.commit()
    
    # Buscando volumetria total salva para exibir no terminal
    cursor.execute("SELECT COUNT(*) FROM bronze.raw_telemetria_energia;")
    total_linhas = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    print(f"\n⚡ Carga concluída com sucesso!")
    print(f"📊 Total de registros inseridos na tabela de Telemetria: {total_linhas:,} linhas!")
    print(f"💼 Total de contratos comerciais de energia criados: 15 contratos.")

if __name__ == "__main__":
    gerar_dados_energia_em_massa()

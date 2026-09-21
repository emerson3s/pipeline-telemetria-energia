from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Emerson_Engenheiro',
    'start_date': datetime(2026, 9, 21),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='pipeline_faturamento_energia',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Comando simplificado que apenas avisa o sucesso na tela sem buscar caminhos complexos
    tarefa_teste_maestro = BashOperator(
        task_id='validacao_maestro_airflow',
        bash_command='echo "Maestro do Airflow ativo e monitorando o Data Warehouse de Energia!"'
    )

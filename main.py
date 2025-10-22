
# Importa o módulo 'os' para interagir com o sistema operacional, como manipulação de caminhos de arquivo.
import os
# Importa a função 'decodificacao' do módulo 'decoder'. Esta função é esperada para decodificar instruções.
from decoder import decodificacao
# Importa a função 'escrever' do módulo 'escrever'. Esta função será usada para salvar os resultados no pendrive.
from escrever import escrever
# Importa as funções de cálculo dos algoritmos de escalonamento do módulo 'calculos'.
from calculos import fifo, sjf, srt, round_robin

# Define a função principal que lê um arquivo de um pendrive.
def lendoArquivoPendrive(drive_path, filename, ns_value):

    # Constrói o caminho completo para o arquivo de entrada combinando o caminho do drive e o nome do arquivo.
    file_path = os.path.join(drive_path, filename)
    # Inicializa uma lista vazia para armazenar as instruções decodificadas lidas do arquivo.
    instrucoes_processos = []
    # Inicializa uma variável para armazenar o valor do quantum, que é a primeira linha do arquivo.
    quantum = 0

    try:
        # Verifica se o arquivo de entrada especificado não existe no caminho fornecido.
        if not os.path.exists(file_path):
            # Se o arquivo não for encontrado, retorna uma mensagem de aviso e pula para o próximo arquivo.
            return f"Aviso: Arquivo de entrada não encontrado: {file_path}. Pulando para o próximo.\n"
        
        # Abre o arquivo de entrada em modo de leitura.
        with open(file_path, 'r', encoding='utf-8') as f:
            # Lê a primeira linha do arquivo, que contém o valor do quantum para o Round Robin.
            quantum_str = f.readline().strip()
            # Converte o valor do quantum para inteiro.
            quantum = int(quantum_str)

            # Itera sobre as linhas restantes do arquivo, começando da segunda linha.
            for linhaNum, linha in enumerate(f, 2):
                # Remove espaços em branco do início e fim da linha.
                instrucao = linha.strip()
                # Verifica se a linha está vazia após remover os espaços em branco.
                if not instrucao:
                    # Se a linha estiver vazia, ignora e passa para a próxima iteração.
                    continue
                
                # Divide a instrução em partes usando espaço como delimitador.
                partes = instrucao.split(' ')
                # Converte as partes para inteiros, representando (chegada e tempo de execução).
                # Adiciona um ID de processo único para cada processo.
                instrucoes_processos.append((linhaNum - 1, int(partes[0]), int(partes[1])))

        # Dicionário para armazenar os resultados de cada algoritmo.
        resultados_algoritmos = {}

        # Executa o algoritmo FIFO e armazena os resultados.
        resultados_algoritmos['FIFO'] = fifo(instrucoes_processos)
        # Executa o algoritmo SJF e armazena os resultados.
        resultados_algoritmos['SJF'] = sjf(instrucoes_processos)
        # Executa o algoritmo SRT e armazena os resultados.
        resultados_algoritmos['SRT'] = srt(instrucoes_processos)
        # Executa o algoritmo Round Robin com o quantum lido e armazena os resultados.
        resultados_algoritmos['RR'] = round_robin(instrucoes_processos, quantum)

        # Após ler e processar as linhas, chama a função 'escrever' para salvar os resultados.
        escrever(resultados_algoritmos, ns_value, drive_path)

        return f"Processamento de {filename} concluído com sucesso."
    
    except FileNotFoundError:
        return f"Erro: O arquivo {filename} não foi encontrado. Verifique se o pendrive está conectado e o caminho está correto."
    except Exception as e:
        return f"Ocorreu um erro ao ler ou processar o arquivo {filename}: {e}"

if __name__ == "__main__":
    
    # Define o caminho base do pendrive. 
    Caminho_pendrive = ''

    # Itera de 1 a 10 para processar 10 arquivos de teste (TESTE-01.txt a TESTE-10.txt).
    for i in range(1, 11):
        # Formata o número 'i' com dois dígitos, preenchendo com zero à esquerda se necessário.
        ns = str(i).zfill(2)
        # Constrói o nome do arquivo de entrada usando o formato 'TESTE-XX.txt'.
        input_filename = f"TESTE-{ns}.txt"

        # Chama a função 'lendoArquivoPendrive' para processar cada arquivo.
        result_message = lendoArquivoPendrive(Caminho_pendrive, input_filename, ns)
        # Imprime a mensagem de resultado retornada pela função.
        print(result_message)
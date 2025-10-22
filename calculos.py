
import collections

def calcular_metricas(processos, tempos_resposta, tempos_espera, tempos_turnaround):

    num_processos = len(processos)
    if num_processos == 0:
        return 0.0, 0.0, 0.0

    total_resposta = sum(tempos_resposta.values())
    total_espera = sum(tempos_espera.values())
    total_turnaround = sum(tempos_turnaround.values())

    tempo_resposta_medio = total_resposta / num_processos
    tempo_espera_medio = total_espera / num_processos
    turnaround_medio = total_turnaround / num_processos

    return tempo_resposta_medio, tempo_espera_medio, turnaround_medio

def fifo(processos):

    processos_ordenados = sorted(processos, key=lambda x: x[1]) # Ordena por tempo de chegada

    tempo_atual = 0
    tempos_resposta = {}
    tempos_espera = {}
    tempos_turnaround = {}

    for pid, chegada, burst in processos_ordenados:
        # Tempo de início da execução
        inicio_execucao = max(tempo_atual, chegada)
        
        # Tempo de resposta
        tempos_resposta[pid] = inicio_execucao - chegada
        
        # Tempo de conclusão
        tempo_conclusao = inicio_execucao + burst
        
        # Tempo de espera
        tempos_espera[pid] = inicio_execucao - chegada
        
        # Tempo de turnaround
        tempos_turnaround[pid] = tempo_conclusao - chegada
        
        tempo_atual = tempo_conclusao

    return calcular_metricas(processos_ordenados, tempos_resposta, tempos_espera, tempos_turnaround)

def sjf(processos):

    processos_copia = sorted(processos, key=lambda x: x[1]) # Ordena por tempo de chegada
    
    tempo_atual = 0
    processos_prontos = []
    processos_completos = 0
    
    tempos_resposta = {}
    tempos_espera = {}
    tempos_turnaround = {}

    n = len(processos_copia)
    
    while processos_completos < n:
        # Adiciona processos que chegaram ao tempo atual na fila de prontos
        while processos_copia and processos_copia[0][1] <= tempo_atual:
            processos_prontos.append(processos_copia.pop(0))
        
        if not processos_prontos:
            if processos_copia:
                tempo_atual = processos_copia[0][1] # Avança o tempo para a chegada do próximo processo
                continue
            else:
                break # Não há mais processos

        # Ordena processos prontos por burst time (SJF)
        processos_prontos.sort(key=lambda x: x[2])
        
        pid, chegada, burst = processos_prontos.pop(0)
        
        # Tempo de início da execução
        inicio_execucao = tempo_atual
        
        # Tempo de resposta
        tempos_resposta[pid] = inicio_execucao - chegada
        
        # Tempo de conclusão
        tempo_conclusao = inicio_execucao + burst
        
        # Tempo de espera
        tempos_espera[pid] = inicio_execucao - chegada
        
        # Tempo de turnaround
        tempos_turnaround[pid] = tempo_conclusao - chegada
        
        tempo_atual = tempo_conclusao
        processos_completos += 1

    return calcular_metricas(processos, tempos_resposta, tempos_espera, tempos_turnaround)

def srt(processos):

    processos_copia = sorted(processos, key=lambda x: x[1])
    
    tempo_atual = 0
    processos_prontos = []
    processos_completos = 0
    
    tempos_resposta = {}
    tempos_espera = {}
    tempos_turnaround = {}
    tempos_inicio_execucao = {}
    burst_restante = {p[0]: p[2] for p in processos}

    n = len(processos_copia)
    
    while processos_completos < n:
        # Adiciona processos que chegaram ao tempo atual na fila de prontos
        while processos_copia and processos_copia[0][1] <= tempo_atual:
            processos_prontos.append(processos_copia.pop(0))
        
        if not processos_prontos:
            if processos_copia:
                tempo_atual = processos_copia[0][1]
                continue
            else:
                break

        # Seleciona o processo com o menor tempo restante
        processos_prontos.sort(key=lambda x: burst_restante[x[0]])
        
        processo_atual = processos_prontos[0] # Processo com menor tempo restante
        pid_atual, chegada_atual, burst_original_atual = processo_atual

        if pid_atual not in tempos_inicio_execucao:
            tempos_inicio_execucao[pid_atual] = tempo_atual
            tempos_resposta[pid_atual] = tempo_atual - chegada_atual

        burst_restante[pid_atual] -= 1
        tempo_atual += 1

        # Verifica se o processo terminou
        if burst_restante[pid_atual] == 0:
            processos_prontos.pop(0) # Remove da fila de prontos
            processos_completos += 1
            
            tempo_conclusao = tempo_atual
            tempos_turnaround[pid_atual] = tempo_conclusao - chegada_atual
            tempos_espera[pid_atual] = tempos_turnaround[pid_atual] - burst_original_atual

    return calcular_metricas(processos, tempos_resposta, tempos_espera, tempos_turnaround)

def round_robin(processos, quantum):
   
    processos_copia = sorted(processos, key=lambda x: x[1])
    
    tempo_atual = 0
    fila_prontos = collections.deque()
    processos_completos = 0
    
    tempos_resposta = {}
    tempos_espera = {}
    tempos_turnaround = {}
    tempos_inicio_execucao = {}
    burst_restante = {p[0]: p[2] for p in processos}

    n = len(processos_copia)
    
    # Adiciona todos os processos que chegam no tempo 0 à fila
    while processos_copia and processos_copia[0][1] == 0:
        pid, chegada, burst = processos_copia.pop(0)
        fila_prontos.append((pid, chegada, burst))

    while processos_completos < n:
        if not fila_prontos:
            # Se a fila estiver vazia, avança o tempo para a chegada do próximo processo
            if processos_copia:
                tempo_atual = processos_copia[0][1]
                # Adiciona processos que chegam no tempo atual à fila
                while processos_copia and processos_copia[0][1] <= tempo_atual:
                    pid, chegada, burst = processos_copia.pop(0)
                    fila_prontos.append((pid, chegada, burst))
            else:
                break # Não há mais processos

        processo_atual = fila_prontos.popleft()
        pid_atual, chegada_atual, burst_original_atual = processo_atual

        if pid_atual not in tempos_inicio_execucao:
            tempos_inicio_execucao[pid_atual] = tempo_atual
            tempos_resposta[pid_atual] = tempo_atual - chegada_atual

        tempo_execucao = min(quantum, burst_restante[pid_atual])
        burst_restante[pid_atual] -= tempo_execucao
        tempo_atual += tempo_execucao

        # Adiciona processos que chegaram durante a execução do quantum
        while processos_copia and processos_copia[0][1] <= tempo_atual:
            pid, chegada, burst = processos_copia.pop(0)
            fila_prontos.append((pid, chegada, burst))

        if burst_restante[pid_atual] > 0:
            fila_prontos.append(processo_atual) # Coloca o processo de volta na fila
        else:
            processos_completos += 1
            tempo_conclusao = tempo_atual
            tempos_turnaround[pid_atual] = tempo_conclusao - chegada_atual
            tempos_espera[pid_atual] = tempos_turnaround[pid_atual] - burst_original_atual

    return calcular_metricas(processos, tempos_resposta, tempos_espera, tempos_turnaround)
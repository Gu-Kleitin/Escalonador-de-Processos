#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def escrever(resultados_por_algoritmo, ns_value, drive_path):
    """
    Escreve os resultados dos cálculos em um arquivo de saída no pendrive.

    Args:
        resultados_por_algoritmo (dict): Um dicionário contendo os resultados para cada algoritmo.
                                       Ex: {'FIFO': [resposta_media, espera_media, turnaround_medio], ...}
        ns_value (str): O número formatado do arquivo de teste (ex: '01', '02').
        drive_path (str): O caminho base para a pasta de trabalho onde o arquivo será salvo.
    """
    output_filename = f"TESTE-{ns_value}-RESULTADO.txt"
    file_path = os.path.join(drive_path, output_filename)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for algoritmo, metricas in resultados_por_algoritmo.items():
                # Formata os valores com 3 casas decimais e usa vírgula como separador decimal
                linha_formatada = ", ".join([f"{m:.3f}".replace('.', ',') for m in metricas])
                f.write(f"{linha_formatada}\n")
        print(f"Arquivo de resultados '{output_filename}' criado com sucesso em {drive_path}")
    except Exception as e:
        print(f"Erro ao escrever o arquivo '{output_filename}': {e}")
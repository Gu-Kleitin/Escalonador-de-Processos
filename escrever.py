
import os

def escrever(resultados_por_algoritmo, ns_value, drive_path):
   
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
import os
import time
import multiprocessing
from multiprocessing import Pool


# ===============================
# Consolidação dos resultados
# ===============================

def consolidar_resultados(resultados):
    total_linhas = 0
    total_palavras = 0
    total_caracteres = 0

    contagem_global = {
        "erro": 0,
        "warning": 0,
        "info": 0
    }

    for r in resultados:
        total_linhas += r["linhas"]
        total_palavras += r["palavras"]
        total_caracteres += r["caracteres"]

        for chave in contagem_global:
            contagem_global[chave] += r["contagem"][chave]

    return {
        "linhas": total_linhas,
        "palavras": total_palavras,
        "caracteres": total_caracteres,
        "contagem": contagem_global
    }


# ===============================
# Processamento de arquivo
# ===============================

def processar_arquivo(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.readlines()

    total_linhas = len(conteudo)
    total_palavras = 0
    total_caracteres = 0

    contagem = {
        "erro": 0,
        "warning": 0,
        "info": 0
    }

    for linha in conteudo:
        palavras = linha.split()

        total_palavras += len(palavras)
        total_caracteres += len(linha)

        for p in palavras:
            if p in contagem:
                contagem[p] += 1

        # Simulação de processamento pesado
        for _ in range(1000):
            pass

    return {
        "linhas": total_linhas,
        "palavras": total_palavras,
        "caracteres": total_caracteres,
        "contagem": contagem
    }


# ===============================
# Execução serial (mantida intacta)
# ===============================

def executar_serial(pasta):
    resultados = []

    inicio = time.time()

    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)

        resultado = processar_arquivo(caminho)
        resultados.append(resultado)

    fim = time.time()

    resumo = consolidar_resultados(resultados)

    print("\n=== EXECUÇÃO SERIAL ===")
    print(f"Arquivos processados: {len(resultados)}")
    print(f"Tempo total: {fim - inicio:.4f} segundos")

    print("\n=== RESULTADO CONSOLIDADO ===")
    print(f"Total de linhas: {resumo['linhas']}")
    print(f"Total de palavras: {resumo['palavras']}")
    print(f"Total de caracteres: {resumo['caracteres']}")

    print("\nContagem de palavras-chave:")
    for k, v in resumo["contagem"].items():
        print(f"  {k}: {v}")

    return resumo


# ===============================
# Execução paralela
# ===============================

def executar_paralelo(pasta, num_processos):
    caminhos = [
        os.path.join(pasta, arquivo)
        for arquivo in os.listdir(pasta)
    ]

    inicio = time.time()

    with Pool(processes=num_processos) as pool:
        resultados = pool.map(processar_arquivo, caminhos)

    fim = time.time()

    resumo = consolidar_resultados(resultados)

    print(f"\n=== EXECUÇÃO PARALELA ({num_processos} processos) ===")
    print(f"Arquivos processados: {len(resultados)}")
    print(f"Tempo total: {fim - inicio:.4f} segundos")

    print("\n=== RESULTADO CONSOLIDADO ===")
    print(f"Total de linhas: {resumo['linhas']}")
    print(f"Total de palavras: {resumo['palavras']}")
    print(f"Total de caracteres: {resumo['caracteres']}")

    print("\nContagem de palavras-chave:")
    for k, v in resumo["contagem"].items():
        print(f"  {k}: {v}")

    return resumo, fim - inicio


# ===============================
# Main
# ===============================

if __name__ == "__main__":
    pasta = "log2"
    configs = [1, 2, 4, 8, 12]
    REPETICOES = 3
    tempos = {}

    for n in configs:
        medicoes = []
        for r in range(1, REPETICOES + 1):
            print(f"\n--- Rodada {r}/{REPETICOES} com {n} processo(s) ---")
            _, t = executar_paralelo(pasta, num_processos=n)
            medicoes.append(t)
        media = sum(medicoes) / len(medicoes)
        tempos[n] = media
        print(f">> Média com {n} processo(s): {media:.4f} segundos")

    print("\n\n=== RESUMO DE TEMPOS (média de 3 execuções) ===")
    print(f"{'Processos':<12} {'Tempo (s)':<14} {'Speedup':<10} {'Eficiência':<10}")
    t1 = tempos[1]
    for n, t in tempos.items():
        speedup = t1 / t
        eficiencia = speedup / n
        print(f"{n:<12} {t:<14.4f} {speedup:<10.4f} {eficiencia:<10.4f}")

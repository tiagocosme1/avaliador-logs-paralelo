import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

processos = [1, 2, 4, 8, 12]
tempos    = [84.7636, 45.7039, 26.7095, 18.8997, 15.6291]

t1 = tempos[0]
speedup    = [t1 / t for t in tempos]
eficiencia = [s / p for s, p in zip(speedup, processos)]
ideal      = [float(p) for p in processos]

os.makedirs("graficos", exist_ok=True)

# Gráfico 1 – Tempo de Execução
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(processos, tempos, "o-", color="#1f77b4", linewidth=2, markersize=7, label="Tempo medido")
ax.set_xlabel("Número de Processos")
ax.set_ylabel("Tempo de Execução (s)")
ax.set_title("Tempo de Execução × Número de Processos")
ax.set_xticks(processos)
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.grid(True, which="major", linestyle="--", alpha=0.6)
ax.legend()
plt.tight_layout()
plt.savefig("graficos/tempo_execucao.png", dpi=150)
plt.close()

# Gráfico 2 – Speedup
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(processos, ideal,   "--", color="gray",   linewidth=1.5, label="Speedup ideal (linear)")
ax.plot(processos, speedup, "s-", color="#d62728", linewidth=2, markersize=7, label="Speedup obtido")
ax.set_xlabel("Número de Processos")
ax.set_ylabel("Speedup")
ax.set_title("Speedup × Número de Processos")
ax.set_xticks(processos)
ax.grid(True, which="major", linestyle="--", alpha=0.6)
ax.legend()
plt.tight_layout()
plt.savefig("graficos/speedup.png", dpi=150)
plt.close()

# Gráfico 3 – Eficiência
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(processos, eficiencia, "^-", color="#2ca02c", linewidth=2, markersize=7, label="Eficiência")
ax.axhline(y=1.0, color="gray", linestyle="--", linewidth=1.2, label="Eficiência ideal (1.0)")
ax.set_xlabel("Número de Processos")
ax.set_ylabel("Eficiência")
ax.set_title("Eficiência × Número de Processos")
ax.set_xticks(processos)
ax.set_ylim(0, 1.1)
ax.grid(True, which="major", linestyle="--", alpha=0.6)
ax.legend()
plt.tight_layout()
plt.savefig("graficos/eficiencia.png", dpi=150)
plt.close()

print("Gráficos gerados com sucesso!")

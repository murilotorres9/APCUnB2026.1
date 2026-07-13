"""
sistema.py — PDAD Explorer: Perfil demográfico e composição domiciliar (Recorte F)

Sistema com interface gráfica (tkinter) para explorar o perfil demográfico
e a composição domiciliar do DF a partir dos microdados do PDAD 2024.

Execução:
    python sistema.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from utils.carregar import carregar_dados, montar_base_unificada, listar_localidades, ROTULOS_SEXO
from utils.calcular import (
    calcular_piramide_etaria,
    calcular_distribuicao_tamanho_domicilio,
    calcular_distribuicao_arranjos,
    calcular_perfil_complementar,
    calcular_estatisticas,
    ordenar_ras_por_tamanho_medio,
)
from utils.exportar import exportar_dados


class PDADExplorerApp:
    """Janela principal do sistema: carrega os dados, monta os widgets e
    conecta os filtros aos gráficos e estatísticas."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("PDAD Explorer — Perfil demográfico e composição domiciliar")
        self.root.geometry("1000x720")

        # --- 1. Carregar dados (Requisito 1: indicação de registros carregados) ---
        self.moradores, self.domicilios = carregar_dados()
        self.base = montar_base_unificada(self.moradores, self.domicilios)
        self.ras = ["Todos"] + listar_localidades(self.domicilios)
        self.ra_selecionada = tk.StringVar(value="Todos")
        self.estatisticas_atuais = {}

        self._montar_cabecalho()
        self._montar_abas()
        self.atualizar_tudo()

    # ------------------------------------------------------------------ UI

    def _montar_cabecalho(self) -> None:
        """Monta o cabeçalho: título, descrição, contagem de registros e filtro de RA."""
        topo = tk.Frame(self.root, padx=12, pady=10)
        topo.pack(fill="x")

        tk.Label(
            topo, text="PDAD Explorer — Perfil demográfico e composição domiciliar",
            font=("Helvetica", 15, "bold")
        ).pack(anchor="w")

        tk.Label(
            topo,
            text="Explore a pirâmide etária, a composição familiar dos domicílios e o perfil "
                 "de gênero/cor-raça do DF, por Região Administrativa (PDAD 2024).",
            wraplength=920, justify="left"
        ).pack(anchor="w", pady=(2, 8))

        self.label_contagem = tk.Label(
            topo,
            text=f"{len(self.moradores):,} moradores · {len(self.domicilios):,} domicílios "
                 f"carregados (Distrito Federal)".replace(",", "."),
            fg="#2563eb", font=("Helvetica", 10, "bold")
        )
        self.label_contagem.pack(anchor="w")

        # --- Requisito 2: filtro interativo (Combobox de RA) ---
        filtro_frame = tk.Frame(topo, pady=8)
        filtro_frame.pack(anchor="w")
        tk.Label(filtro_frame, text="Região Administrativa:").pack(side="left")
        combo = ttk.Combobox(
            filtro_frame, textvariable=self.ra_selecionada, values=self.ras,
            state="readonly", width=25
        )
        combo.pack(side="left", padx=6)
        combo.bind("<<ComboboxSelected>>", lambda e: self.atualizar_tudo())

        tk.Button(
            filtro_frame, text="Exportar dados filtrados", command=self.abrir_dialogo_exportar
        ).pack(side="left", padx=12)

    def _montar_abas(self) -> None:
        """Monta as abas (Requisito 1: pelo menos duas funcionalidades distintas)."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=8)

        # --- Aba 1: Pirâmide etária ---
        self.aba_piramide = tk.Frame(self.notebook)
        self.notebook.add(self.aba_piramide, text="Pirâmide etária")
        self._montar_estatisticas(self.aba_piramide)
        self.figura_piramide = Figure(figsize=(7.8, 4.0), dpi=100)
        self.eixo_piramide = self.figura_piramide.add_subplot(111)
        self.canvas_piramide = FigureCanvasTkAgg(self.figura_piramide, master=self.aba_piramide)
        self.canvas_piramide.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)

        # --- Aba 2: Composição domiciliar ---
        self.aba_domicilios = tk.Frame(self.notebook)
        self.notebook.add(self.aba_domicilios, text="Composição domiciliar")
        self.figura_domicilios = Figure(figsize=(7.8, 4.0), dpi=100)
        self.eixo_domicilios = self.figura_domicilios.add_subplot(111)
        self.canvas_domicilios = FigureCanvasTkAgg(self.figura_domicilios, master=self.aba_domicilios)
        self.canvas_domicilios.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)

        ranking_frame = tk.Frame(self.aba_domicilios, pady=6)
        ranking_frame.pack(fill="x")
        tk.Label(
            ranking_frame, text="Ranking de RAs por tamanho médio de domicílio "
                                 "(ordenado manualmente com Selection Sort):",
            font=("Helvetica", 9, "italic")
        ).pack(anchor="w")
        self.label_ranking = tk.Label(ranking_frame, justify="left", anchor="w")
        self.label_ranking.pack(anchor="w")

        # --- Aba 3: Arranjo familiar + perfil complementar (id_genero, cor/raça) ---
        self.aba_perfil = tk.Frame(self.notebook)
        self.notebook.add(self.aba_perfil, text="Arranjo familiar e perfil")
        self.figura_arranjos = Figure(figsize=(7.8, 3.4), dpi=100)
        self.eixo_arranjos = self.figura_arranjos.add_subplot(111)
        self.canvas_arranjos = FigureCanvasTkAgg(self.figura_arranjos, master=self.aba_perfil)
        self.canvas_arranjos.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)

        perfil_frame = tk.Frame(self.aba_perfil, pady=4)
        perfil_frame.pack(fill="x")
        self.label_perfil_genero = tk.Label(perfil_frame, justify="left", anchor="w")
        self.label_perfil_genero.pack(anchor="w")
        self.label_perfil_cor_raca = tk.Label(perfil_frame, justify="left", anchor="w")
        self.label_perfil_cor_raca.pack(anchor="w")

    def _montar_estatisticas(self, container: tk.Frame) -> None:
        """Monta os labels de estatísticas descritivas (Requisito 4: pelo menos 3)."""
        stats_frame = tk.Frame(container, pady=6)
        stats_frame.pack(fill="x")

        self.label_idade_media = tk.Label(stats_frame, font=("Helvetica", 10))
        self.label_idade_media.pack(anchor="w")
        self.label_tamanho_medio = tk.Label(stats_frame, font=("Helvetica", 10))
        self.label_tamanho_medio.pack(anchor="w")
        self.label_pct_criancas = tk.Label(stats_frame, font=("Helvetica", 10))
        self.label_pct_criancas.pack(anchor="w")

    # ------------------------------------------------------------- Ações

    def atualizar_tudo(self) -> None:
        """Recalcula estatísticas e redesenha os gráficos para a RA selecionada."""
        ra = self.ra_selecionada.get()

        self.estatisticas_atuais = calcular_estatisticas(self.base, self.domicilios, ra)
        self._atualizar_labels_estatisticas(self.estatisticas_atuais)
        self._atualizar_grafico_piramide(ra)
        self._atualizar_grafico_domicilios(ra)
        self._atualizar_ranking()
        self._atualizar_grafico_arranjos(ra)
        self._atualizar_perfil_complementar(ra)

    def _atualizar_labels_estatisticas(self, stats: dict) -> None:
        """Atualiza os labels de texto com as estatísticas descritivas (f-strings)."""
        self.label_idade_media.config(
            text=f"Idade média: {stats['idade_media']:.1f} anos  "
                 f"({stats['n_moradores']} moradores considerados)"
        )
        self.label_tamanho_medio.config(
            text=f"Tamanho médio do domicílio: {stats['tamanho_medio_domicilio']:.1f} pessoas  "
                 f"({stats['n_domicilios']} domicílios considerados)"
        )
        self.label_pct_criancas.config(
            text=f"Domicílios com pelo menos 1 criança (0-12 anos): {stats['pct_domicilios_com_criancas']:.1f}%"
        )

    def _atualizar_grafico_piramide(self, ra: str) -> None:
        """Redesenha a pirâmide etária por sexo (E03) — Requisito 3.

        Usamos E03 (Sexo) em vez de id_genero porque id_genero tem
        sentinela para crianças (ver utils/carregar.py); usar id_genero
        aqui quebraria a pirâmide justamente nas faixas mais jovens.
        """
        piramide = calcular_piramide_etaria(self.base, ra)
        self.eixo_piramide.clear()

        faixas = piramide.index.tolist()
        homens = -piramide.get(1, 0)  # negativo para desenhar à esquerda
        mulheres = piramide.get(2, 0)

        self.eixo_piramide.barh(faixas, homens, color="#2563eb", label=ROTULOS_SEXO[1])
        self.eixo_piramide.barh(faixas, mulheres, color="#db2777", label=ROTULOS_SEXO[2])
        self.eixo_piramide.set_title(f"Pirâmide etária por sexo — {ra}")
        self.eixo_piramide.set_xlabel("Número de moradores")
        self.eixo_piramide.set_ylabel("Faixa etária")
        self.eixo_piramide.legend()
        self.eixo_piramide.axvline(0, color="black", linewidth=0.5)
        self.figura_piramide.tight_layout()
        self.canvas_piramide.draw()

    def _atualizar_grafico_domicilios(self, ra: str) -> None:
        """Redesenha a distribuição de domicílios por tamanho (Diferencial
        D1: segundo tipo de gráfico, complementando a pirâmide etária)."""
        distribuicao = calcular_distribuicao_tamanho_domicilio(self.domicilios, ra)
        self.eixo_domicilios.clear()
        self.eixo_domicilios.bar(distribuicao.index.astype(str), distribuicao.values, color="#16a34a")
        self.eixo_domicilios.set_title(f"Domicílios por número de moradores — {ra}")
        self.eixo_domicilios.set_xlabel("Número de pessoas no domicílio")
        self.eixo_domicilios.set_ylabel("Número de domicílios")
        self.figura_domicilios.tight_layout()
        self.canvas_domicilios.draw()

    def _atualizar_ranking(self) -> None:
        """Atualiza o texto do ranking de RAs por tamanho médio de domicílio."""
        ranking = ordenar_ras_por_tamanho_medio(self.domicilios)
        linhas = [f"{i+1}. {ra} — {media:.2f} pessoas/domicílio" for i, (ra, media) in enumerate(ranking[:10])]
        self.label_ranking.config(text="\n".join(linhas))

    def _atualizar_grafico_arranjos(self, ra: str) -> None:
        """Redesenha a distribuição de domicílios por tipo de arranjo familiar."""
        distribuicao = calcular_distribuicao_arranjos(self.domicilios, ra)
        self.eixo_arranjos.clear()
        self.eixo_arranjos.barh(distribuicao.index, distribuicao.values, color="#f59e0b")
        self.eixo_arranjos.set_title(f"Domicílios por tipo de arranjo familiar — {ra}")
        self.eixo_arranjos.set_xlabel("Número de domicílios")
        self.figura_arranjos.tight_layout()
        self.canvas_arranjos.draw()

    def _atualizar_perfil_complementar(self, ra: str) -> None:
        """Atualiza os textos de perfil de gênero (id_genero) e cor/raça (E05)."""
        perfil = calcular_perfil_complementar(self.base, ra)

        linhas_genero = [f"  {categoria}: {pct:.1f}%" for categoria, pct in perfil["id_genero_pct"].items()]
        self.label_perfil_genero.config(
            text="Identidade de gênero (id_genero, entre quem respondeu):\n" + "\n".join(linhas_genero)
        )

        linhas_cor_raca = [f"  {categoria}: {pct:.1f}%" for categoria, pct in perfil["cor_raca_pct"].items()]
        self.label_perfil_cor_raca.config(
            text="Cor ou raça (E05):\n" + "\n".join(linhas_cor_raca)
        )

    def abrir_dialogo_exportar(self) -> None:
        """Abre o diálogo de exportação (Requisito 5) para salvar as estatísticas atuais."""
        caminho = filedialog.asksaveasfilename(
            title="Exportar dados filtrados",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("Texto", "*.txt")],
        )
        if not caminho:
            return
        exportar_dados(self.estatisticas_atuais, self.ra_selecionada.get(), caminho)
        messagebox.showinfo("Exportação concluída", f"Dados exportados para:\n{caminho}")


def main() -> None:
    """Ponto de entrada: cria a janela raiz e inicia o loop principal do tkinter."""
    root = tk.Tk()
    PDADExplorerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

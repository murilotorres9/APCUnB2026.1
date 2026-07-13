"""
sistema.py — PDAD Explorer: Perfil demográfico e composição domiciliar (Recorte F)

Sistema com interface gráfica (tkinter) para explorar o perfil demográfico
e a composição domiciliar do DF a partir dos microdados do PDAD 2024.

Execução:
    python sistema.py
"""

# --- Bibliotecas da interface gráfica ---
import tkinter as tk
# ttk = "themed tkinter" — widgets com aparência mais moderna (Combobox, Notebook/abas)
# filedialog = abre as janelas nativas do sistema operacional para "Salvar como..."
# messagebox = janelas de alerta/confirmação (ex: "Exportação concluída")
from tkinter import ttk, filedialog, messagebox

# --- Bibliotecas de gráficos ---
import matplotlib
# Define explicitamente que o matplotlib deve desenhar usando o motor gráfico
# do tkinter ("TkAgg"). Isso precisa vir ANTES de importar pyplot/Figure,
# senão o matplotlib pode tentar usar outro motor e falhar dentro do tkinter.
matplotlib.use("TkAgg")
# FigureCanvasTkAgg é a "ponte" que permite desenhar uma figura do matplotlib
# dentro de um widget do tkinter (sem ela, o gráfico abriria em outra janela).
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Figure é o "quadro em branco" do matplotlib onde os gráficos são desenhados.
from matplotlib.figure import Figure

# --- Funções próprias do projeto (separadas da interface, em utils/) ---
# carregar.py cuida de ler os arquivos, limpar sentinelas e juntar as tabelas
from utils.carregar import carregar_dados, montar_base_unificada, listar_localidades, ROTULOS_SEXO
# calcular.py cuida só de contas/estatísticas — não sabe nada sobre tkinter
from utils.calcular import (
    calcular_piramide_etaria,
    calcular_distribuicao_tamanho_domicilio,
    calcular_distribuicao_arranjos,
    calcular_perfil_complementar,
    calcular_estatisticas,
    ordenar_ras_por_tamanho_medio,
)
# exportar.py cuida de salvar os dados filtrados em arquivo
from utils.exportar import exportar_dados


class PDADExplorerApp:
    """Janela principal do sistema: carrega os dados, monta os widgets e
    conecta os filtros aos gráficos e estatísticas."""

    def __init__(self, root: tk.Tk) -> None:
        # 'root' é a janela principal do tkinter, criada em main() e passada
        # pra cá. Guardamos numa variável da classe (self.root) pra poder
        # usá-la em outros métodos depois.
        self.root = root

        # Texto que aparece na barra de título da janela (lá em cima, no SO)
        self.root.title("PDAD Explorer — Perfil demográfico e composição domiciliar")

        # Tamanho inicial da janela em pixels: largura x altura
        self.root.geometry("1000x720")

        # --- 1. Carregar dados (Requisito 1: indicação de registros carregados) ---
        # Chama a função do módulo carregar.py que lê os CSV/XLSX, filtra o
        # DF e remove os valores sentinela (99999/88888). Isso acontece UMA
        # vez, quando o programa abre — não a cada clique do usuário.
        self.moradores, self.domicilios = carregar_dados()

        # Junta (merge) as duas tabelas por A01nficha, trazendo a RA
        # (que só existe na tabela de domicílios) para cada morador.
        self.base = montar_base_unificada(self.moradores, self.domicilios)

        # Monta a lista de opções do filtro de RA: "Todos" + cada RA
        # encontrada nos dados, em ordem alfabética.
        self.ras = ["Todos"] + listar_localidades(self.domicilios)

        # tk.StringVar é uma "variável viva" do tkinter: quando ela muda de
        # valor (ex: o usuário escolhe outra RA no Combobox), qualquer
        # widget conectado a ela é avisado automaticamente. Começa em "Todos".
        self.ra_selecionada = tk.StringVar(value="Todos")

        # Vai guardar o último dicionário de estatísticas calculado, para
        # que o botão "Exportar" saiba o que salvar sem precisar recalcular.
        self.estatisticas_atuais = {}

        # Constrói os pedaços da tela, na ordem: cabeçalho, depois as abas.
        self._montar_cabecalho()
        self._montar_abas()

        # Faz o primeiro cálculo e desenho de tudo, assim que a janela abre
        # (sem isso, a tela ficaria em branco até o usuário mexer no filtro).
        self.atualizar_tudo()

    # ------------------------------------------------------------------ UI

    def _montar_cabecalho(self) -> None:
        """Monta o cabeçalho: título, descrição, contagem de registros e filtro de RA."""

        # Frame = um "retângulo invisível" que agrupa outros widgets.
        # padx/pady = espaçamento interno (em pixels) nas bordas horizontal/vertical.
        topo = tk.Frame(self.root, padx=12, pady=10)
        # .pack() posiciona o widget na janela. fill="x" faz o frame esticar
        # na largura toda da janela (mas não na altura).
        topo.pack(fill="x")

        # Título grande em negrito.
        tk.Label(
            topo, text="PDAD Explorer — Perfil demográfico e composição domiciliar",
            font=("Helvetica", 15, "bold")
        ).pack(anchor="w")  # anchor="w" = alinha à esquerda ("west")

        # Parágrafo de descrição, quebrando linha automaticamente depois de
        # 920 pixels de largura (wraplength) e alinhado à esquerda (justify).
        tk.Label(
            topo,
            text="Explore a pirâmide etária, a composição familiar dos domicílios e o perfil "
                 "de gênero/cor-raça do DF, por Região Administrativa (PDAD 2024).",
            wraplength=920, justify="left"
        ).pack(anchor="w", pady=(2, 8))

        # Label que mostra quantos registros foram carregados.
        # len(self.moradores) e len(self.domicilios) contam quantas linhas
        # (registros) sobraram depois da limpeza de sentinelas.
        # A f-string formata os números com separador de milhar (":,") e
        # depois trocamos a vírgula por ponto (padrão brasileiro).
        self.label_contagem = tk.Label(
            topo,
            text=f"{len(self.moradores):,} moradores · {len(self.domicilios):,} domicílios "
                 f"carregados (Distrito Federal)".replace(",", "."),
            fg="#2563eb", font=("Helvetica", 10, "bold")  # fg = cor do texto (foreground)
        )
        self.label_contagem.pack(anchor="w")

        # --- Requisito 2: filtro interativo (Combobox de RA) ---
        # Novo frame só para agrupar o filtro e o botão de exportar lado a lado.
        filtro_frame = tk.Frame(topo, pady=8)
        filtro_frame.pack(anchor="w")

        tk.Label(filtro_frame, text="Região Administrativa:").pack(side="left")

        # ttk.Combobox = a "caixa suspensa" onde o usuário escolhe a RA.
        # textvariable=self.ra_selecionada conecta o Combobox à StringVar:
        # quando o usuário escolhe algo, self.ra_selecionada é atualizada
        # automaticamente.
        # state="readonly" impede o usuário de digitar um valor que não
        # esteja na lista (só pode escolher entre as opções).
        combo = ttk.Combobox(
            filtro_frame, textvariable=self.ra_selecionada, values=self.ras,
            state="readonly", width=25
        )
        combo.pack(side="left", padx=6)  # side="left" empilha da esquerda pra direita

        # .bind() conecta um EVENTO (o usuário escolher uma opção no Combobox)
        # a uma AÇÃO (chamar self.atualizar_tudo()). O "<<ComboboxSelected>>"
        # é o nome do evento que o ttk dispara quando a seleção muda.
        # A função lambda existe porque o bind manda um argumento de evento
        # (e) para a função, mas atualizar_tudo() não precisa dele.
        combo.bind("<<ComboboxSelected>>", lambda e: self.atualizar_tudo())

        # Botão que abre o diálogo de exportação quando clicado.
        # command=self.abrir_dialogo_exportar diz qual função rodar ao clicar
        # (repare que NÃO tem parênteses aqui — senão a função rodaria na
        # hora de montar a tela, e não quando o usuário clicasse).
        tk.Button(
            filtro_frame, text="Exportar dados filtrados", command=self.abrir_dialogo_exportar
        ).pack(side="left", padx=12)

    def _montar_abas(self) -> None:
        """Monta as abas (Requisito 1: pelo menos duas funcionalidades distintas)."""

        # ttk.Notebook é o widget de "abas" (como abas de navegador).
        self.notebook = ttk.Notebook(self.root)
        # fill="both", expand=True faz o notebook ocupar todo o espaço
        # restante da janela (largura E altura), crescendo se a janela crescer.
        self.notebook.pack(fill="both", expand=True, padx=12, pady=8)

        # ============================== ABA 1: Pirâmide etária ==============================
        # Cada aba é, por baixo dos panos, um Frame normal — só é "registrado"
        # como aba através de self.notebook.add(frame, text="Nome da Aba").
        self.aba_piramide = tk.Frame(self.notebook)
        self.notebook.add(self.aba_piramide, text="Pirâmide etária")

        # Monta os 3 labels de estatística dentro dessa aba (ver método abaixo).
        self._montar_estatisticas(self.aba_piramide)

        # Cria a "tela em branco" do matplotlib (figsize em polegadas, dpi=resolução).
        self.figura_piramide = Figure(figsize=(7.8, 4.0), dpi=100)
        # add_subplot(111) cria 1 único gráfico dentro da figura (1 linha, 1
        # coluna, posição 1) — é o "eixo" onde de fato desenhamos as barras.
        self.eixo_piramide = self.figura_piramide.add_subplot(111)
        # Conecta essa Figure do matplotlib a um widget que o tkinter entende.
        self.canvas_piramide = FigureCanvasTkAgg(self.figura_piramide, master=self.aba_piramide)
        # .get_tk_widget() pega o "widget tkinter de verdade" dentro do canvas,
        # que é o que efetivamente colocamos na tela com .pack().
        self.canvas_piramide.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)

        # ============================== ABA 2: Composição domiciliar ==============================
        self.aba_domicilios = tk.Frame(self.notebook)
        self.notebook.add(self.aba_domicilios, text="Composição domiciliar")

        self.figura_domicilios = Figure(figsize=(7.8, 4.0), dpi=100)
        self.eixo_domicilios = self.figura_domicilios.add_subplot(111)
        self.canvas_domicilios = FigureCanvasTkAgg(self.figura_domicilios, master=self.aba_domicilios)
        self.canvas_domicilios.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)

        # Frame extra dentro da Aba 2, só para o texto do ranking de RAs
        # (fica abaixo do gráfico de barras).
        ranking_frame = tk.Frame(self.aba_domicilios, pady=6)
        ranking_frame.pack(fill="x")
        tk.Label(
            ranking_frame, text="Ranking de RAs por tamanho médio de domicílio "
                                 "(ordenado manualmente com Selection Sort):",
            font=("Helvetica", 9, "italic")
        ).pack(anchor="w")
        # Este Label começa vazio (sem texto="...") porque o conteúdo dele
        # é preenchido depois, dinamicamente, por _atualizar_ranking().
        self.label_ranking = tk.Label(ranking_frame, justify="left", anchor="w")
        self.label_ranking.pack(anchor="w")

        # ============================== ABA 3: Arranjo familiar + perfil ==============================
        # (id_genero e cor/raça, que não entram na pirâmide etária — ver
        # comentário detalhado dentro de _atualizar_grafico_piramide)
        self.aba_perfil = tk.Frame(self.notebook)
        self.notebook.add(self.aba_perfil, text="Arranjo familiar e perfil")

        self.figura_arranjos = Figure(figsize=(7.8, 3.4), dpi=100)
        self.eixo_arranjos = self.figura_arranjos.add_subplot(111)
        self.canvas_arranjos = FigureCanvasTkAgg(self.figura_arranjos, master=self.aba_perfil)
        self.canvas_arranjos.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)

        # Frame com os dois textos de perfil complementar (gênero e cor/raça),
        # abaixo do gráfico de arranjos.
        perfil_frame = tk.Frame(self.aba_perfil, pady=4)
        perfil_frame.pack(fill="x")
        # Ambos começam vazios — preenchidos por _atualizar_perfil_complementar().
        self.label_perfil_genero = tk.Label(perfil_frame, justify="left", anchor="w")
        self.label_perfil_genero.pack(anchor="w")
        self.label_perfil_cor_raca = tk.Label(perfil_frame, justify="left", anchor="w")
        self.label_perfil_cor_raca.pack(anchor="w")

    def _montar_estatisticas(self, container: tk.Frame) -> None:
        """Monta os labels de estatísticas descritivas (Requisito 4: pelo menos 3)."""
        # 'container' é o Frame (a aba) onde esses labels devem aparecer —
        # assim esse método pode ser reaproveitado em qualquer aba, não só na 1.
        stats_frame = tk.Frame(container, pady=6)
        stats_frame.pack(fill="x")

        # Os 3 labels começam vazios; o texto de verdade (com números) é
        # preenchido depois por _atualizar_labels_estatisticas(), toda vez
        # que o filtro de RA mudar.
        self.label_idade_media = tk.Label(stats_frame, font=("Helvetica", 10))
        self.label_idade_media.pack(anchor="w")
        self.label_tamanho_medio = tk.Label(stats_frame, font=("Helvetica", 10))
        self.label_tamanho_medio.pack(anchor="w")
        self.label_pct_criancas = tk.Label(stats_frame, font=("Helvetica", 10))
        self.label_pct_criancas.pack(anchor="w")

    # ------------------------------------------------------------- Ações

    def atualizar_tudo(self) -> None:
        """Recalcula estatísticas e redesenha os gráficos para a RA selecionada.

        Esta é a função "central": é chamada tanto na abertura do programa
        quanto toda vez que o usuário troca a RA no filtro. Ela não faz
        nenhum cálculo sozinha — só chama, em ordem, todas as funções que
        atualizam cada pedaço da tela.
        """
        # .get() lê o valor ATUAL da StringVar (a RA escolhida no Combobox).
        ra = self.ra_selecionada.get()

        # 1) Recalcula as estatísticas (idade média, tamanho médio, etc.)
        #    para a RA escolhida, usando a função de utils/calcular.py.
        self.estatisticas_atuais = calcular_estatisticas(self.base, self.domicilios, ra)

        # 2) Atualiza cada parte visual da tela, uma de cada vez:
        self._atualizar_labels_estatisticas(self.estatisticas_atuais)  # os 3 textos de estatística
        self._atualizar_grafico_piramide(ra)                            # gráfico da Aba 1
        self._atualizar_grafico_domicilios(ra)                          # gráfico da Aba 2
        self._atualizar_ranking()                                       # texto do ranking (Aba 2)
        self._atualizar_grafico_arranjos(ra)                            # gráfico da Aba 3
        self._atualizar_perfil_complementar(ra)                         # textos da Aba 3

    def _atualizar_labels_estatisticas(self, stats: dict) -> None:
        """Atualiza os labels de texto com as estatísticas descritivas (f-strings)."""
        # .config(text=...) muda o texto de um Label que já existe na tela
        # (diferente de criar um Label novo — aqui só trocamos o conteúdo).
        # stats é o dicionário devolvido por calcular_estatisticas(), então
        # stats['idade_media'] é um número (float) que formatamos com
        # ":.1f" para mostrar só 1 casa decimal.
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
        # Pede pro módulo calcular.py montar uma tabela: linhas = faixa
        # etária, colunas = sexo (1=Masculino, 2=Feminino), valores =
        # quantidade de moradores.
        piramide = calcular_piramide_etaria(self.base, ra)

        # .clear() apaga o desenho anterior do eixo — sem isso, cada troca
        # de filtro ia DESENHAR EM CIMA do gráfico antigo, acumulando barras.
        self.eixo_piramide.clear()

        faixas = piramide.index.tolist()  # lista das faixas etárias, ex: ["0-4", "5-11", ...]

        # Pirâmide etária clássica: homens desenhados para a ESQUERDA (por
        # isso o valor negativo) e mulheres para a DIREITA (valor positivo).
        # piramide.get(1, 0) pega a coluna do sexo 1 (Masculino); se essa
        # coluna não existir (ex: filtro sem nenhum homem), usa 0 no lugar.
        homens = -piramide.get(1, 0)
        mulheres = piramide.get(2, 0)

        # barh() = gráfico de barras HORIZONTAIS (a versão vertical seria .bar()).
        # ROTULOS_SEXO[1] e [2] transformam o código numérico em texto
        # legível ("Masculino"/"Feminino") só para a legenda do gráfico.
        self.eixo_piramide.barh(faixas, homens, color="#2563eb", label=ROTULOS_SEXO[1])
        self.eixo_piramide.barh(faixas, mulheres, color="#db2777", label=ROTULOS_SEXO[2])

        self.eixo_piramide.set_title(f"Pirâmide etária por sexo — {ra}")
        self.eixo_piramide.set_xlabel("Número de moradores")
        self.eixo_piramide.set_ylabel("Faixa etária")
        self.eixo_piramide.legend()  # desenha a legenda (caixinha com as cores)

        # Linha vertical em x=0, para marcar visualmente onde "homens" termina
        # e "mulheres" começa (já que um lado é negativo e o outro positivo).
        self.eixo_piramide.axvline(0, color="black", linewidth=0.5)

        # tight_layout() ajusta as margens automaticamente para nada ficar
        # cortado (títulos, rótulos dos eixos, etc.).
        self.figura_piramide.tight_layout()

        # .draw() manda o matplotlib efetivamente RENDERIZAR o gráfico na
        # tela — sem essa chamada, as mudanças feitas acima não apareceriam.
        self.canvas_piramide.draw()

    def _atualizar_grafico_domicilios(self, ra: str) -> None:
        """Redesenha a distribuição de domicílios por tamanho (Diferencial
        D1: segundo tipo de gráfico, complementando a pirâmide etária)."""
        # calcular_distribuicao_tamanho_domicilio devolve uma Series do
        # pandas: índice = número de pessoas no domicílio, valor = quantos
        # domicílios têm esse tamanho.
        distribuicao = calcular_distribuicao_tamanho_domicilio(self.domicilios, ra)

        self.eixo_domicilios.clear()

        # .bar() = gráfico de barras VERTICAIS.
        # distribuicao.index.astype(str) converte os números do eixo X
        # (1, 2, 3...) para texto, para o matplotlib tratá-los como
        # categorias (senão poderia tentar interpolar entre 1 e 2, etc.).
        self.eixo_domicilios.bar(distribuicao.index.astype(str), distribuicao.values, color="#16a34a")
        self.eixo_domicilios.set_title(f"Domicílios por número de moradores — {ra}")
        self.eixo_domicilios.set_xlabel("Número de pessoas no domicílio")
        self.eixo_domicilios.set_ylabel("Número de domicílios")
        self.figura_domicilios.tight_layout()
        self.canvas_domicilios.draw()

    def _atualizar_ranking(self) -> None:
        """Atualiza o texto do ranking de RAs por tamanho médio de domicílio."""
        # ordenar_ras_por_tamanho_medio() devolve uma lista de tuplas
        # [(nome_da_ra, media), ...], já ordenada do maior para o menor
        # usando Selection Sort implementado à mão (Diferencial D4).
        ranking = ordenar_ras_por_tamanho_medio(self.domicilios)

        # Monta uma linha de texto por RA, numerada (1., 2., 3., ...),
        # mas só para as 10 primeiras (ranking[:10]) para não estourar a tela.
        # enumerate(ranking[:10]) gera pares (índice, item) começando em 0,
        # por isso usamos i+1 para a numeração começar em 1.
        linhas = [f"{i+1}. {ra} — {media:.2f} pessoas/domicílio" for i, (ra, media) in enumerate(ranking[:10])]

        # "\n".join(linhas) junta a lista de textos numa string só, com
        # quebra de linha entre cada item, para exibir tudo num único Label.
        self.label_ranking.config(text="\n".join(linhas))

    def _atualizar_grafico_arranjos(self, ra: str) -> None:
        """Redesenha a distribuição de domicílios por tipo de arranjo familiar."""
        # Series do pandas: índice = tipo de arranjo (ex: "Casal com 1 filho"),
        # valor = quantos domicílios têm esse arranjo.
        distribuicao = calcular_distribuicao_arranjos(self.domicilios, ra)

        self.eixo_arranjos.clear()
        # Barras horizontais de novo aqui, porque os nomes dos arranjos são
        # longos ("Casal com 3 filhos ou mais") e ficam mais legíveis no
        # eixo vertical do que espremidos no eixo horizontal.
        self.eixo_arranjos.barh(distribuicao.index, distribuicao.values, color="#f59e0b")
        self.eixo_arranjos.set_title(f"Domicílios por tipo de arranjo familiar — {ra}")
        self.eixo_arranjos.set_xlabel("Número de domicílios")
        self.figura_arranjos.tight_layout()
        self.canvas_arranjos.draw()

    def _atualizar_perfil_complementar(self, ra: str) -> None:
        """Atualiza os textos de perfil de gênero (id_genero) e cor/raça (E05)."""
        # calcular_perfil_complementar() devolve um dicionário com duas
        # Series do pandas: uma para id_genero (%), outra para E05 (%).
        perfil = calcular_perfil_complementar(self.base, ra)

        # Para cada categoria (ex: "Cisgênero") e sua porcentagem, monta uma
        # linha de texto "  Categoria: XX.X%". .items() percorre a Series
        # como pares (índice, valor).
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
        # filedialog.asksaveasfilename() abre a janela NATIVA do sistema
        # operacional (a mesma que qualquer programa usa) para o usuário
        # escolher onde salvar e com que nome.
        # defaultextension=".csv" -> se o usuário não digitar extensão, usa .csv
        # filetypes -> define os filtros que aparecem no seletor de arquivos
        caminho = filedialog.asksaveasfilename(
            title="Exportar dados filtrados",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("Texto", "*.txt")],
        )

        # Se o usuário clicar em "Cancelar" na janela de salvar, caminho
        # volta como uma string vazia "" — nesse caso, não fazemos nada.
        if not caminho:
            return

        # Chama a função de utils/exportar.py, passando as estatísticas
        # atuais (calculadas na última vez que atualizar_tudo() rodou),
        # o nome da RA selecionada, e o caminho escolhido pelo usuário.
        exportar_dados(self.estatisticas_atuais, self.ra_selecionada.get(), caminho)

        # Mostra uma janelinha de confirmação para o usuário saber que deu certo.
        messagebox.showinfo("Exportação concluída", f"Dados exportados para:\n{caminho}")


def main() -> None:
    """Ponto de entrada: cria a janela raiz e inicia o loop principal do tkinter."""
    # tk.Tk() cria a JANELA PRINCIPAL do programa (ainda vazia, sem widgets).
    root = tk.Tk()

    # Cria o "aplicativo" de verdade, passando essa janela para ele —
    # é dentro do __init__ da classe que todos os widgets são montados.
    PDADExplorerApp(root)

    # root.mainloop() inicia o "loop de eventos" do tkinter: o programa
    # fica escutando cliques, teclas, seleções no Combobox, etc., e chamando
    # as funções conectadas a cada evento (via .bind() ou command=...).
    # O código FICA PARADO nessa linha até a janela ser fechada.
    root.mainloop()


# Esse "if" só é verdadeiro quando o arquivo é executado diretamente
# (python sistema.py) — e não quando ele é importado por outro arquivo
# (ex: um teste que faz "from sistema import PDADExplorerApp").
# É uma convenção padrão do Python para separar "código que roda ao
# executar o arquivo" de "código reutilizável ao importar o arquivo".
if __name__ == "__main__":
    main()

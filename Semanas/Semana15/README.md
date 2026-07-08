# Semana 15 — Projeto final, robótica educacional e GitHub Pages

**Conceito principal:** síntese de todo o semestre — projeto final,
robótica virtual integradora, publicação do portfólio via GitHub Pages,
peer review entre colegas.

## Arquivos

- **`projeto_final/`** — recurso educacional final (README, proposta
  pedagógica, código em `src/main.py`, reaproveitando o CSV de escolas da
  semana 11).
- **`projeto_robotica_integrador.md`** — projeto Tinkercad integrador:
  simulador ambiental com sensor de temperatura + sensor ultrassônico,
  lógica de alerta condicional e log de dados via Serial Monitor.
- **`roteiro_apresentacao.md`** — estrutura para a apresentação de 10 min +
  5 de perguntas na segunda-feira.
- **`peer_review.md`** — template para a issue de peer review (elogio +
  sugestão) a ser aberta no repositório de um(a) colega.
- **`configurar_github_pages.md`** — passo a passo para ativar o GitHub
  Pages e publicar a URL.
- **`../index.html`** (na raiz do repositório) — página pessoal publicada
  via GitHub Pages: apresentação, projetos OctoStudio, projetos Python,
  robótica, reflexão sobre o semestre.

## Como rodar o projeto final

```bash
cd projeto_final/src
python3 main.py
python3 -m doctest main.py -v
```

## Checklist de encerramento do semestre

- [ ] Preencher o tema real do projeto final em `projeto_final/README.md`
- [ ] Preencher a proposta pedagógica
- [ ] Print do projeto Tinkercad integrador
- [ ] Apresentar (10 min) usando `roteiro_apresentacao.md`
- [ ] Abrir issue de peer review no repositório de um(a) colega
- [ ] Ativar GitHub Pages (`configurar_github_pages.md`)
- [ ] Escrever a reflexão final no `index.html` e no `README.md` da raiz
- [ ] Registrar a URL do GitHub Pages no formulário da turma

"""
Semana 12 - Estruturas de dados heterogêneas
Simulador 9: agenda de contatos usando dicionários aninhados, busca por
nome e exportação/leitura em JSON.
"""

import json


def criar_agenda() -> dict:
    """Cria uma agenda inicial com alguns contatos de exemplo."""
    return {
        "Ana Souza": {"telefone": "(61) 99999-0001", "email": "ana@exemplo.com"},
        "Bruno Lima": {"telefone": "(61) 99999-0002", "email": "bruno@exemplo.com"},
    }


def adicionar_contato(agenda: dict, nome: str, telefone: str, email: str) -> dict:
    """Adiciona (ou sobrescreve) um contato na agenda.

    >>> agenda = {}
    >>> agenda = adicionar_contato(agenda, "Carla", "111", "c@x.com")
    >>> agenda["Carla"]["telefone"]
    '111'
    """
    agenda[nome] = {"telefone": telefone, "email": email}
    return agenda


def buscar_contato(agenda: dict, nome: str) -> dict | None:
    """Busca um contato pelo nome exato (chave do dicionário — O(1) médio).

    >>> agenda = {"Ana": {"telefone": "1", "email": "a@x.com"}}
    >>> buscar_contato(agenda, "Ana")
    {'telefone': '1', 'email': 'a@x.com'}
    >>> buscar_contato(agenda, "Zeca") is None
    True
    """
    return agenda.get(nome)


def salvar_json(agenda: dict, caminho: str) -> None:
    """Exporta a agenda para um arquivo JSON."""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(agenda, f, ensure_ascii=False, indent=2)


def carregar_json(caminho: str) -> dict:
    """Lê uma agenda a partir de um arquivo JSON."""
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    agenda = criar_agenda()
    agenda = adicionar_contato(agenda, "Carla Dias", "(61) 99999-0003", "carla@exemplo.com")
    salvar_json(agenda, "agenda.json")
    recarregada = carregar_json("agenda.json")
    print("Contato encontrado:", buscar_contato(recarregada, "Carla Dias"))

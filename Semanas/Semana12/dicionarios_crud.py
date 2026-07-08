"""
Semana 12 - Dicionários Python: chave-valor, hashing intuitivo, CRUD

Hashing intuitivo: um dicionário Python guarda cada par chave-valor numa
posição calculada a partir de um "hash" da chave (um número gerado pela
função hash()). É por isso que dict["Ana"] é quase instantâneo (O(1) médio)
mesmo com milhões de registros — o Python não precisa percorrer a lista
inteira como faria uma busca linear, ele "pula direto" para a posição
calculada a partir do hash da chave.
"""


def exemplo_hash() -> None:
    """Mostra que strings iguais sempre geram o mesmo hash (mesma posição),
    e que é por isso que dicionários conseguem localizar uma chave direto."""
    print("hash('Ana'):", hash("Ana"))
    print("hash('Ana') de novo:", hash("Ana"))  # sempre igual na mesma execução
    print("hash('Bruno'):", hash("Bruno"))       # posição diferente


def crud_dicionario() -> None:
    """Demonstra as quatro operações CRUD (Create, Read, Update, Delete)
    num dicionário representando um contato."""
    contatos = {}

    # CREATE
    contatos["Ana Souza"] = {"telefone": "(61) 99999-0001", "email": "ana@exemplo.com"}
    print("CREATE:", contatos)

    # READ
    ana = contatos["Ana Souza"]
    print("READ:", ana)
    ana_ou_none = contatos.get("Zeca")  # get() evita KeyError se não existir
    print("READ (chave inexistente com get):", ana_ou_none)

    # UPDATE
    contatos["Ana Souza"]["telefone"] = "(61) 98888-0001"
    print("UPDATE:", contatos["Ana Souza"])

    # DELETE
    del contatos["Ana Souza"]
    print("DELETE — contatos restantes:", contatos)


if __name__ == "__main__":
    print("=== Hashing intuitivo ===")
    exemplo_hash()
    print("\n=== CRUD com dicionário ===")
    crud_dicionario()

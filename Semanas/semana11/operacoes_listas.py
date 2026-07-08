"""
Semana 11 - Listas em Python: criação, indexação, fatiamento, mutabilidade
Demonstração das operações pedidas no plano de aula: append, insert, remove,
sort, len, in — e percurso com for, enumerate e zip.
"""


def demonstrar_operacoes_basicas() -> None:
    """Criação, indexação, fatiamento e mutabilidade de listas."""
    notas = [7.5, 8.0, 6.5, 9.0, 5.5]
    print("Lista original:", notas)
    print("Indexação notas[0]:", notas[0])
    print("Indexação notas[-1]:", notas[-1])
    print("Fatiamento notas[1:3]:", notas[1:3])

    # mutabilidade: alterar um elemento no lugar
    notas[0] = 7.8
    print("Após notas[0] = 7.8:", notas)


def demonstrar_operacoes_de_lista() -> None:
    """append, insert, remove, sort, len, in."""
    notas = [7.5, 8.0, 6.5]

    notas.append(9.0)
    print("Após append(9.0):", notas)

    notas.insert(0, 10.0)
    print("Após insert(0, 10.0):", notas)

    notas.remove(6.5)
    print("Após remove(6.5):", notas)

    print("len(notas):", len(notas))
    print("9.0 in notas:", 9.0 in notas)
    print("6.5 in notas:", 6.5 in notas)  # já removido

    notas.sort()
    print("Após sort():", notas)

    notas.sort(reverse=True)
    print("Após sort(reverse=True):", notas)


def demonstrar_percurso(escolas: list[dict]) -> None:
    """Percurso de listas com for, enumerate e zip."""
    print("--- for simples ---")
    for e in escolas:
        print(f"- {e['escola']}")

    print("--- enumerate (índice + valor) ---")
    for i, e in enumerate(escolas, start=1):
        print(f"{i}. {e['escola']}")

    print("--- zip (percorrer duas listas em paralelo) ---")
    nomes = [e["escola"] for e in escolas]
    notas_mat = [e["proficiencia_matematica"] for e in escolas]
    for nome, nota in zip(nomes, notas_mat):
        print(f"{nome}: {nota}")


if __name__ == "__main__":
    import csv

    print("=== 1. Operações básicas de lista ===")
    demonstrar_operacoes_basicas()

    print("\n=== 2. append, insert, remove, sort, len, in ===")
    demonstrar_operacoes_de_lista()

    print("\n=== 3. Percurso: for, enumerate, zip ===")
    with open("escolas_amostra.csv", encoding="utf-8") as f:
        escolas = list(csv.DictReader(f))
        for e in escolas:
            e["proficiencia_matematica"] = float(e["proficiencia_matematica"])
    demonstrar_percurso(escolas)

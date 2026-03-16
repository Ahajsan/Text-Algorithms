from lab_3.aho_corasick_algorithm import AhoCorasick
from collections import defaultdict

def find_pattern_in_column(text_column: str, pattern_columns: list[str]) -> list[tuple[int, int]]:
    """
    Wyszukuje wszystkie kolumny wzorca w kolumnie tekstu.

    Args:
        text_column: Kolumna tekstu
        pattern_columns: Lista kolumn wzorca

    Returns:
        Lista krotek (pozycja, indeks kolumny), gdzie znaleziono kolumnę wzorca
    """
    # TODO: Zaimplementuj wyszukiwanie kolumn wzorca w kolumnie tekstu
    # TODO: Dla każdej kolumny wzorca, przeszukaj kolumnę tekstu
    # TODO: Zwróć listę krotek (pozycja, indeks kolumny) dla znalezionych dopasowań

    pattern_to_indices = defaultdict(list)
    for i, pattern in enumerate(pattern_columns):
        pattern_to_indices[pattern].append(i)

    ac = AhoCorasick(pattern_columns)
    tmp = ac.search(text_column)

    result = []
    for pos, matched_pattern in tmp:
        for idx in pattern_to_indices[matched_pattern]:
            result.append((pos, idx))

    return result

def find_pattern_2d(text: list[str], pattern: list[str]) -> list[tuple[int, int]]:
    """
    Wyszukuje wzorzec dwuwymiarowy w tekście dwuwymiarowym.

    Args:
        text: Tekst dwuwymiarowy (lista ciągów znaków tej samej długości)
        pattern: Wzorzec dwuwymiarowy (lista ciągów znaków tej samej długości)

    Returns:
        Lista krotek (i, j), gdzie (i, j) to współrzędne lewego górnego rogu wzorca w tekście
    """
    # TODO: Zaimplementuj wyszukiwanie wzorca dwuwymiarowego
    # TODO: Obsłuż przypadki brzegowe (pusty tekst/wzorzec, wymiary)
    # TODO: Sprawdź, czy wszystkie wiersze mają taką samą długość
    # TODO: Zaimplementuj algorytm wyszukiwania dwuwymiarowego
    # TODO: Zwróć listę współrzędnych lewego górnego rogu dopasowanego wzorca

    if pattern == [] or text == [] or len(pattern) > len(text) or len(pattern[0]) > len(text[0]):

        return []

    x = pattern[0]
    n = len(x)
    for y in pattern:
        if n != len(y):
            return []

    x = text[0]
    n = len(x)
    for y in text:
        if n != len(y):
            return []

    T = [[None for _ in range(n)] for _ in range(len(text))]

    pattern_columns = []
    for i in range(len(pattern[0])):
        tmp = ""
        for j in range(len(pattern)):
            tmp += pattern[j][i]
        pattern_columns.append(tmp)

    for i in range(len(text[0])):
        tmp = ""
        for j in range(len(text)):
            tmp += text[j][i]
        matches = find_pattern_in_column(tmp, pattern_columns)
        for x, y in matches:
            if T[x][i] is None:
                T[x][i] = set()
            T[x][i].add(y)

    result = []
    mx = len(pattern[0]) - 1
    for i in range(len(text)):
        for j in range(len(text[0]) - mx):
            if T[i][j] is not None and 0 in T[i][j]:
                cnt = 0
                while j + cnt + 1 < len(text[0]) and T[i][j + cnt + 1] is not None and cnt + 1 in T[i][j + cnt + 1]:
                    cnt += 1
                if cnt == mx:
                    result.append((i,j))

    return result




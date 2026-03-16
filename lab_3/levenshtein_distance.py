def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Oblicza odległość Levenshteina między dwoma ciągami znaków.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość Levenshteina (minimalna liczba operacji wstawienia, usunięcia
        lub zamiany znaku potrzebnych do przekształcenia s1 w s2)
    """
    # TODO: Zaimplementuj obliczanie odległości Levenshteina
    # TODO: Obsłuż przypadki brzegowe (puste ciągi)
    # TODO: Zaimplementuj algorytm dynamicznego programowania do obliczenia odległości

    n1 = len(s1)
    n2 = len(s2)
    if n1 == 0 | n2 == 0:
        return max(n1, n2)

    result = 0
    if n1 == n2:
        for i in range(n2):
            if s1[i] != s2[i]:
                result += 1
        return result

    result += abs(n1 - n2)
    if n1 > n2:
        s1, n1, s2, n2 = s2, n2, s1, n1

    cnt = n1
    j = 0

    for i in range(n1):
        k = j
        while j < n2:
            if s1[i] == s2[j]:
                cnt -= 1
                j += 1
                break
            j += 1
        if j == n2:
            j = k
    return result + cnt




def hamming_distance(s1: str, s2: str) -> int:
    """
    Oblicza odległość Hamminga między dwoma ciągami znaków.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość Hamminga (liczba pozycji, na których znaki się różnią)
        Jeśli ciągi mają różne długości, zwraca -1
    """
    # TODO: Zaimplementuj obliczanie odległości Hamminga
    if len(s1) != len(s2):
        return -1
    cnt = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            cnt += 1
    return cnt


def set_nth_bit(n: int) -> int:
    """
    Zwraca maskę bitową z ustawionym n-tym bitem na 1.

    Args:
        n: Pozycja bitu do ustawienia (0-indeksowana)

    Returns:
        Maska bitowa z n-tym bitem ustawionym na 1
    """
    # TODO: Zaimplementuj ustawianie n-tego bitu
    return 1 << n


def nth_bit(m: int, n: int) -> int:
    """
    Zwraca wartość n-tego bitu w masce m.

    Args:
        m: Maska bitowa
        n: Pozycja bitu do odczytania (0-indeksowana)

    Returns:
        Wartość n-tego bitu (0 lub 1)
    """
    # TODO: Zaimplementuj odczytywanie n-tego bitu
    return (m >> n) & 1


def make_mask(pattern: str) -> list:
    """
    Tworzy tablicę masek dla algorytmu Shift-Or.

    Args:
        pattern: Wzorzec do wyszukiwania

    Returns:
        Tablica 256 masek, gdzie każda maska odpowiada jednemu znakowi ASCII
    """
    # TODO: Zaimplementuj tworzenie tablicy masek
    m = [0xFF] * 256
    for j, c in enumerate(pattern):
        m[ord(c)] &= ~set_nth_bit(j)
    return m


def fuzzy_shift_or(text: str, pattern: str, k: int = 2) -> list[int]:
    """
    Implementacja przybliżonego wyszukiwania wzorca przy użyciu algorytmu Shift-Or.

    Args:
        text: Tekst do przeszukania
        pattern: Wzorzec do wyszukiwania
        k: Maksymalna dopuszczalna liczba różnic (odległość Hamminga)

    Returns:
        Lista pozycji (0-indeksowanych), na których znaleziono wzorzec
        z maksymalnie k różnicami
    """
    # TODO: Zaimplementuj algorytm przybliżonego wyszukiwania Shift-Or
    # TODO: Obsłuż przypadki brzegowe (pusty wzorzec, wzorzec dłuższy niż tekst, k < 0)
    # TODO: Zaimplementuj główną logikę algorytmu

    if pattern == "" or pattern is None or k < 0 or len(pattern) > len(text) or text is None:
        return []
    m = make_mask(pattern)

    S = [~0] * (k + 1)
    result = []

    for i, c in enumerate(text):
        prev = S[0]
        S[0] = ((S[0] << 1) | m[ord(c)])
        for j in range(1, k + 1):
            temp = S[j]
            S[j] = ((S[j] << 1) | m[ord(c)]) & (prev << 1)
            prev = temp
        if nth_bit(S[k], len(pattern) - 1) == 0:
            result.append(i - len(pattern) + 1)

    return result
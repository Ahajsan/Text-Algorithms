def wagner_fischer(s1: str, s2: str,
                   insert_cost: int = 1,
                   delete_cost: int = 1,
                   substitute_cost: int = 1) -> int:
    """
    Oblicza odległość edycyjną używając algorytmu Wagnera-Fischera (programowanie dynamiczne).

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków
        insert_cost: Koszt operacji wstawienia
        delete_cost: Koszt operacji usunięcia
        substitute_cost: Koszt operacji zamiany

    Returns:
        Odległość edycyjna z uwzględnieniem kosztów operacji
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i * delete_cost
    for j in range(n + 1):
        dp[0][j] = j * insert_cost

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost_sub = 0 if s1[i - 1] == s2[j - 1] else substitute_cost
            dp[i][j] = min(
                dp[i - 1][j] + delete_cost,
                dp[i][j - 1] + insert_cost,
                dp[i - 1][j - 1] + cost_sub
            )
    return dp[m][n]


def wagner_fischer_with_alignment(s1: str, s2: str) -> tuple[int, str, str]:
    """
    Oblicza odległość edycyjną i zwraca wyrównanie sekwencji.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Krotka zawierająca odległość edycyjną i dwa wyrównane ciągi
        (w wyrównanych ciągach '-' oznacza lukę)
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    backtrack = [[(0, 0)] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
        if i > 0:
            backtrack[i][0] = (i - 1, 0)
    for j in range(n + 1):
        dp[0][j] = j
        if j > 0:
            backtrack[0][j] = (0, j - 1)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost_sub = 0 if s1[i - 1] == s2[j - 1] else 1
            choices = [
                (dp[i - 1][j] + 1, (i - 1, j)),      # DELETE
                (dp[i][j - 1] + 1, (i, j - 1)),      # INSERT
                (dp[i - 1][j - 1] + cost_sub, (i - 1, j - 1))  # SUBSTITUTE or MATCH
            ]
            dp[i][j], backtrack[i][j] = min(choices)

    aligned_s1, aligned_s2 = "", ""
    i, j = m, n
    while i > 0 or j > 0:
        prev_i, prev_j = backtrack[i][j]
        if prev_i == i - 1 and prev_j == j - 1:
            aligned_s1 = (s1[i - 1] if i > 0 else '-') + aligned_s1
            aligned_s2 = (s2[j - 1] if j > 0 else '-') + aligned_s2
        elif prev_i == i - 1 and prev_j == j:
            aligned_s1 = s1[i - 1] + aligned_s1
            aligned_s2 = '-' + aligned_s2
        else:
            aligned_s1 = '-' + aligned_s1
            aligned_s2 = s2[j - 1] + aligned_s2
        i, j = prev_i, prev_j

    return dp[m][n], aligned_s1, aligned_s2


def wagner_fischer_space_optimized(s1: str, s2: str) -> int:
    """
    Oblicza odległość edycyjną używając zoptymalizowanej pamięciowo wersji algorytmu.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość edycyjna
    """
    m, n = len(s1), len(s2)

    if m < n:
        s1, s2 = s2, s1
        m, n = n, m

    prev = list(range(n + 1))
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            curr[j] = min(
                prev[j] + 1,
                curr[j - 1] + 1,
                prev[j - 1] + cost
            )
        prev, curr = curr, prev

    return prev[n]

def allison_global_alignment(s1: str, s2: str,
                             match_score: int = 2,
                             mismatch_score: int = -1,
                             gap_penalty: int = -1) -> tuple[int, str, str]:
    """
    Znajduje optymalne globalne wyrównanie używając algorytmu Allisona.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków
        match_score: Punkty za dopasowanie
        mismatch_score: Punkty za niedopasowanie
        gap_penalty: Kara za lukę

    Returns:
        Krotka zawierająca wynik wyrównania i dwa wyrównane ciągi
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    bt = [[(0, 0)] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        dp[i][0] = i * gap_penalty
        bt[i][0] = (i - 1, 0)
    for j in range(1, n + 1):
        dp[0][j] = j * gap_penalty
        bt[0][j] = (0, j - 1)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                score = match_score
            else:
                score = mismatch_score

            choices = [
                (dp[i - 1][j - 1] + score, (i - 1, j - 1)),
                (dp[i - 1][j] + gap_penalty, (i - 1, j)),
                (dp[i][j - 1] + gap_penalty, (i, j - 1))
            ]
            dp[i][j], bt[i][j] = max(choices)

    aligned_s1 = ""
    aligned_s2 = ""
    i, j = m, n
    while i > 0 or j > 0:
        pi, pj = bt[i][j]
        if pi == i - 1 and pj == j - 1:
            aligned_s1 = s1[i - 1] + aligned_s1
            aligned_s2 = s2[j - 1] + aligned_s2
        elif pi == i - 1 and pj == j:
            aligned_s1 = s1[i - 1] + aligned_s1
            aligned_s2 = '-' + aligned_s2
        else:
            aligned_s1 = '-' + aligned_s1
            aligned_s2 = s2[j - 1] + aligned_s2
        i, j = pi, pj

    return dp[m][n], aligned_s1, aligned_s2


def allison_local_alignment(s1: str, s2: str,
                            match_score: int = 2,
                            mismatch_score: int = -1,
                            gap_penalty: int = -1) -> tuple[int, str, str, int, int]:
    """
    Znajduje optymalne lokalne wyrównanie (podobnie do algorytmu Smith-Waterman).

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków
        match_score: Punkty za dopasowanie
        mismatch_score: Punkty za niedopasowanie
        gap_penalty: Kara za lukę

    Returns:
        Krotka zawierająca wynik wyrównania, dwa wyrównane ciągi oraz pozycje początku
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    bt = [[(0, 0)] * (n + 1) for _ in range(m + 1)]

    max_score = 0
    max_pos = (0, 0)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                score = match_score
            else:
                score = mismatch_score

            choices = [
                (0, (0, 0)),
                (dp[i - 1][j - 1] + score, (i - 1, j - 1)),
                (dp[i - 1][j] + gap_penalty, (i - 1, j)),
                (dp[i][j - 1] + gap_penalty, (i, j - 1))
            ]
            dp[i][j], bt[i][j] = max(choices)
            if dp[i][j] > max_score:
                max_score = dp[i][j]
                max_pos = (i, j)

    i, j = max_pos
    aligned_s1 = ""
    aligned_s2 = ""

    while dp[i][j] != 0:
        pi, pj = bt[i][j]
        if pi == i - 1 and pj == j - 1:
            aligned_s1 = s1[i - 1] + aligned_s1
            aligned_s2 = s2[j - 1] + aligned_s2
        elif pi == i - 1 and pj == j:
            aligned_s1 = s1[i - 1] + aligned_s1
            aligned_s2 = '-' + aligned_s2
        else:
            aligned_s1 = '-' + aligned_s1
            aligned_s2 = s2[j - 1] + aligned_s2
        i, j = pi, pj

    return max_score, aligned_s1, aligned_s2, i, j

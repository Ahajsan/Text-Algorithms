def naive_edit_distance(s1: str, s2: str) -> int:
    """
    Oblicza odległość edycyjną między dwoma ciągami używając naiwnego algorytmu rekurencyjnego.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość edycyjna (minimalna liczba operacji wstawienia, usunięcia
        lub zamiany znaku potrzebnych do przekształcenia s1 w s2)
    """
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)

    if s1[0] == s2[0]:
        return naive_edit_distance(s1[1:], s2[1:])
    else:
        insert_op = 1 + naive_edit_distance(s1, s2[1:])
        delete_op = 1 + naive_edit_distance(s1[1:], s2)
        replace_op = 1 + naive_edit_distance(s1[1:], s2[1:])
        return min(insert_op, delete_op, replace_op)


def naive_edit_distance_with_operations(s1: str, s2: str) -> tuple[int, list[str]]:
    """
    Oblicza odległość edycyjną i zwraca listę operacji potrzebnych do przekształcenia s1 w s2.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Krotka zawierająca odległość edycyjną i listę operacji
        Operacje: "INSERT x", "DELETE x", "REPLACE x->y", "MATCH x"
    """
    if not s1:
        return len(s2), [f"INSERT {c}" for c in s2]
    if not s2:
        return len(s1), [f"DELETE {c}" for c in s1]

    if s1[0] == s2[0]:
        dist, ops = naive_edit_distance_with_operations(s1[1:], s2[1:])
        return dist, ["MATCH " + s1[0]] + ops
    else:
        # INSERT
        dist_insert, ops_insert = naive_edit_distance_with_operations(s1, s2[1:])
        # DELETE
        dist_delete, ops_delete = naive_edit_distance_with_operations(s1[1:], s2)
        # REPLACE
        dist_replace, ops_replace = naive_edit_distance_with_operations(s1[1:], s2[1:])

        min_dist = min(dist_insert + 1, dist_delete + 1, dist_replace + 1)

        if min_dist == dist_insert + 1:
            return min_dist, [f"INSERT {s2[0]}"] + ops_insert
        elif min_dist == dist_delete + 1:
            return min_dist, [f"DELETE {s1[0]}"] + ops_delete
        else:
            return min_dist, [f"REPLACE {s1[0]}->{s2[0]}"] + ops_replace

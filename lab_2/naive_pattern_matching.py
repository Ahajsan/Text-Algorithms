def naive_pattern_match(text: str, pattern: str) -> list[int]:
    """
    Implementation of the naive pattern matching algorithm.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # TODO: Implement the naive pattern matching algorithm
    # This is the most straightforward approach to string matching:
    # 1. Check every possible starting position in the text
    # 2. For each position, compare the pattern with the text character by character
    # 3. If all characters match, add the starting position to the results
    # 4. Handle edge cases like empty patterns and patterns longer than the text

    def is_it_pattern(text, pattern, i):
        cnt = 1
        j = i + 1
        while cnt < len(pattern) and j < len(text) and text[j] == pattern[cnt]:
            j += 1
            cnt += 1
        return i if cnt == len(pattern) else None

    if pattern == "" or text == "":
        return []
    i = 0
    result = []
    while i < len(text) - len(pattern) + 1:
        if text[i] == pattern[0]:
            x = is_it_pattern(text, pattern, i)
            if x is not None:
                result.append(i)
        i += 1
    return result
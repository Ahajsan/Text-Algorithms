from typing import List

def build_suffix_array(s: str) -> List[int]:
    return sorted(range(len(s)), key=lambda i: s[i:])

def build_lcp(s: str, sa: List[int]) -> List[int]:
    n = len(s)
    rank = [0] * n
    for i, suffix in enumerate(sa):
        rank[suffix] = i

    lcp = [0] * (n - 1)
    k = 0
    for i in range(n):
        if rank[i] == n - 1:
            k = 0
            continue
        j = sa[rank[i] + 1]
        while i + k < n and j + k < n and s[i + k] == s[j + k]:
            k += 1
        lcp[rank[i]] = k
        if k:
            k -= 1
    return lcp

def longest_common_substring(str1: str, str2: str) -> str:
    combined = str1 + '#' + str2 + '$'
    separator_index = len(str1)

    sa = build_suffix_array(combined)
    lcp = build_lcp(combined, sa)

    max_len = 0
    max_pos = 0
    for i in range(1, len(combined)):
        in_first = sa[i] < separator_index
        in_second = sa[i - 1] < separator_index
        if in_first != in_second and lcp[i - 1] > max_len:
            max_len = lcp[i - 1]
            max_pos = sa[i]
    return combined[max_pos:max_pos + max_len]

def longest_common_substring_multiple(strings: List[str]) -> str:
    if not strings:
        return ""
    if len(strings) == 1:
        return strings[0]

    separators = [chr(256 + i) for i in range(len(strings))]
    combined = ""
    owner = []

    for i, s in enumerate(strings):
        combined += s + separators[i]
        owner += [i] * (len(s) + 1)

    sa = build_suffix_array(combined)
    lcp = build_lcp(combined, sa)

    max_len = 0
    max_pos = 0
    total_strings = len(strings)

    from collections import Counter

    i = 0
    while i < len(lcp):
        seen = set()
        j = i
        while j < len(lcp) and len(seen) < total_strings:
            seen.add(owner[sa[j]])
            seen.add(owner[sa[j + 1]])
            j += 1
        if len(seen) == total_strings:
            min_lcp = min(lcp[i:j])
            if min_lcp > max_len:
                max_len = min_lcp
                max_pos = sa[i]
        i += 1

    return combined[max_pos:max_pos + max_len]


def longest_palindromic_substring(text: str) -> str:
    if not text:
        return ""

    rev = text[::-1]
    combined = text + "#" + rev + "$"
    sep_index = len(text)

    sa = build_suffix_array(combined)
    lcp = build_lcp(combined, sa)

    max_len = 0
    max_pos = 0
    for i in range(1, len(combined)):
        a, b = sa[i], sa[i-1]
        if (a < sep_index) != (b < sep_index):
            start_in_original = a if a < sep_index else b
            candidate = text[start_in_original:start_in_original + lcp[i-1]]
            if candidate == candidate[::-1] and len(candidate) > max_len:
                max_len = len(candidate)
                max_pos = start_in_original
    return text[max_pos:max_pos + max_len]



# =======================
# TESTY JEDNOSTKOWE
# =======================

import unittest

class TestSuffixStructures(unittest.TestCase):

    def test_longest_common_substring(self):
        self.assertEqual(longest_common_substring("abcdef", "zabcxy"), "abc")
        self.assertEqual(longest_common_substring("12345", "54321"), "1")
        self.assertEqual(longest_common_substring("xyz", "abc"), "")
        self.assertEqual(longest_common_substring("aaa", "aa"), "aa")
        self.assertEqual(longest_common_substring("", "abc"), "")

    def test_longest_common_substring_multiple(self):
        self.assertEqual(longest_common_substring_multiple(["abcdef", "bcdefg", "cdefgh"]), "cdef")
        self.assertEqual(longest_common_substring_multiple(["aaa", "aa", "a"]), "a")
        self.assertEqual(longest_common_substring_multiple(["apple", "banana", "orange"]), "a")
        self.assertEqual(longest_common_substring_multiple(["abcabc", "abc", "zabcx"]), "abc")

    def test_longest_palindromic_substring(self):
        self.assertIn(longest_palindromic_substring("babad"), ["bab", "aba"])  # oba poprawne
        self.assertEqual(longest_palindromic_substring("cbbd"), "bb")
        self.assertEqual(longest_palindromic_substring("a"), "a")
        self.assertEqual(longest_palindromic_substring(""), "")
        self.assertEqual(longest_palindromic_substring("abcdeedcba"), "abcdeedcba")


if __name__ == "__main__":
    unittest.main()

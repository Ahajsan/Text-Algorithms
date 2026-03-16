import hashlib
from typing import List, Tuple


class NilsimsHash:
    """Klasa implementująca algorytm Nilsimsa."""

    def __init__(self):
        """Inicjalizuje hash Nilsimsa."""
        self.hash_size = 256

    def _rolling_hash(self, text: str) -> list[int]:
        """
        Oblicza rolling hash dla tekstu.

        Args:
            text: Tekst do przetworzenia

        Returns:
            Lista wartości rolling hash, dopasowana długością do długości tekstu
        """
        trigrams = self._trigrams(text)
        hashes = [
            int(hashlib.md5(trigram.encode('utf-8')).hexdigest(), 16)
            for trigram in trigrams
        ]

        if not hashes:
            return []

        result = []
        for i in range(len(text)):
            result.append(hashes[i % len(hashes)])
        return result

    def _trigrams(self, text: str) -> list[str]:
        """
        Generuje trigramy z tekstu.

        Args:
            text: Tekst do przetworzenia

        Returns:
            Lista trigramów
        """
        text = text.lower()
        return [text[i:i + 3] for i in range(len(text) - 2)]

    def compute_hash(self, text: str) -> bytes:
        """
        Oblicza hash Nilsimsa dla tekstu.

        Args:
            text: Tekst do zahashowania

        Returns:
            256-bitowy hash jako bytes
        """
        vector = [0] * self.hash_size
        rolling_hashes = self._rolling_hash(text)

        for h in rolling_hashes:
            for i in range(self.hash_size):
                bit = (h >> i) & 1
                vector[i] += 1 if bit else -1

        final_bits = 0
        for i in range(self.hash_size):
            if vector[i] > 0:
                final_bits |= (1 << i)

        return final_bits.to_bytes(self.hash_size // 8, byteorder='big')

    def compare_hashes(self, hash1: bytes, hash2: bytes) -> float:
        """
        Porównuje dwa hashe Nilsimsa i zwraca stopień podobieństwa.

        Args:
            hash1: Pierwszy hash
            hash2: Drugi hash

        Returns:
            Stopień podobieństwa w zakresie [0, 1]
        """
        xor = int.from_bytes(hash1, 'big') ^ int.from_bytes(hash2, 'big')
        differing_bits = bin(xor).count('1')
        return 1 - (differing_bits / self.hash_size)


def nilsims_similarity(text1: str, text2: str) -> float:
    """
    Oblicza podobieństwo między dwoma tekstami używając algorytmu Nilsimsa.

    Args:
        text1: Pierwszy tekst
        text2: Drugi tekst

    Returns:
        Stopień podobieństwa w zakresie [0, 1]
    """
    hasher = NilsimsHash()
    hash1 = hasher.compute_hash(text1)
    hash2 = hasher.compute_hash(text2)
    return hasher.compare_hashes(hash1, hash2)


def find_similar_texts(target: str, candidates: list[str], threshold: float = 0.7) -> list[tuple[int, float]]:
    """
    Znajduje teksty podobne do tekstu docelowego.

    Args:
        target: Tekst docelowy
        candidates: Lista kandydatów
        threshold: Próg podobieństwa

    Returns:
        Lista krotek (indeks, podobieństwo) dla tekstów powyżej progu
    """
    hasher = NilsimsHash()
    target_hash = hasher.compute_hash(target)
    result = []

    for i, candidate in enumerate(candidates):
        candidate_hash = hasher.compute_hash(candidate)
        similarity = hasher.compare_hashes(target_hash, candidate_hash)
        if similarity >= threshold:
            result.append((i, similarity))

    return result

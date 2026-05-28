"""Tests for embedding functions."""

import pytest

from script.embeddings import (
    compute_centroid,
    cosine_similarity,
    deserialize_embedding,
    find_nearest_above_threshold,
    find_similar,
    find_similar_pairs,
    normalize_vector,
    serialize_embedding,
)


class TestCosineSimilarity:
    """Tests for cosine_similarity."""

    def test_identical_vectors(self):
        v = [1.0, 2.0, 3.0]
        assert cosine_similarity(v, v) == pytest.approx(1.0)

    def test_opposite_vectors(self):
        v1 = [1.0, 0.0]
        v2 = [-1.0, 0.0]
        assert cosine_similarity(v1, v2) == pytest.approx(-1.0)

    def test_orthogonal_vectors(self):
        v1 = [1.0, 0.0]
        v2 = [0.0, 1.0]
        assert cosine_similarity(v1, v2) == pytest.approx(0.0)

    def test_similar_vectors(self):
        v1 = [1.0, 1.0]
        v2 = [1.0, 0.9]
        sim = cosine_similarity(v1, v2)
        assert 0.9 < sim < 1.0

    def test_length_mismatch_raises(self):
        with pytest.raises(ValueError, match="length mismatch"):
            cosine_similarity([1, 2], [1, 2, 3])

    def test_empty_vectors_raises(self):
        with pytest.raises(ValueError, match="Empty"):
            cosine_similarity([], [])

    def test_zero_vector_returns_zero(self):
        v1 = [0.0, 0.0]
        v2 = [1.0, 2.0]
        assert cosine_similarity(v1, v2) == 0.0


class TestComputeCentroid:
    """Tests for compute_centroid."""

    def test_single_vector(self):
        v = [1.0, 2.0, 3.0]
        centroid = compute_centroid([v])
        assert centroid == pytest.approx(v)

    def test_two_vectors(self):
        v1 = [0.0, 0.0]
        v2 = [2.0, 4.0]
        centroid = compute_centroid([v1, v2])
        assert centroid == pytest.approx([1.0, 2.0])

    def test_multiple_vectors(self):
        vectors = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
        centroid = compute_centroid(vectors)
        expected = [2/3, 2/3]
        assert centroid == pytest.approx(expected)

    def test_empty_list_raises(self):
        with pytest.raises(ValueError, match="Empty"):
            compute_centroid([])

    def test_dimension_mismatch_raises(self):
        with pytest.raises(ValueError, match="same dimension"):
            compute_centroid([[1, 2], [1, 2, 3]])


class TestNormalizeVector:
    """Tests for normalize_vector."""

    def test_unit_vector_unchanged(self):
        v = [1.0, 0.0, 0.0]
        result = normalize_vector(v)
        assert result == pytest.approx(v)

    def test_normalizes_to_unit_length(self):
        v = [3.0, 4.0]
        result = normalize_vector(v)
        assert result == pytest.approx([0.6, 0.8])

    def test_zero_vector_returns_zero(self):
        v = [0.0, 0.0, 0.0]
        result = normalize_vector(v)
        assert result == [0.0, 0.0, 0.0]


class TestFindSimilar:
    """Tests for find_similar."""

    def test_finds_similar_above_threshold(self):
        query = [1.0, 0.0]
        candidates = [
            ("a", [1.0, 0.1]),   # Similar
            ("b", [0.0, 1.0]),   # Orthogonal
            ("c", [0.9, 0.1]),   # Similar
        ]
        results = find_similar(query, candidates, threshold=0.8)
        ids = [r[0] for r in results]
        assert "a" in ids
        assert "c" in ids
        assert "b" not in ids

    def test_returns_sorted_by_similarity(self):
        query = [1.0, 0.0]
        candidates = [
            ("a", [0.9, 0.1]),
            ("b", [1.0, 0.0]),
        ]
        results = find_similar(query, candidates, threshold=0.5)
        assert results[0][0] == "b"  # Most similar first
        assert results[1][0] == "a"

    def test_top_k_limits_results(self):
        query = [1.0, 0.0]
        candidates = [
            ("a", [1.0, 0.0]),
            ("b", [0.99, 0.1]),
            ("c", [0.98, 0.2]),
        ]
        results = find_similar(query, candidates, threshold=0.5, top_k=2)
        assert len(results) == 2

    def test_empty_candidates_returns_empty(self):
        results = find_similar([1.0, 0.0], [], threshold=0.5)
        assert results == []


class TestFindSimilarPairs:
    """Tests for find_similar_pairs."""

    def test_finds_pairs_above_threshold(self):
        group_a = [("a1", [1.0, 0.0]), ("a2", [0.0, 1.0])]
        group_b = [("b1", [1.0, 0.1]), ("b2", [0.0, 0.9])]

        pairs = find_similar_pairs(group_a, group_b, threshold=0.9)

        # a1-b1 and a2-b2 should be similar
        pair_ids = [(p[0], p[1]) for p in pairs]
        assert ("a1", "b1") in pair_ids
        assert ("a2", "b2") in pair_ids

    def test_returns_sorted_by_similarity(self):
        group_a = [("a1", [1.0, 0.0])]
        group_b = [("b1", [0.9, 0.1]), ("b2", [1.0, 0.0])]

        pairs = find_similar_pairs(group_a, group_b, threshold=0.5)

        # b2 is more similar to a1
        assert pairs[0][1] == "b2"

    def test_empty_groups_return_empty(self):
        assert find_similar_pairs([], [("b", [1, 0])], 0.5) == []
        assert find_similar_pairs([("a", [1, 0])], [], 0.5) == []


class TestFindNearestAboveThreshold:
    """Tests for find_nearest_above_threshold."""

    def test_finds_nearest(self):
        query = [1.0, 0.0]
        candidates = [
            ("a", [0.9, 0.1]),
            ("b", [1.0, 0.0]),  # Most similar
            ("c", [0.8, 0.2]),
        ]
        result = find_nearest_above_threshold(query, candidates, threshold=0.8)
        assert result is not None
        assert result[0] == "b"
        assert result[1] == pytest.approx(1.0)

    def test_returns_none_below_threshold(self):
        query = [1.0, 0.0]
        candidates = [("a", [0.0, 1.0])]  # Orthogonal
        result = find_nearest_above_threshold(query, candidates, threshold=0.9)
        assert result is None

    def test_empty_candidates_returns_none(self):
        result = find_nearest_above_threshold([1.0, 0.0], [], threshold=0.5)
        assert result is None


class TestSerializeDeserialize:
    """Tests for serialize/deserialize embedding."""

    def test_roundtrip(self):
        original = [1.5, -2.3, 0.0, 999.999]
        serialized = serialize_embedding(original)
        deserialized = deserialize_embedding(serialized)
        assert deserialized == pytest.approx(original, rel=1e-5)

    def test_empty_vector(self):
        original = []
        serialized = serialize_embedding(original)
        deserialized = deserialize_embedding(serialized)
        assert deserialized == []

    def test_single_element(self):
        original = [42.0]
        serialized = serialize_embedding(original)
        deserialized = deserialize_embedding(serialized)
        assert deserialized == pytest.approx(original)

    def test_large_vector(self):
        original = [float(i) for i in range(1536)]  # OpenAI embedding dimension
        serialized = serialize_embedding(original)
        deserialized = deserialize_embedding(serialized)
        assert deserialized == pytest.approx(original)

from system_design_labs.bloom_filter import BloomFilter


def test_inserted_values_are_never_false_negatives():
    bloom = BloomFilter(size_bits=128, hash_count=3)

    bloom.add("alice")
    bloom.add("bob")

    assert "alice" in bloom
    assert "bob" in bloom


def test_false_positive_rate_improves_with_more_bits():
    small = BloomFilter(size_bits=64, hash_count=3)
    large = BloomFilter(size_bits=512, hash_count=3)

    assert large.estimated_false_positive_rate(20) < small.estimated_false_positive_rate(20)

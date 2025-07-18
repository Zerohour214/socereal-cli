from src.modules.validations.entropy_validation import compute_stats, detect_outlier_indices

def test_corpus_outlier():
    corpus = [
        "ABCD-1234-5678",   # 0 Normal
        "EFGH-4321-8765",   # 1 Normal
        "SN: 9876/5432",    # 2 Normal-ish
        "序列号: 1234-5678", # 3 Outlier (CJK)
        "☺️A___Z",          # 4 Outlier (emoji)
        "ABCD-1234-5678",   # 5 Normal (duplicate)
    ]
    stats = compute_stats(corpus)
    outliers = detect_outlier_indices(stats, threshold=1.5)
    print("Outlier indices:", outliers)
    print("Outlier texts:", [corpus[i] for i in outliers])

    outlier_texts = [corpus[i] for i in outliers]
    normal_texts = [corpus[i] for i in range(len(corpus)) if i not in outliers]

    # Outliers should include at least one "abnormal" pattern
    assert any("序列号" in text or "☺️" in text for text in outlier_texts)

    # Normals should NOT all be flagged
    assert any("ABCD" in text or "EFGH" in text or "SN" in text for text in normal_texts)

    # There should be at least one outlier, and not all entries should be outliers
    assert 1 <= len(outliers) < len(corpus)

import pytest
from scripts.populate_facilities_table import check_womens_section, nlp


def test_detects_positive_womens_section():
    """Core functionality: explicit positive mentions return True."""
    review = "Clean wudu area and a dedicated sisters entrance upstairs."
    assert check_womens_section(review, nlp) is True


@pytest.mark.parametrize(
    "keyword_review",
    [
        "Spacious women's section on the second floor.",
        "There is a separate ladies prayer hall.",
        "Great female prayer area available.",
    ],
)
def test_detects_various_womens_section_terms(keyword_review):
    """Core functionality: verifies all regex keyword variations match properly."""
    assert check_womens_section(keyword_review, nlp) is True


@pytest.mark.parametrize(
    "negated_review",
    [
        "Nice masjid, though there is no women's section here.",
        "They do not have a sisters area.",
        "This location doesn't have a ladies section.",
    ],
)
def test_negated_mentions_return_false(negated_review):
    """Edge case: negation words in the same sentence prevent false positives."""
    assert check_womens_section(negated_review, nlp) is False


def test_multi_sentence_negation_does_not_overwrite_positive():
    """Boundary condition: negation in a separate sentence should not cancel a positive mention."""
    review = "There is no parking lot. However, there is a clean sisters section upstairs."
    assert check_womens_section(review, nlp) is True


def test_neutral_review_returns_false():
    """Boundary condition: reviews without facility keywords return False."""
    review = "Great Friday khutbah and welcoming community."
    assert check_womens_section(review, nlp) is False


def test_empty_string_returns_false():
    """Error/edge scenario: empty review text returns False without raising an error."""
    assert check_womens_section("", nlp) is False
import pytest

from streak import longest_positive_streak


def test_empty():
    assert longest_positive_streak([]) == 0


def test_all_positive():
    assert longest_positive_streak([1, 1, 1]) == 3


def test_multiple_streaks():
    data = [2, 3, -1, 5, 6, 7, 0, 4]
    # streaks: [2,3] -> 2 ; [5,6,7] -> 3 ; [4] -> 1
    assert longest_positive_streak(data) == 3


def test_zeros_and_negatives():
    assert longest_positive_streak([0, -1, 2, 3, 0, -5, 1, 2]) == 2

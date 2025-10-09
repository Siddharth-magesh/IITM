# tests/test_streak.py

import pytest
from streak import longest_positive_streak

def test_empty_list():
    assert longest_positive_streak([]) == 0

def test_single_streak():
    assert longest_positive_streak([1, 2, 3]) == 3

def test_multiple_streaks():
    assert longest_positive_streak([2, 3, -1, 5, 6, 7, 0, 4]) == 3

def test_zeros_and_negatives():
    assert longest_positive_streak([0, -1, 2, 3, -5, 4, 1]) == 2

def test_all_non_positive():
    assert longest_positive_streak([0, -1, -2]) == 0

def test_mixed_longest_at_end():
    assert longest_positive_streak([-1, 0, 1, 2, 3]) == 3

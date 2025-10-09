import pytest
from streak import longest_positive_streak

def test_empty_list():
    """Test that an empty list returns a streak of 0."""
    assert longest_positive_streak([]) == 0

def test_no_positive_numbers():
    """Test that a list with no positive numbers returns a streak of 0."""
    assert longest_positive_streak([-1, -2, 0, -5]) == 0

def test_all_positive_numbers():
    """Test a list where all numbers are positive."""
    assert longest_positive_streak([1, 2, 3, 4, 5]) == 5

def test_single_streak_at_beginning():
    """Test a single streak at the beginning of the list."""
    assert longest_positive_streak([1, 2, 3, 0, -1, -2]) == 3

def test_single_streak_at_end():
    """Test a single streak at the end of the list."""
    assert longest_positive_streak([-1, 0, 1, 2, 3, 4]) == 4

def test_single_streak_in_middle():
    """Test a single streak in the middle of the list."""
    assert longest_positive_streak([-1, 0, 1, 2, 0, -5]) == 2

def test_multiple_streaks_longest_first():
    """Test multiple streaks where the longest streak is first."""
    assert longest_positive_streak([1, 2, 3, 0, 1, 2, 0, 1]) == 3

def test_multiple_streaks_longest_last():
    """Test multiple streaks where the longest streak is last."""
    assert longest_positive_streak([1, 0, 1, 2, 0, 1, 2, 3, 4]) == 4

def test_multiple_streaks_longest_in_middle():
    """Test multiple streaks where the longest streak is in the middle."""
    assert longest_positive_streak([1, 0, 1, 2, 3, 4, 0, 1, 2]) == 4

def test_list_with_zeros():
    """Test that zeros correctly break a streak."""
    assert longest_positive_streak([1, 2, 0, 3, 4, 5]) == 3

def test_list_with_negatives():
    """Test that negative numbers correctly break a streak."""
    assert longest_positive_streak([1, 2, -5, 3, 4, 5, 6]) == 4

def test_single_number_list():
    """Test a list with a single positive number."""
    assert longest_positive_streak([5]) == 1

def test_single_negative_number_list():
    """Test a list with a single negative number."""
    assert longest_positive_streak([-5]) == 0
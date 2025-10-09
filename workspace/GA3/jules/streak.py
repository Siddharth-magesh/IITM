from typing import List


def longest_positive_streak(nums: List[int]) -> int:
    """Return the length of the longest run of consecutive values strictly > 0.

    Deterministic and pure: no prints, no randomness, no global state.
    """
    if not nums:
        return 0

    max_streak = 0
    cur = 0
    for v in nums:
        if v > 0:
            cur += 1
            if cur > max_streak:
                max_streak = cur
        else:
            cur = 0

    return max_streak

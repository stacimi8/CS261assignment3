# Course: CS261 - Data Structures
# Assignment: Programming Assignment 3: Implementation of Linked Lists, ADTs using
#             Linked Lists and Binary Search
# Description: Implementation of two binary search methods.

import random
import time
from static_array import *


# ------------------- PROBLEM 1 - -------------------------------------------


def binary_search(arr: StaticArray, target: int) -> int:
    """
    A function that receives a StaticArray and an integer target and returns the index
    of the target element if it is present in the array or returns -1 if it is not. The
    original array should not be modified. You may assume that the input array will contain
    at least one element and that all elements will be integers in the range [-109, 109].
    It is guaranteed that all elements in the input array will be distinct and that the
    input array will be sorted in either ascending or descending order. Your binary search
    implementation must have O(logN) runtime complexity.
    """

    # help from CS162 - assignment 3 binary_search.py
    first = 0
    last = arr.size() - 1

    # input array is stored in ascending order
    if arr.get(first) <= arr.get(last):
        while first <= last:
            middle = (first + last) // 2
            if arr.get(middle) == target:    # target value found
                return middle    # returns index of found target value
            if arr.get(middle) > target:
                last = middle - 1
            else:
                first = middle + 1
        return -1

    # input array is sorted in descending order
    if arr.get(first) > arr.get(last):
        while first <= last:
            middle = (first + last) // 2
            if arr.get(middle) == target:    # target value found
                return middle    # returns index of found target value
            if arr.get(middle) > target:
                first = middle + 1
            else:
                last = middle - 1
        return -1

# ------------------- PROBLEM 2 - -------------------------------------------


def binary_search_rotated(arr: StaticArray, target: int) -> int:
    """
    A function that receives a StaticArray and an integer target and returns the index
    of the target element if it is present in the array or returns -1 if it is not. The
    original array should not be modified. You may assume that the input array will contain
    at least one element and that all elements will be integers in the range [-109, 109].
    It is guaranteed that all elements in the input array will be distinct. The input array
    will be sorted in the ascending order. But, before being passed to your function, the input
    array will be rotated an unknown number of steps (either right or left). Your binary
    search implementation must have O(logN) runtime complexity.
    """

    # help from CS162 - assignment 3 binary_search.py

    length = arr.size()

    # base case: size of array is 1
    if length == 1:
        if arr.get(0) == target:
            return 0

    first = 0
    last = length - 1

    while first < last:

        middle = (first + last) // 2

        if arr.get(middle) == target:    # target value found
            return middle    # returns index of found target value

        if arr.get(first) < arr.get(middle):
            # sorted in ascending order
            if arr.get(first) <= target < arr.get(middle):
                last = middle
            else:
                first = middle + 1
        else:
            # sorted in ascending order
            if arr.get(middle) < target <= arr.get(last):
                first = middle + 1
            else:
                last = middle

    # check last value (since the while loop breaks if first == last)
    if arr.get(length-1) == target:
        return (length - 1)

    return - 1

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":
    pass

    # print('\n# problem 1 example 1')
    # src = (-10, -5, 0, 5, 7, 9, 11)
    # targets = (7, -10, 11, 0, 8, 1, -100, 100)
    # arr = StaticArray(len(src))
    # for i, value in enumerate(src):
    #     arr[i] = value
    # print([binary_search(arr, target) for target in targets])
    # arr._data.reverse()
    # print([binary_search(arr, target) for target in targets])
    #
    # print('\n# problem 1 example 2')
    """
    src = [random.randint(-10 ** 7, 10 ** 7) for _ in range(5_000_000)]
    src = sorted(set(src))
    arr = StaticArray(len(src))
    arr._data = src[:]

    # add 20 valid and 20 (likely) invalid targets
    targets = [-10 ** 8, 10 ** 8]
    targets += [arr[random.randint(0, len(src) - 1)] for _ in range(20)]
    targets += [random.randint(-10 ** 7, 10 ** 7) for _ in range(18)]

    result, total_time = True, 0
    for target in targets:
        total_time -= time.time()
        answer = binary_search(arr, target)
        total_time += time.time()
        result &= arr[answer] == target if target in src else answer == -1
    print(result, total_time < 0.5)

    arr._data.reverse()
    for target in targets:
        total_time -= time.time()
        answer = binary_search(arr, target)
        total_time += time.time()
        result &= arr[answer] == target if target in src else answer == -1
    print(result, total_time < 0.5)
    """


    print('\n# problem 2 example 1')
    test_cases = (
        ((935981732, 567475463), 567475463),
        ((6, 8, 12, 20, 0, 2, 5), -1),
        ((1,), 1),
        ((1,), 0),
    )
    result = []
    for src, target in test_cases:
        arr = StaticArray(len(src))
        for i, value in enumerate(src):
            arr[i] = value
        result.append((binary_search_rotated(arr, target)))
    print(*result)


    # print('\n# problem 2 example 2')
    #
    # src = [random.randint(-10 ** 7, 10 ** 7) for _ in range(5_000_000)]
    # src = sorted(set(src))
    # arr = StaticArray(len(src))
    # arr._data = src[:]
    #
    # # add 20 valid and 20 (likely) invalid targets
    # targets = [-10 ** 8, 10 ** 8]
    # targets += [arr[random.randint(0, len(src) - 1)] for _ in range(20)]
    # targets += [random.randint(-10 ** 7, 10 ** 7) for _ in range(18)]
    #
    # result, total_time = True, 0
    # for target in targets:
    #     # rotate arr random number of steps
    #     pivot = random.randint(0, len(src) - 1)
    #     arr._data = src[pivot:] + src[:pivot]
    #
    #     total_time -= time.time()
    #     answer = binary_search_rotated(arr, target)
    #     total_time += time.time()
    #     result &= arr[answer] == target if target in src else answer == -1
    # print(result, total_time < 0.5)

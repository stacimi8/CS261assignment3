# Course: CS261 - Data Structures
# Assignment: Programming Assignment 3: Implementation of Linked Lists, ADTs using
#             Linked Lists and Binary Search
# Description: Implementation of Deque and Bag ADT interfaces with a circular
#              doubly linked list data structure.


class CDLLException(Exception):
    """
    Custom exception class to be used by Circular Doubly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DLNode:
    """
    Doubly Linked List Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        self.next = None
        self.prev = None
        self.value = value


class CircularList:
    def __init__(self, start_list=None):
        """
        Initializes a new linked list with sentinel
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.sentinel = DLNode(None)
        self.sentinel.next = self.sentinel
        self.sentinel.prev = self.sentinel

        # populate CDLL with initial values (if provided)
        # before using this feature, implement add_back() method
        if start_list is not None:
            for value in start_list:
                self.add_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'CDLL ['
        if self.sentinel.next != self.sentinel:
            cur = self.sentinel.next.next
            out = out + str(self.sentinel.next.value)
            while cur != self.sentinel:
                out = out + ' <-> ' + str(cur.value)
                cur = cur.next
        out = out + ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list

        This can also be used as troubleshooting method. This method works
        by independently measuring length during forward and backward
        traverse of the list and return the length if results agree or error
        code of -1 or -2 if thr measurements are different.

        Return values:
        >= 0 - length of the list
        -1 - list likely has an infinite loop (forward or backward)
        -2 - list has some other kind of problem

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """

        # length of the list measured traversing forward
        count_forward = 0
        cur = self.sentinel.next
        while cur != self.sentinel and count_forward < 101_000:
            count_forward += 1
            cur = cur.next
        # length of the list measured traversing backwards
        count_backward = 0
        cur = self.sentinel.prev
        while cur != self.sentinel and count_backward < 101_000:
            count_backward += 1
            cur = cur.prev
        # if any of the result is > 100,000 -> list has a loop
        if count_forward > 100_000 or count_backward > 100_000:
            return -1

        # if counters have different values -> there is some other problem
        return count_forward if count_forward == count_backward else -2

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.sentinel.next == self.sentinel

    # ------------------------------------------------------------------ #

    def add_front(self, value: object) -> None:
        """
        A function that adds a new node at the beginning of the list (right after
        the sentinel).
        """
        new_node = DLNode(value)

        # link new node's next node to sentinel's next node
        new_node.next = self.sentinel.next

        # link new node's previous node to sentinel
        new_node.prev = self.sentinel

        # link new_node next's previous node to new node
        new_node.next.prev = new_node

        # link sentinel's next node to new node
        self.sentinel.next = new_node

    def add_back(self, value: object) -> None:
        """
        A function that adds a new node at the end of the list (right before the
        sentinel).
        """

        new_node = DLNode(value)

        # link new node's next node to sentinel
        new_node.next = self.sentinel

        # link new node's previous node to sentinel.prev
        new_node.prev = self.sentinel.prev

        # link new node previous' next node to new node
        new_node.prev.next = new_node

        # link sentinel's previous node to new node
        self.sentinel.prev = new_node

    def insert_at_index(self, index: int, value: object) -> None:
        """
        A function that adds a new value at the specified index position in the
        linked list. Index 0 refers to the beginning of the list (right after the
        sentinel). If the provided index is invalid, the method raises a custom
        “CDLLException”. If the linked list contains N nodes (not including sentinel
        node in this count), valid indices for this method are [0, N] inclusive.
        """

        # invalid index
        if 0 > index or index > self.length():
            raise CDLLException

        new_node = DLNode(value)
        midway = self.length()//2

        if index <= midway:
            curr = self.sentinel.next
            for pos in range(0, midway+1):
                # index is found at pos
                if pos == index:
                    # new node is linked to its next and prev nodes
                    new_node.next = curr
                    new_node.prev = curr.prev

                    # link curr previous' node to new node
                    curr.prev = new_node

                    # link new node previous' next node to new node
                    new_node.prev.next = new_node
                    return
                curr = curr.next

        if index > midway:
            curr = self.sentinel
            for pos in range(self.length(), midway, - 1):
                # index is found at pos
                if pos == index:

                    # new node is linked to its next and prev nodes.
                    new_node.next = curr
                    new_node.prev = curr.prev

                    # link new node previous' next node to new node
                    new_node.prev.next = new_node

                    # link current's prev node to new node
                    curr.prev = new_node
                    return
                curr = curr.prev

    def remove_front(self) -> None:
        """
        A function that removes the first node from the list. If the list is empty,
        the method raises a custom “CDLLException”.
        """

        if self.is_empty():
            raise CDLLException

        self.sentinel.next = self.sentinel.next.next
        self.sentinel.next.prev = self.sentinel

    def remove_back(self) -> None:
        """
        A function that removes the last node from the list. If the list is empty,
        the method raises a custom “CDLLException”.
        """

        if self.is_empty():
            raise CDLLException

        self.sentinel.prev = self.sentinel.prev.prev
        self.sentinel.prev.next = self.sentinel

    def remove_at_index(self, index: int) -> None:
        """
        A function that removes a node from the list given its index. Index 0
        refers to the beginning of the list (right after the sentinel). If the
        provided index is invalid, the method raises a custom “CDLLException”.
        If the list contains N elements (not including sentinel node in this count),
        valid indices for this method are [0, N - 1] inclusive.
        """

        # invalid index
        if 0 > index or index > self.length() - 1:
            raise CDLLException

        midway = self.length()//2

        if index <= midway:
            curr = self.sentinel.next
            for pos in range(0, midway + 1):
                # index is found at pos
                if pos == index:
                    curr.next.prev = curr.prev
                    curr.prev.next = curr.next
                    return
                curr = curr.next

        if index > midway:
            curr = self.sentinel.prev
            for pos in range(self.length() - 1, midway, - 1):
                # index is found at pos
                if pos == index:
                    curr.next.prev = curr.prev
                    curr.prev.next = curr.next
                    return
                curr = curr.prev

    def get_front(self) -> object:
        """
        Returns the value from the first node in the list without removing it.
        If the list is empty, the method raises a custom “CDLLException”.
        """

        if self.is_empty():
            raise CDLLException

        return self.sentinel.next.value

    def get_back(self) -> object:
        """
        Returns the value from the last node in the list without removing it.
        If the list is empty, the method raises a custom “CDLLException”.
        """

        if self.is_empty():
            raise CDLLException

        return self.sentinel.prev.value

    def remove(self, value: object) -> bool:
        """
        A function that traverses the list from the beginning to the end and
        removes the first node in the list that matches the provided “value”
        object. The method returns True if some node was actually removed from
        the list. Otherwise, it returns False.
        """

        curr = self.sentinel.next

        # traversing through list from beginning to end
        for pos in range(0, self.length()):

            # value is found
            if curr.value == value:

                # remove first node that matches the value
                self.remove_at_index(pos)
                return True

            curr = curr.next

        return False

    def count(self, value: object) -> int:
        """
        A function that counts and returns the number of elements in the list
        that matches the provided "value" object.
        """

        curr = self.sentinel.next
        count = 0

        for pos in range(0, self.length()):
            # value is found, add 1 to count
            if curr.value == value:
                count += 1
            curr = curr.next

        return count

    def swap_pairs(self, index1: int, index2: int) -> None:
        """
        A function that swaps two nodes given their indices. All work must be done
        “in place” without creating any new nodes. You are not allowed to change the
        values of the nodes; the solution must change node pointers. Your solution
        must have O(N) runtime complexity for finding the pointers to the nodes and
        O(1) for actually swapping them. If either of the provided indices is invalid,
        the method raises a custom “CDLLException”. If the linked list contains N
        nodes (not including sentinel nodes in this count), valid indices for this
        method are [0, N - 1] inclusive.
        """

        # invalid index
        if 0 > index1 or 0 > index2 or \
                index1 > self.length() - 1 or index2 > self.length() - 1:
            raise CDLLException

        if index1 <= index2:
            length = index2 + 1
        else:
            length = index1 + 1

        curr = self.sentinel.next
        for index in range(0, length):

            if index == index1:
                index1_node = curr
                index1_next = curr.next
                index1_prev = curr.prev

            if index == index2:
                index2_node = curr
                index2_next = curr.next
                index2_prev = curr.prev

            curr = curr.next

        # change pointers - if indices are next to each other
        if index2 - index1 == 1:  # index2 is after index1

            # swapping two provided indices and linking them to each other
            index1_next.next = index2_prev
            index2_prev.prev = index1_next

            # linking index2 to index1 prev and linking index1 prev back to index2
            index1_next.prev = index1_prev
            index1_prev.next = index1_next

            # linking index1 to index2 next and linking index2 next back to index1
            index2_prev.next = index2_next
            index2_next.prev = index2_prev

        elif index1 - index2 == 1:  # index1 is after index2

            # swapping two provided indices and linking them to each other
            index2_next.next = index1_prev
            index1_prev.prev = index2_next

            # linking index1 to index2 prev and linking index2 prev back to index1
            index2_next.prev = index2_prev
            index2_prev.next = index2_next

            # linking index2 to index1 next and linking index1 next back to index2
            index1_prev.next = index1_next
            index1_next.prev = index1_prev

        # change pointers - if indices are not next to each other
        elif abs(index2 - index1) != 1:
            # updating index1 next and prev pointers
            index1_node.next = index2_next
            index1_node.prev = index2_prev

            # updating index1 next previous and index1 previous next pointers
            index1_next.prev = index2_node
            index1_prev.next = index2_node

            # updating index2 next and prev pointers
            index2_node.next = index1_next
            index2_node.prev = index1_prev

            # updating index2 next previous and index2 previous next pointers
            index2_next.prev = index1_node
            index2_prev.next = index1_node

    def reverse(self) -> None:
        """
        A function that reverses the order of the nodes in the list. All work
        must be done “in place” without creating any new nodes. You are not
        allowed to change the values of the nodes; the solution must change node
        pointers. Your solution must have O(N) runtime complexity.
        """

        # start with self.sentinel as curr
        curr = self.sentinel

        # iterate through the list swapping next and previous pointer for each node
        for node in range(-1, self.length()):

            # variable to hold curr.next node
            original_next = curr.next

            # swapping curr next with curr prev to reverse list
            curr.next = curr.prev
            curr.prev = original_next

            curr = curr.next

    def sort(self) -> None:
        """
        A function that sorts the content of the list in non-descending order. All
        work must be done “in place” without creating any new nodes. You are not
        allowed to change the values of the nodes; the solution must change node
        pointers. You can implement any sort method of your choice. Sorting does not
        have to be very efficient or fast; a simple insertion or bubble sort will
        suffice. However, runtime complexity of your implementation cannot be worse
        than O(N^2). Duplicates in the list can be placed in any relative order in
        the sorted list (in other words, your sort does not have to be ‘stable’).
        For this method, you may assume that elements stored in the linked list are all
        of the same type (either all numbers, or strings, or custom objects, but never
        a mix of these).
        """

        swapped = True

        while swapped:
            curr = self.sentinel.next
            swapped = False

            while curr != self.sentinel:
                next_node = curr.next
                if next_node is not self.sentinel and curr.value > next_node.value:

                    # linking left outer node to next_node and right outer node to next_node next
                    curr.prev.next = next_node
                    curr.next = next_node.next

                    # linking next_node to left outer node and right outer node to curr
                    next_node.prev = curr.prev
                    curr.next.prev = curr

                    # linking curr and next_node to each other
                    curr.prev = next_node
                    next_node.next = curr

                    swapped = True
                else:
                    curr = curr.next


    def rotate(self, steps: int) -> None:
        """
        A function that‘rotates’ the linked list by shifting the position of its elements
        right or left steps number of times. If steps is a positive integer, elements should
        be rotated right. Otherwise, the elements should be rotated left. All work must be
        done “in place” without creating any new nodes. You are not allowed to change the
        values of the nodes; the solution must change node pointers. Please note that the
        value of the steps parameter can be very large (from -109 to 109). The solution’s
        runtime complexity must be O(N), where N is the length of the list.
        """

        if steps == 0:
            return

        if self.length() == 0 or self.length() == 1:
            return

        count = abs(steps) % self.length()

        # the number of steps required does not actually change the node placements
        if count == 0:
            return

        if steps < 0:
            curr = self.sentinel
            sentinel_next = self.sentinel.next
            sentinel_prev = self.sentinel.prev
            for index in range(0, self.length()):
                if index == count:

                    # linking sentinel to its new previous and next
                    self.sentinel.prev = curr
                    # accounting for if curr next node was originally self.sentinel
                    if curr.next == self.sentinel:
                        self.sentinel.next = curr.next.next
                    else:
                        self.sentinel.next = curr.next

                    # linking new sentinel next and new sentinel prev to sentinel
                    self.sentinel.next.prev = self.sentinel
                    curr.next = self.sentinel

                    # closing the gap from where sentinel originally moved from
                    sentinel_next.prev = sentinel_prev
                    sentinel_prev.next = sentinel_next
                    break
                curr = curr.next

        if steps > 0:
            curr = self.sentinel
            sentinel_next = self.sentinel.next
            sentinel_prev = self.sentinel.prev
            for index in range(0, self.length()):
                if index == count:

                    # linking sentinel to its new next and previous
                    self.sentinel.next = curr
                    # accounting for if curr prev node was originally self.sentinel
                    if curr.prev == self.sentinel:
                        self.sentinel.prev = curr.prev.prev
                    else:
                        self.sentinel.prev = curr.prev

                    # linking new sentinel previous and new sentinel next to sentinel
                    self.sentinel.prev.next = self.sentinel
                    curr.prev = self.sentinel

                    # closing the gap from where sentinel originally moved from
                    sentinel_next.prev = sentinel_prev
                    sentinel_prev.next = sentinel_next
                    break
                curr = curr.prev

    def remove_duplicates(self) -> None:
        """
        A function that deletes all nodes that have duplicate values from a sorted linked list,
        leaving only nodes with distinct values. All work must be done “in place” without creating
        any new nodes. You are not allowed to change the values of the nodes; the solution must
        change node pointers. Your solution must have O(N) runtime complexity. You may assume that
        the list is sorted.
        """

        curr = self.sentinel.next
        val = curr.prev.value

        while curr is not self.sentinel:

            # val doesn't equal current value, update val to next value to compare
            # duplicates for that value
            if val != curr.value:
                val = curr.value
                curr = curr.next

            # matching value found, use remove method to remove value
            if val == curr.value:
                self.remove(val)

                # curr next value is not a duplicate, remove comparison val
                # and update val to next value
                if val != curr.next.value:
                    self.remove(val)
                curr = curr.next

    def odd_even(self) -> None:
        """
        A function that regroups list nodes by first grouping all ODD nodes together followed
        by all EVEN nodes (here, “odd” and “even” refer to the node position in the list
        (starting from 1), not the node values). All work must be done “in place” without
        creating any new nodes. You are not allowed to change the values of the nodes; the
        solution must change node pointers. Your solution must have O(N) runtime complexity.
        """

        if self.length() <= 1:
            return

        # curr is even nodes
        curr = self.sentinel.next.next
        odd = curr.next
        count = (self.length()-1)//2
        first_even_node = curr

        while count != 0:

            # place holder for next even curr
            next_even = odd.next

            curr.prev.next = odd
            odd.prev = curr.prev

            self.sentinel.prev.next = curr
            curr.prev = self.sentinel.prev

            self.sentinel.prev = curr
            curr.next = self.sentinel

            curr = next_even
            odd = curr.next

            if odd is first_even_node:

                # linking last odd node and first even node to each other
                next_even.prev.next = odd
                odd.prev = next_even.prev

                # linking next_even (last even node) and prior even node to each other
                self.sentinel.prev.next = next_even
                next_even.prev = self.sentinel.prev

                # linking next_even (last even node) and self.sentinel to each other
                self.sentinel.prev = next_even
                next_even.next = self.sentinel

            count -= 1

    def add_integer(self, num: int) -> None:
        """Assume the content of the linked list represents a non-negative integer such that each
        digit is stored in a separate node. This method will receive another non-negative integer
        num, add it to the number already stored in the linked list, and then store the result of
        the addition back into the list nodes, one digit per node. This addition must be done “in place”,
        by changing the values of the existing nodes to the extent that is possible. However, since the
        result of the addition may have more digits than nodes in the original linked list, you may need
        to add some new nodes. However, you should only add the minimum number of nodes necessary and not
        recreate the entire linked list.
        """

        # invalid num input
        if num < 0:
            raise CDLLException

        # converts num into a string
        second_integer = str(num)
        curr = self.sentinel.prev

        # iterates through second integer in reverse
        for digit in second_integer[::-1]:

            if curr is not self.sentinel:

                sum = int(digit) + curr.value

                # sum is less than 10 - update the curr value to sum
                if sum < 10:
                    curr.value = sum
                    curr = curr.prev

                # sum is greater than 10
                else:

                    # create a new node to add 1
                    if curr.prev is self.sentinel:
                        curr.value = sum % 10
                        self.add_front(1)
                        curr = curr.prev

                    # add 1 to curr previous node
                    else:
                        curr.value = sum % 10
                        curr.prev.value += 1
                        curr = curr.prev

            # no nodes left in linked list to add digits to
            # create additional nodes if there are remaining digits to add
            else:
                remaining_digit = int(digit)
                self.add_front(remaining_digit)


if __name__ == '__main__':
    pass

    # print('\n# add_front example 1')
    # lst = CircularList()
    # print(lst)
    # lst.add_front('A')
    # lst.add_front('B')
    # lst.add_front('C')
    # print(lst)
    #
    # print('\n# add_back example 1')
    # lst = CircularList()
    # print(lst)
    # lst.add_back('C')
    # lst.add_back('B')
    # lst.add_back('A')
    # print(lst)
    #
    # print('\n# insert_at_index example 1')
    # lst = CircularList()
    # test_cases = [(0, 'A'), (0, 'B'), (1, 'C'), (3, 'D'), (-1, 'E'), (5, 'F')]
    # for index, value in test_cases:
    #     print('Insert of', value, 'at', index, ': ', end='')
    #     try:
    #         lst.insert_at_index(index, value)
    #         print(lst)
    #     except Exception as e:
    #         print(type(e))
    #
    # print('\n# remove_front example 1')
    # lst = CircularList([1, 2])
    # print(lst)
    # for i in range(3):
    #     try:
    #         lst.remove_front()
    #         print('Successful removal', lst)
    #     except Exception as e:
    #         print(type(e))
    #
    # print('\n# remove_back example 1')
    # lst = CircularList()
    # try:
    #     lst.remove_back()
    # except Exception as e:
    #     print(type(e))
    # lst.add_front('Z')
    # lst.remove_back()
    # print(lst)
    # lst.add_front('Y')
    # lst.add_back('Z')
    # lst.add_front('X')
    # print(lst)
    # lst.remove_back()
    # print(lst)
    #
    # print('\n# remove_at_index example 1')
    # lst = CircularList([1, 2, 3, 4, 5, 6])
    # print(lst)
    # for index in [0, 0, 0, 2, 2, -2]:
    #     print('Removed at index:', index, ': ', end='')
    #     try:
    #         lst.remove_at_index(index)
    #         print(lst)
    #     except Exception as e:
    #         print(type(e))
    # print(lst)
    #
    # print('\n# get_front example 1')
    # lst = CircularList(['A', 'B'])
    # print(lst.get_front())
    # print(lst.get_front())
    # lst.remove_front()
    # print(lst.get_front())
    # lst.remove_back()
    # try:
    #     print(lst.get_front())
    # except Exception as e:
    #     print(type(e))
    #
    # print('\n# get_back example 1')
    # lst = CircularList([1, 2, 3])
    # lst.add_back(4)
    # print(lst.get_back())
    # lst.remove_back()
    # print(lst)
    # print(lst.get_back())
    #
    # print('\n# remove example 1')
    # lst = CircularList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    # print(lst)
    # for value in [7, 3, 3, 3, 3]:
    #     print(lst.remove(value), lst.length(), lst)
    #
    # print('\n# count example 1')
    # lst = CircularList([1, 2, 3, 1, 2, 2])
    # print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))
    # #
    # print('\n# swap_pairs example 1')
    # lst = CircularList([0, 1, 2, 3, 4, 5, 6])
    # test_cases = ((0, 6), (0, 7), (-1, 6), (1, 5),
    #               (4, 2), (3, 3), (1, 2), (2, 1))
    #
    # for i, j in test_cases:
    #     print('Swap nodes ', i, j, ' ', end='')
    #     try:
    #         lst.swap_pairs(i, j)
    #         print(lst)
    #     except Exception as e:
    #         print(type(e))
    #
    # print('\n# reverse example 1')
    # test_cases = (
    #     [1, 2, 3, 3, 4, 5],
    #     [1, 2, 3, 4, 5],
    #     ['A', 'B', 'C', 'D']
    # )
    # for case in test_cases:
    #     lst = CircularList(case)
    #     lst.reverse()
    #     print(lst)
    #
    # print('\n# reverse example 2')
    # lst = CircularList()
    # print(lst)
    # lst.reverse()
    # print(lst)
    # lst.add_back(2)
    # lst.add_back(3)
    # lst.add_front(1)
    # lst.reverse()
    # print(lst)
    #
    # print('\n# reverse example 3')
    #
    #
    # class Student:
    #     def __init__(self, name, age):
    #         self.name, self.age = name, age
    #
    #     def __eq__(self, other):
    #         return self.age == other.age
    #
    #     def __str__(self):
    #         return str(self.name) + ' ' + str(self.age)
    #
    #
    # s1, s2 = Student('John', 20), Student('Andy', 20)
    # lst = CircularList([s1, s2])
    # print(lst)
    # lst.reverse()
    # print(lst)
    # print(s1 == s2)
    #
    # print('\n# reverse example 4')
    # lst = CircularList([1, 'A'])
    # lst.reverse()
    # print(lst)
    #
    # print('\n# sort example 1')
    # test_cases = (
    #     [1, 10, 2, 20, 3, 30, 4, 40, 5],
    #     ['zebra2', 'apple', 'tomato', 'apple', 'zebra1'],
    #     [(1, 1), (20, 1), (1, 20), (2, 20)]
    # )
    # for case in test_cases:
    #     lst = CircularList(case)
    #     print(lst)
    #     lst.sort()
    #     print(lst)
    #
    # print('\n# rotate example 1')
    # source = [_ for _ in range(-20, 20, 7)]
    # for steps in [1, 2, 0, -1, -2, 28, -100]:
    #     lst = CircularList(source)
    #     lst.rotate(steps)
    #     print(lst, steps)
    #
    # print('\n# rotate example 2')
    # lst = CircularList([10, 20, 30, 40])
    # for j in range(-1, 2, 2):
    #     for _ in range(3):
    #         lst.rotate(j)
    #         print(lst)
    #
    # print('\n# rotate example 3')
    # lst = CircularList([])
    # lst.rotate(10)
    # print(lst)
    #
    # print('\n# remove_duplicates example 1')
    # test_cases = (
    #     [1, 2, 3, 4, 5], [1, 1, 1, 1, 1],
    #     [], [1], [1, 1], [1, 1, 1, 2, 2, 2],
    #     [0, 1, 1, 2, 3, 3, 4, 5, 5, 6],
    #     list("abccd"),
    #     list("005BCDDEEFI")
    # )
    #
    # for case in test_cases:
    #     lst = CircularList(case)
    #     print('INPUT :', lst)
    #     lst.remove_duplicates()
    #     print('OUTPUT:', lst)
    #
    # print('\n# odd_even example 1')
    # test_cases = (
    #     [1, 2, 3, 4, 5], list('ABCDE'),
    #     [], [100], [100, 200], [100, 200, 300],
    #     [100, 200, 300, 400],
    #     [10, 'A', 20, 'B', 30, 'C', 40, 'D', 50, 'E']
    # )
    #
    # for case in test_cases:
    #     lst = CircularList(case)
    #     print('INPUT :', lst)
    #     lst.odd_even()
    #     print('OUTPUT:', lst)
    #
    print('\n# add_integer example 1')
    test_cases = (
        ([1, 2, 3], 10456),
        ([], 25),
        ([2, 0, 9, 0, 7], 108),
        ([9, 9, 9], 9_999_999)
    )
    for list_content, integer in test_cases:
        lst = CircularList(list_content)
        print('INPUT :', lst, 'INTEGER', integer)
        lst.add_integer(integer)
        print('OUTPUT:', lst)

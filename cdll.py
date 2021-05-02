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





    def reverse(self) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def sort(self) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def rotate(self, steps: int) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def remove_duplicates(self) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def odd_even(self) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def add_integer(self, num: int) -> None:
        """
        TODO: Write this implementation
        """
        pass


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
    print('\n# count example 1')
    lst = CircularList([1, 2, 3, 1, 2, 2])
    print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))
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
    # lst = CircularList()
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

    # print('\n# add_integer example 1')
    # test_cases = (
    #   ([1, 2, 3], 10456),
    #   ([], 25),
    #   ([2, 0, 9, 0, 7], 108),
    #    ([9, 9, 9], 9_999_999),
    #
    # for list_content, integer in test_cases:
    #    lst = CircularList(list_content)
    # print('INPUT :', lst, 'INTEGER', integer)
    # lst.add_integer(integer)
    # print('OUTPUT:', lst)

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

        midway = self.length()//2
        count = midway

        # assigning index 1 and index 2 to use with swap_pairs method
        index_1 = 0
        index_2 = self.length() - 1

        # swapping the first half of the list with its mirror image on the second half of the list
        while count != 0:
            self.swap_pairs(index_1, index_2)
            index_1 += 1
            index_2 -= 1
            count -= 1

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

        # starting with number that is not 0 to start while loop
        count = 1

        while count != 0:
            count = 0
            curr = self.sentinel.next
            curr_next = self.sentinel.next.next

            for node in range(0, self.length()):
                # breaking since the sentinel value NONE can't be compared
                if curr == self.sentinel or curr_next == self.sentinel:
                    break
                curr_val = curr.value
                next_val = curr_next.value

                # swap places if current value (left side) is greater than the next node
                if curr_val > next_val:
                    self.swap_pairs(node, node + 1)
                    count += 1
                    curr_next = curr.next
                else:
                    curr = curr.next
                    curr_next = curr.next

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
        pass




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

        count = (self.length()-1)//2
        prev_odd = self.sentinel.next
        curr_even = prev_odd.next
        curr_odd = curr_even.next

        # accounts for an odd length array
        while count != 0 and self.length() > 2 and self.length() % 2 != 0:
            # defining next odd and next even for later use
            next_odd = curr_odd.next.next
            next_even = curr_even.next.next

            # linking curr odd prev to prev odd and prev odd next to curr odd
            curr_odd.prev = prev_odd
            prev_odd.next = curr_odd

            # updating previous odd
            prev_odd = curr_odd

            # linking curr even to back of self.sentinel and curr even prev to sentinel prev
            curr_even.next = self.sentinel
            curr_even.prev = self.sentinel.prev

            self.sentinel.prev.next = curr_even
            self.sentinel.prev = curr_even

            # updating curr_even to next even node
            curr_odd = next_odd
            curr_even = next_even

            count -= 1

        # accounts for even length array (where to apply the remaining index)
        while count != 0 and self.length() > 2 and self.length() % 2 == 0:
            # defining next odd and next even for later use
            next_odd = curr_odd.next.next
            next_even = curr_even.next.next

            # linking curr odd prev to prev odd and prev odd next to curr odd
            curr_odd.prev = prev_odd
            prev_odd.next = curr_odd

            # updating previous odd
            prev_odd = curr_odd

            # linking curr even to back of self.sentinel prev and curr even prev to sentinel prev prev
            curr_even.next = self.sentinel.prev
            curr_even.prev = self.sentinel.prev.prev

            self.sentinel.prev.prev.next = curr_even
            self.sentinel.prev.prev = curr_even

            # updating curr_even to next even node
            curr_odd = next_odd
            curr_even = next_even

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

        # convert CDLL to integer
        length = self.length()
        factor = self.length() - 1
        curr = self.sentinel.next
        cdll_integer = 0

        for node in range(0, length):
            val = curr.value
            cdll_integer += val*(10**factor)
            factor -= 1
            curr = curr.next

        # find the sum of the two integers
        total = cdll_integer + num

        # finding total amount of nodes needed
        total_copy = total
        factor = 0
        while total_copy >= 10:
            total_copy = total_copy//10
            factor += 1

        # changing values
        curr = self.sentinel.next
        beginning_factor = factor
        start = 0

        # handles zeroes in front (i.e. ([0, 7], 1 --> [0, 8]))
        # total would use less nodes than originally given
        for zero in range(start, length):
            if beginning_factor < length - 1:
                curr.val = 0
                beginning_factor += 1
                start += 1
                curr = curr.next

        for pos in range(start, length):
            val = total // (10 ** factor)
            total -= val*(10**factor)
            factor -= 1
            curr.value = val
            curr = curr.next

        # if there is a remaining total, factor will not be -1
        while factor != -1:
            add_val = total//(10 ** factor)
            total -= add_val*(10**factor)
            factor -= 1
            self.add_back(add_val)



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
    print('\n# sort example 1')
    test_cases = (
        [1, 10, 2, 20, 3, 30, 4, 40, 5],
        ['zebra2', 'apple', 'tomato', 'apple', 'zebra1'],
        [(1, 1), (20, 1), (1, 20), (2, 20)]
    )
    for case in test_cases:
        lst = CircularList(case)
        print(lst)
        lst.sort()
        print(lst)
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
    #
    # print('\n# add_integer example 1')
    # test_cases = (
    #     ([1, 2, 3], 10456),
    #     ([], 25),
    #     ([2, 0, 9, 0, 7], 108),
    #     ([9, 9, 9], 9_999_999)
    # )
    # for list_content, integer in test_cases:
    #     lst = CircularList(list_content)
    #     print('INPUT :', lst, 'INTEGER', integer)
    #     lst.add_integer(integer)
    #     print('OUTPUT:', lst)

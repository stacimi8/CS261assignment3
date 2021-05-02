# Course: CS261 - Data Structures
# Student Name: Staci Ihori
# Assignment: Programming Assignment 3: Implementation of Linked Lists, ADTs using
#             Linked Lists and Binary Search
# Description: Implementation of Deque and Bag ADT interfaces with a Singly Linked
#              Linked List data structure.


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class SLNode:
    """
    Singly Linked List Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        self.next = None
        self.value = value


class LinkedList:
    def __init__(self, start_list=None):
        """
        Initializes a new linked list with front and back sentinels
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.head = SLNode(None)
        self.tail = SLNode(None)
        self.head.next = self.tail

        # populate SLL with initial values (if provided)
        # before using this feature, implement add_back() method
        if start_list is not None:
            for value in start_list:
                self.add_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        if self.head.next != self.tail:
            cur = self.head.next.next
            out = out + str(self.head.next.value)
            while cur != self.tail:
                out = out + ' -> ' + str(cur.value)
                cur = cur.next
        out = out + ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        cur = self.head
        while cur.next != self.tail:
            cur = cur.next
            length += 1
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.head.next == self.tail

    # ------------------------------------------------------------------ #

    def add_front(self, value: object) -> None:
        """
        A function that adds a new node at the beginning of the list (right after
        the front sentinel).
        """

        new_node = SLNode(value)

        # link new node's next node to self.head's next node
        new_node.next = self.head.next

        # update self.head's next node link to the new node
        self.head.next = new_node

    def add_back(self, value: object) -> None:
        """
        A function that adds a new node at the end of the list (right before the
        back sentinel).
        """
        # traverse the list to find last node
        new_node = SLNode(value)
        self.add_back_helper(new_node, curr=self.head)

    def add_back_helper(self, new_node, curr):
        """A recursive helper for add_back method."""

        if curr.next == self.tail:
            # link new node's next node to self.tail
            new_node.next = self.tail

            # update the current node's next node link to the new node
            curr.next = new_node
            return

        self.add_back_helper(new_node, curr.next)

    def insert_at_index(self, index: int, value: object) -> None:
        """
        A function that adds a new value at the specified index position in the
        linked list. Index 0 refers to the beginning of the list (right after the
        front sentinel). If the provided index is invalid, the method raises a
        custom “SLLException”. If the linked list contains N nodes (not including
        sentinel nodes in this count), valid indices for this method are [0, N]
        inclusive.
        """

        # invalid index
        if 0 > index or index > self.length():
            raise SLLException

        new_node = SLNode(value)
        self.insert_at_index_helper(index, new_node, curr=self.head, pos=0)

    def insert_at_index_helper(self, index, new_node, curr, pos):
        """A recursive helper for insert_at_index method."""

        # index is found at pos
        if pos == index:
            new_node.next = curr.next
            curr.next = new_node
            return

        # calling method again because index was not found at pos
        self.insert_at_index_helper(index, new_node, curr.next, pos + 1)

    def remove_front(self) -> None:
        """
        A function that removes the first node from the list. If the list is
        empty, the method raises a custom “SLLException”.
        """

        if self.is_empty():
            raise SLLException

        self.head.next = self.head.next.next

    def remove_back(self) -> None:
        """
        A function that removes the last node from the list. If the list is
        empty, the method raises a custom “SLLException”.
        """

        if self.is_empty():
            raise SLLException

        self.remove_back_helper(curr=self.head)

    def remove_back_helper(self, curr):
        """A recursive helper for remove_back method."""

        # found the node right before the last node in the list
        if curr.next.next == self.tail:
            curr.next = self.tail
            return

        self.remove_back_helper(curr.next)

    def remove_at_index(self, index: int) -> None:
        """
        A function that removes a node from the list given its index. Index 0
        refers to the beginning of the list (right after the front sentinel).
        If the provided index is invalid, the method raises a custom “SLLException”.
        If the list contains N elements (not including sentinel nodes in this count),
        valid indices for this method are [0, N - 1] inclusive.
        """

        # invalid index
        if 0 > index or index > self.length() - 1:
            raise SLLException

        self.remove_at_index_helper(index, curr=self.head, pos=0)

    def remove_at_index_helper(self, index, curr, pos):
        """A recursive helper for remove_at_index method."""

        # index is found at pos
        if pos == index:
            curr.next = curr.next.next
            return

        self.remove_at_index_helper(index, curr.next, pos + 1)

    def get_front(self) -> object:
        """
        Returns the value from the first node in the list without removing it.
        If the list is empty, the method raises a custom “SLLException”.
        """

        if self.is_empty():
            raise SLLException

        return self.head.next.value

    def get_back(self) -> object:
        """
        Returns the value from the last node in the list without removing it.
        If the list is empty, the method raises a custom “SLLException”.
        """

        if self.is_empty():
            raise SLLException

        return self.get_back_helper(curr=self.head)

    def get_back_helper(self, curr):
        """A recursive helper for get_back method."""

        # found last node in the list
        if curr.next == self.tail:
            return curr.value

        return self.get_back_helper(curr.next)

    def remove(self, value: object) -> bool:
        """
        A function that traverses the list from the beginning to the end and
        removes the first node in the list that matches the provided “value”
        object. The method returns True if some node was actually removed from
        the list. Otherwise, it returns False.
        """

        return self.remove_helper(value, curr=self.head.next, pos=0)

    def remove_helper(self, value, curr, pos):
        """A recursive helper for the remove method."""

        # base case: traversed through entire list - value not found, returns False
        if curr == self.tail:
            return False

        # value is found, removed first matched value, and returns True
        if curr.value == value:
            self.remove_at_index(pos)
            return True

        return self.remove_helper(value, curr.next, pos + 1)

    def count(self, value: object) -> int:
        """
        A function that counts and returns the number of elements in the list
        that matches the provided "value" object.
        """

        return self.count_helper(value, curr=self.head.next, count=0)

    def count_helper(self, value, curr, count):
        """A recursive helper for the count method."""

        # base case: traversed through entire list
        if curr == self.tail:
            return count

        # if a match is found, add 1 to count
        if curr.value == value:
            count += 1
            return self.count_helper(value, curr.next, count)

        return self.count_helper(value, curr.next, count)

    def slice(self, start_index: int, size: int) -> object:
        """Returns a new LinkedList object that contains the requested number of
        nodes from the original list starting with the node located at the requested
        start index. If the original list contains N nodes, a valid start_index is
        in range [0, N - 1] inclusive. Runtime complexity of your implementation
        must be O(N). If the provided start index is invalid or if there are not
        enough nodes between the start index and the end of the list to make a slice
        of the requested size, this method raises a custom “SLLException”.
        """

        # invalid start
        if start_index < 0 or start_index > self.length() - 1:
            raise SLLException

        # invalid size
        if size + start_index > self.length():
            raise SLLException

        # invalid size - size is negative
        if size < 0:
            raise SLLException

        end_index = size + start_index - 1

        # created new LinkedList for slice
        new_linked_list = LinkedList()

        return self.slice_helper(start_index, end_index, new_linked_list, curr=self.head.next, pos=0)

    def slice_helper(self, start_index, end_index, new_linked_list, curr, pos):
        """A recursive helper for slice method."""

        # base case: traversed through entire slice
        if pos > end_index:
            return new_linked_list

        # if position is within slice, add value to new LinkedList
        if start_index <= pos <= end_index:
            val = curr.value
            new_linked_list.add_back(val)

        return self.slice_helper(start_index, end_index, new_linked_list, curr.next, pos + 1)


if __name__ == '__main__':
    pass

    # print('\n# add_front example 1')
    # list = LinkedList()
    # print(list)
    # list.add_front('A')
    # list.add_front('B')
    # list.add_front('C')
    # print(list)
    #
    #
    # print('\n# add_back example 1')
    # list = LinkedList()
    # print(list)
    # list.add_back('C')
    # list.add_back('B')
    # list.add_back('A')
    # print(list)
    #
    #
    # print('\n# insert_at_index example 1')
    # list = LinkedList()
    # test_cases = [(0, 'A'), (0, 'B'), (1, 'C'), (3, 'D'), (-1, 'E'), (5, 'F')]
    # for index, value in test_cases:
    #     print('Insert of', value, 'at', index, ': ', end='')
    #     try:
    #         list.insert_at_index(index, value)
    #         print(list)
    #     except Exception as e:
    #         print(type(e))
    #
    #
    # print('\n# remove_front example 1')
    # list = LinkedList([1, 2])
    # print(list)
    # for i in range(3):
    #     try:
    #         list.remove_front()
    #         print('Successful removal', list)
    #     except Exception as e:
    #         print(type(e))
    #
    #
    # print('\n# remove_back example 1')
    # list = LinkedList()
    # try:
    #     list.remove_back()
    # except Exception as e:
    #     print(type(e))
    # list.add_front('Z')
    # list.remove_back()
    # print(list)
    # list.add_front('Y')
    # list.add_back('Z')
    # list.add_front('X')
    # print(list)
    # list.remove_back()
    # print(list)
    #
    #
    # print('\n# remove_at_index example 1')
    # list = LinkedList([1, 2, 3, 4, 5, 6])
    # print(list)
    # for index in [0, 0, 0, 2, 2, -2]:
    #     print('Removed at index:', index, ': ', end='')
    #     try:
    #         list.remove_at_index(index)
    #         print(list)
    #     except Exception as e:
    #         print(type(e))
    # print(list)
    #
    #
    # print('\n# get_front example 1')
    # list = LinkedList(['A', 'B'])
    # print(list.get_front())
    # print(list.get_front())
    # list.remove_front()
    # print(list.get_front())
    # list.remove_back()
    # try:
    #     print(list.get_front())
    # except Exception as e:
    #     print(type(e))
    #
    #
    # print('\n# get_back example 1')
    # list = LinkedList([1, 2, 3])
    # list.add_back(4)
    # print(list.get_back())
    # list.remove_back()
    # print(list)
    # print(list.get_back())
    #
    #
    # print('\n# remove example 1')
    # list = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    # print(list)
    # for value in [7, 3, 3, 3, 3]:
    #     print(list.remove(value), list.length(), list)
    #
    #
    # print('\n# count example 1')
    # list = LinkedList([1, 2, 3, 1, 2, 2])
    # print(list, list.count(1), list.count(2), list.count(3), list.count(4))
    #
    #
    print('\n# slice example 1')
    list = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = list.slice(1, 3)
    print(list, ll_slice, sep="\n")
    ll_slice.remove_at_index(0)
    print(list, ll_slice, sep="\n")


    print('\n# slice example 2')
    list = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", list)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Slice", index, "/", size, end="")
        try:
            print(" --- OK: ", list.slice(index, size))
        except:
            print(" --- exception occurred.")

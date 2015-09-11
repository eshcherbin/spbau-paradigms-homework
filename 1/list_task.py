

# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    return [lst[i] for i in range(len(lst)) if i == 0 or lst[i] != lst[i - 1]]


# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    res = []
    while lst1 or lst2:
        if not lst1 or not lst2:
            res.append(lst1.pop() if lst1 else lst2.pop())
        elif lst1[-1] > lst2[-1]:
            res.append(lst1.pop())
        else:
            res.append(lst2.pop())
    res.reverse()
    return res


if __name__ == '__main__':
    assert remove_adjacent([1, 1, 2, 2, 3]) == [1, 2, 3]
    assert linear_merge([2, 4, 6], [1, 2, 3, 5]) == [1, 2, 2, 3, 4, 5, 6]

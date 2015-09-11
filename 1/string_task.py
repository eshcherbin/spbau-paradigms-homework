

# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
#
# Example input: 'read'
# Example output: 'reading'
def verbing(s):
    if len(s) >= 3:
        s += 'ly' if s[-3:] == 'ing' else 'ing'
    return s


# Given a string, find the first appearance of the
# substring 'not' and 'bad'. If the 'bad' follows
# the 'not', replace the whole 'not'...'bad' substring
# with 'good'.
# Return the resulting string.
#
# Example input: 'This dinner is not that bad!'
# Example output: 'This dinner is good!'
def not_bad(s):
    not_pos, bad_pos = s.find('not'), s.find('bad')
    return s if not_pos == -1 or bad_pos == -1 or not_pos > bad_pos \
                else s[:not_pos] + 'good' + s[bad_pos+3:]


# Consider dividing a string into two halves.
# If the length is even, the front and back halves are the same length.
# If the length is odd, we'll say that the extra char goes in the front half.
# e.g. 'abcde', the front half is 'abc', the back half 'de'.
#
# Given 2 strings, a and b, return a string of the form
#  a-front + b-front + a-back + b-back
#
# Example input: 'abcd', 'xy'
# Example output: 'abxcdy'
def front_back(a, b):
    return a[:(len(a) + 1) // 2] + b[:(len(b) + 1) // 2] + \
        a[(len(a) + 1) // 2:] + b[(len(b) + 1) // 2:]


if __name__ == '__main__':
    assert verbing('aa') == 'aa'
    assert verbing('read') == 'reading'
    assert verbing('ing') == 'ingly'
    assert not_bad('This dinner is not that bad!') == 'This dinner is good!'
    assert not_bad('badnot') == 'badnot'
    assert not_bad('notbadnotbad') == 'goodnotbad'
    assert front_back('abcde', 'xy') == 'abcxdey'

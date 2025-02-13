from timeit import timeit
from random import randint


def remove_duplicate_loop(a):
    new_list = []
    for x in a:
        if x not in new_list:
            new_list.append(x)
    return new_list


def remove_duplicate_dict(a):
    return list(dict().fromkeys(a).keys())


def remove_duplicate_set(a):
    new_list = []
    seen = set()
    for x in a:
        if x not in seen:
            new_list.append(x)
            seen.add(x)
    return new_list


print('Test random sparse in ns')
for n in 10, 100, 1000, 10000, 50000:
    print('N:', n)
    a = [randint(0, n * 10) for _ in range(n)]
    print('  loop: %11d' % int(timeit('remove_duplicate_loop(a)', globals=globals(), number=1) * (10 ** 9)))
    print('  dict: %11d' % int(timeit('remove_duplicate_dict(a)', globals=globals(), number=1) * (10 ** 9)))
    print('  set : %11d' % int(timeit('remove_duplicate_set(a)', globals=globals(), number=1) * (10 ** 9)))

print()
print('Test random dense in ns')
for n in 10, 100, 1000, 10000, 50000:
    print('N:', n)
    a = [randint(0, n // 5) for _ in range(n)]
    print('  loop: %10d' % int(timeit('remove_duplicate_loop(a)', globals=globals(), number=1) * (10 ** 9)))
    print('  dict: %10d' % int(timeit('remove_duplicate_dict(a)', globals=globals(), number=1) * (10 ** 9)))
    print('  set : %10d' % int(timeit('remove_duplicate_set(a)', globals=globals(), number=1) * (10 ** 9)))
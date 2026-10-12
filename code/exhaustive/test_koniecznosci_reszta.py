from test_koniecznosci import test
for pr, q in (([2,5,7,11,13],3), ([2,3,5,7,13],11), ([2,3,7,11,13,17],5), ([2,3,5,11,13,17],7)):
    test(pr, q, 40)

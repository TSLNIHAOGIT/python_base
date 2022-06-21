import bisect

a = [0, 4, 5, 7, 19, 25]

# a[2]=5，表示值5的索引位置是2
# bisect 函数其实是 bisect_right 函数的别名，后者还有个姊妹函数叫bisect_left。
# bisect_left函数是新元素会被放置于它相等的元素的前面，而 bisect_right返回的则是跟它相等的元素之后的位置。
# 这个返回3，是因为bisect会把新的元素放在相等元素后面即 2 + 1 = 3
a1 = bisect.bisect(a, 5)

# 这个返回2，是因为bisect_left会把新的元素放在相等元素前面即原来值5的索引位置2
a2 = bisect.bisect_left(a, 5)
a3 = bisect.bisect_right(a, 55)

print(a1, a2,a3) # 3, 2

def len_of_longest_ascending_subsequences(nums):
		if len(nums)<=1:
			return len(nums)
		# 用来存放各个字串的最长上升子序列个数
		mem = [1 for _ in range(len(nums))]

		for j in range(1,len(nums)):
			for i in range(0,j):
				# 1<2
				if nums[i]<nums[j]:
					# max(1,1+1)
					# 更新各个字串的最长上升子序列个数
					# 状态转移方程
					mem[j] = max(mem[j],mem[i]+1)
					# mem[1] = 2
		print(mem)

		return max(mem)
# list01=[2,-5,-6,-8,-3,3,56,6,3,6,7,100,9,3]
list01=[1,2,6,3,5,8]
# list01=[1]
print(len_of_longest_ascending_subsequences(list01))

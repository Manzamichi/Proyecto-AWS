class Solution:
    def removeElement(self, nums: list[int], val: int) -> int:
        nums = [3,2,2,3]
        val = 3
        counter = 0
        for i in range(0, len(nums)):
            if nums[i] == val:
                nums.remove(val)
            counter += 1
        print(counter)
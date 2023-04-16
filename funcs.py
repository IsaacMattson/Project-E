def add(*nums):
    result = 0
    for num in nums:
        result+=num
    return result

def sub(*nums):
    result = nums[0]
    nums = nums[1:]
    for num in nums:
        result-=num
    return result

def mul(*nums):
    result = nums[0]
    nums = nums[1:]
    for num in nums:
        result*=num
    return result

def div(*nums):
    result = nums[0]
    nums = nums[1:]
    for num in nums:
        result/=num
    return result

def eq(*args):
    arg1 = args[0]
    for arg in args[1:]:
        if arg != arg1: return '#f'
    return '#t'

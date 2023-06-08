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
        if arg != arg1: return False
    return True


def add_dict(a,b):
    a.update(b)

def l_input(string):
    return input(string);

def load_lib(name):
    global global_env
    lib = __import__(name)
    global_env.update(lib.lib_env)
    
def test():
    pass

        

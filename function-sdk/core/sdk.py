#Sprint 1

registered_functions = {} 
def registerFunction(function_name: str, handler: callable, runtime: str) -> bool:
    """
    Allows developers to register a new function with the Osiris platform with 
    a unique name, handler (code logic), and runtime environment (e.g., Python, Node.js).
    Returns True if the registration is successful, False otherwise.
    """
    if function_name in registered_functions:
        print(f"Function '{function_name}' is already registered.")
        return False
    registered_functions[function_name] = {
        'handler': handler,
        'runtime': runtime, 
        'timeout': "none"
    }
    return True


def deregisterFunction(function_name: str) -> bool:
    pass

def invokeRegisteredFunction(function_name: str, *args: list) -> any:
    '''
    API calls a function that has been registered on the platform by passing in the necessary arguments and returning the result.
    The function is invoked with the specified arguments, and the output from the function handler is returned.
    '''
    if function_name in registered_functions:
        return registered_functions[function_name]['handler'](*args)
    else:
        raise ValueError(f"Function '{function_name}' is not registered.")

def setFunctionTimeout(function_name: str, timeout_ms: int) -> bool:
    """
    Sets a maximum execution time for a registered function. If the function exceeds this time, it will be terminated.
    It returns True if the timeout was successfully set, otherwise False.
    """
    if function_name in registered_functions:
        registered_functions[function_name]['timeout'] = timeout_ms
        return True
    return False

def setFunctionEnv(function_name: str, env_vars: dict) -> bool:
    pass

def getFunctionLogs(function_name: str, limit: int = 100) -> list:
    pass

def handleFunctionError(function_name: str, error_handler: callable) -> bool:
    pass

def invokeWithRetry(function_name: str, *args: list, retries: int = 3) -> any:
    pass

async def invokeFunctionAsync(function_name: str, input_data: dict) -> str:
    pass

def checkFunctionStatus(request_id: str) -> str:
    pass

async def getFunctionResultAsync(request_id: str) -> dict:
    pass

'''
#Test Case For API 1
print("Test Case 1:")
def addNumbers(a, b):
    return a + b
response = registerFunction("addNumbers", addNumbers, "Python 3.8") #should return true
if response:
    print("addNumbers is registered.")

#Test Case for API 3
print("Test Case 3:")
result = invokeRegisteredFunction("addNumbers", 3, 5)  # Should return 8
print(f"Result of addNumbers 3 and 5: {result}") 

#Text Case for API 4
print("Test Case 4:")
response = setFunctionTimeout("addNumbers", 5000)  # 5 seconds, should return true
print(f"Timeout set: {response}")
'''
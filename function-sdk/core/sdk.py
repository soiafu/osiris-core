#Sprint 1
from datetime import datetime
import asyncio
import uuid

registered_functions = {} 
async_status = {}
async_result = {}
logs_storage = {} # separate storage for logs
error_handlers = {}

#API 1 -  Register Function Command
def registerFunction(function_name: str, handler: callable, runtime: str) -> bool:
    """
    Allows developers to register a new function with the Osiris platform with 
    a unique name, handler (code logic), and runtime environment (e.g., Python, Node.js).
    
    Returns True if the registration is successful, False otherwise.
    
    Parameters:
        - function_name: The unique name of the function to register. (string)
        - handler: The function handler that contains the logic for this function. (callable)
        - runtime: The runtime environment (e.g., Python 3.8, Node.js). (string)
    """
    # Check if the function name is already registered
    if function_name in registered_functions:
        print(f"Function '{function_name}' is already registered.")
        return False

    #registered_functions[function_name] = handler #allows it to be callable
    # Register the function
    registered_functions[function_name] = {
        'handler': handler,
        'runtime': runtime, 
        'timeout': "none"
    }
    return True

#API 2: Deregister Function Command
def deregisterFunction(function_name: str) -> bool:
    '''
    The deregisterFunction API removes an existing function from the platform, ensuring that it can no longer be invoked.
    The function returns True if the deregistration is successful, False otherwise.

    Paramters:
        - function_name: The unique name of the function to deregister. (string)    
    '''
    # Check if the function name is registered
    if function_name in registered_functions:
        # Deregister the function
        del registered_functions[function_name]
        return True
    
    print(f"Error: Function '{function_name}' is not registered.")
    return False

#API 3 - Invoke Registered Function Command
def invokeRegisteredFunction(function_name: str, *args: list) -> any:
    '''
    API calls a function that has been registered on the platform by passing in the necessary arguments and returning the result.
    The function is invoked with the specified arguments, and the output from the function handler is returned.

    Parameters:
        - function_name: The name of the function to invoke. (string)
        - args: The list of arguments to pass to the function. (list of any)
    '''
    # Ensure logs_storage has a list for this function's logs
    if function_name not in logs_storage:
        logs_storage[function_name] = []
    
    # Helper function to generate a timestamped log message
    def timestamped_log(message: str) -> str:
        return f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}"

    if function_name in registered_functions:
        try:
            # Log function start with inputs
            inputs = ", ".join(map(str, args))
            logs_storage[function_name].append(timestamped_log(f"Function started with inputs: {inputs}"))
            
            # Invoke the function and get the result
            result = registered_functions[function_name]['handler'](*args)
            
            # Log the successful result
            logs_storage[function_name].append(timestamped_log(f"Function executed successfully. Result: {result}"))
            
            return result
        except Exception as e:
            # Log the error if function execution fails
            logs_storage[function_name].append(timestamped_log(f"Function execution failed with error: {str(e)}"))
            raise
    else:
        # Log if function is not registered
        logs_storage[function_name].append(timestamped_log("Attempted to invoke unregistered function"))
        raise ValueError(f"Function '{function_name}' is not registered.")

#API 4 - Set Function Timeout Command
def setFunctionTimeout(function_name: str, timeout_ms: int) -> bool:
    """
    Sets a maximum execution time for a registered function. If the function exceeds this time, it will be terminated.
    It returns True if the timeout was successfully set, otherwise False.

    Parameters:
        - function_name: The name of the function to set a timeout for.(string)
        - timeout_ms: The execution time limit in milliseconds. (integer)
    """
    #Check if function is registered
    if function_name in registered_functions:
        # Set the timeout in milliseconds
        registered_functions[function_name]['timeout'] = timeout_ms
        return True
    return False

#API 5: Set Function Environment Variables Command
def setFunctionEnv(function_name: str, env_vars: dict) -> bool:
    if function_name not in registered_functions:
        return False
    func = registered_functions[function_name]
    if "env_vars" not in func:
        func["env_vars"] = env_vars
    else:
        func["env_vars"].update(env_vars)
    return True

#API 6: Retrieve Function Logs Command
def getFunctionLogs(function_name: str, limit: int = 100) -> list:
    '''
    The getFunctionLogs API retrieves the logs for a specified function, with an optional limit on the number of log entries to return.
    It returns a list of log entries, where each entry is a string representing a log message.

    Parameters:
        - function_name: The name of the function to retrieve logs for. (string)
        - limit: The maximum number of log entries to return (default is 100). (integer)
    '''
    # Retrieve the logs for the given function name, or an empty list if not found
    logs = logs_storage.get(function_name, [])

    return logs[:limit]

# API 7: Handle Function Errors Command
def handleFunctionError(function_name: str, error_handler: callable) -> bool:
    try:
        error_handlers[function_name] = error_handler
        return True
    except Exception as e:
        print(f"Error in setting error handler: {e}")
        return False

# API 8: Invoke Function with Retry Command
def invokeWithRetry(function_name: str, *args: list, retries: int = 3) -> any:
    attempt = 0
    while attempt < retries:
        try:
            return invokeRegisteredFunction(function_name, *args)
        except Exception as e:
            attempt += 1
            if attempt == retries:
                raise e

#API 9: Invoke Function Asynchronously
async def invokeFunctionAsync(function_name: str, input_data: dict) -> str:
    request_id = f"request-{uuid.uuid4().hex[:8]}"
    async_status[request_id] = "pending"
    async def run_function(req):
        async_status[req] = "running"
        try:
            async_result[req] = invokeRegisteredFunction(function_name, input_data.values()[0], input_data.values()[1])
            async_status[req] = "completed"
        except:
            async_status[req] = "failed"
    asyncio.create_task(run_function(request_id))
    return request_id

#API 10: Check Function Status
def checkFunctionStatus(request_id: str) -> str:
    if request_id not in async_status:
        return "unrecognized"
    return async_status[request_id]

# API 11: Get Function Result
async def getFunctionResultAsync(request_id: str) -> dict:
    pass

# ------------ Test Cases --------------

#Test Case For API 1
print("Test Case 1:")
def addNumbers(a, b):
    return a + b
response = registerFunction("addNumbers", addNumbers, "Python 3.8") #should return true
if response:
    print("addNumbers is registered.")
print()

#Test Case for API 3
print("Test Case 3:")
result = invokeRegisteredFunction("addNumbers", 3, 5)  # Should return 8
print(f"Result of addNumbers 3 and 5: {result}") 
print()


#Text Case for API 4
print("Test Case 4:")
response = setFunctionTimeout("addNumbers", 5000)  # 5 seconds, should return true
print(f"Timeout set: {response}")
print()


#Text Case for API 6
print("Test Case 6:")
logs = getFunctionLogs("addNumbers", limit=10)
print(f"Logs for addNumbers: {logs}")
print()

# Test case of API 5
print("Test Case 5:")
response = setFunctionEnv("addNumbers", {"a": 1, "b": 2})
response = setFunctionEnv("addNumbers", {"b": 1, "c": 2})
print(response, registered_functions)

# Test case of API 9 and 10
print("Test Case 9 and 10:")
async def test_api9():
    input_data = {
        "a": 10,
        "b": 5
    }
    request_id = await invokeFunctionAsync("addNumbers", input_data)
    print(request_id)
    print(checkFunctionStatus(request_id))
    await asyncio.sleep(1)
    print(checkFunctionStatus(request_id))

asyncio.run(test_api9())

#Test case API 7 8
print("Test case 7")
def customErrorHandler(error):
    print(f"Error occurred: {error}")

response = handleFunctionError("addNumbers", customErrorHandler)
print(response)

print("test case 8")
response = invokeWithRetry("addNumbers", 3, 5, retries=3)
print(response)


#PUTTING AT END SO THAT FUNCTION EXISTS FOR OTHER TEST CASES
#Test Case for API 2 
print("Test Case 2:")
response = deregisterFunction("addNumbers")
print(f"Result of deregistering addNumbers: {response}") 

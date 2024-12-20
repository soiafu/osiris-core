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
    if function_name not in logs_storage:
        logs_storage[function_name] = []
    
    def timestamped_log(message: str) -> str:
        return f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}"

    if function_name in registered_functions:
        try:
            # test case for dictionary
            if len(args) == 1 and isinstance(args[0], dict) and "__async_key" in args[0]:
                input_data = args[0]
                prepared_args = []
                for key in args[0]:
                    if key != "__async_key":
                        prepared_args.append(input_data[key])
            else: 
                prepared_args = args
            inputs = ", ".join(map(str, prepared_args))
            print("Arguments:", prepared_args)
            logs_storage[function_name].append(timestamped_log(f"Function started with inputs: {inputs}"))
            result = registered_functions[function_name]['handler'](*prepared_args)
            logs_storage[function_name].append(timestamped_log(f"Function executed successfully. Result: {result}"))
            print(f"result {result}")
            return result
        except Exception as e:
            logs_storage[function_name].append(timestamped_log(f"Function execution failed with error: {str(e)}"))
            raise
    else:
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
            #key_value_pairs = [(key, value) for key, value in input_data.items()]
            #async_result[req] = await asyncio.to_thread(invokeRegisteredFunction, function_name, *key_value_pairs)
            input_data["__async_key"] = True
            async_result[req] = invokeRegisteredFunction(function_name, input_data)
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
    while checkFunctionStatus(request_id) != "completed":
        print(f"Waiting for completion of {request_id}")
        await asyncio.sleep(1)  

    result = async_result.get(request_id, {})
    print(f"Result for {request_id}: {result}")
    return result

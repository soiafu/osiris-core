def registerFunction(function_name: str, handler: callable, runtime: str) -> bool:
    pass

def deregisterFunction(function_name: str) -> bool:
    pass

def invokeRegisteredFunction(function_name: str, *args: list) -> any:
    pass

def setFunctionTimeout(function_name: str, timeout_ms: int) -> bool:
    pass

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
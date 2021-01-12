import concurrent.futures
import os
from functools import wraps

def make_parallel(func):
    """
        Parallelizes the execution of the funcion called using futures
        :param func: function
            The instance of the function that needs to be parallelized.
        :return: function
    """

    @wraps(func)
    def wrapper(lst):
        """
        Creates max number of threads based on the items in the list limiting to the cpus for not to overwhelm
        :param lst:
            The inputs of the function in a list.
        :return:
        """        
        number_of_threads_multiple = 2 
        number_of_workers = int(os.cpu_count() * number_of_threads_multiple)
        if len(lst) < number_of_workers:
            number_of_workers = len(lst)

        if number_of_workers:
            if number_of_workers == 1:
                result = [func(lst[0])]
            else:
                result = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executer:                    
                    bag = {executer.submit(func, i): i for i in lst}
                    for f, i in bag.items():
                        try:
                            output = concurrent.futures.as_completed({f:i})                            
                            result.append(next(output).result())
                        except Exception as e:
                            print(f"Failed to retrieve analyst info for {e} with {i}")                        
        else:
            result = []
        return result
    return wrapper
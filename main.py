import numpy as np
import time
import re
import random
import string
import asyncio
from strgen import StringGenerator as SG


'''
Pseudo Class manipulates random strings 
'''
class Pseudo:
    def __init__(self):
        pass

    #Generate random strings based on StringGenerator Module#
    def generate_rand_string(self):
        self.rand_num = np.random.randint(low=3,high=10)
        self.rand_pattern = "[A-Z]{"+str(self.rand_num)+"}"
        return SG(self.rand_pattern).render()

    #Handles 50-50% Probability#
    def binary_clock(self):
        self.rand_choice = np.random.choice([True,False])
        return self.rand_choice

    #Fix String Generate#
    def get_Maruti(self):
        return "MARUTI"

async def start_conditional_string():
    pseu_obj = Pseudo()

    while True:

        try:
            choice = pseu_obj.binary_clock()

            # 50-50% Probability Logic #
            if choice:
                pseu_string = pseu_obj.get_Maruti()
            else:
                pseu_string = pseu_obj.generate_rand_string()

            print(pseu_string)
            await asyncio.sleep(1.0)

        except KeyboardInterrupt:
            print('Keyboard interrupt caught')
            break
    return


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = loop.create_task(start_conditional_string())
    loop.run_until_complete(task)

    #Handling the pending tasks#
    pending = asyncio.all_tasks(loop=loop)
    for tasks in pending:
        tasks.cancel()

    # Throw exception error in tasks #
    group = asyncio.gather(*pending, return_exceptions=True)
    loop.run_until_complete(group)





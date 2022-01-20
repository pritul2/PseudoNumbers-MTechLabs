import numpy as np
import os
import time
import re
import random
import string
import asyncio
from strgen import StringGenerator as SG

STRING = "MARUTI"

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

    def obtain_cndntn_string(self):
        self.choice = self.binary_clock()
        # 50-50% Probability Logic #
        if self.choice:
            self.pseu_string = STRING
        else:
            self.pseu_string = self.generate_rand_string()

        return self.pseu_string


class file:
    def __init__(self):
        self.file1_desc = open(os.getcwd()+"/fil1.txt","w")
        self.file2_desc = open(os.getcwd()+"/fil2.txt","w")
        self.logfile_desc = open(os.getcwd()+"/counts.log","w")
        self.pseu_obj_file1 = Pseudo()
        self.pseu_obj_file2 = Pseudo()

    async def write_data_file1(self):
        self.file1_desc.write(self.pseu_obj_file1.obtain_cndntn_string())
        await asyncio.sleep(1.0)


    async def write_data_file2(self):
        self.file2_desc.write(self.pseu_obj_file2.obtain_cndntn_string())
        await asyncio.sleep(1.0)


if __name__ == '__main__':

    f = file()

    loop = asyncio.get_event_loop()

    task1 = loop.create_task(f.write_data_file1())
    task2 = loop.create_task(f.write_data_file2())

    loop.run_until_complete(task1)
    loop.run_until_complete(task1)

    #Handling the pending tasks#
    pending = asyncio.all_tasks(loop=loop)
    for tasks in pending:
        tasks.cancel()

    # Throw exception error in tasks #
    group = asyncio.gather(*pending, return_exceptions=True)
    loop.run_until_complete(group)





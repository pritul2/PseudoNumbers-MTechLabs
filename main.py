import numpy as np
import re
import random
import string
import asyncio
from strgen import StringGenerator as SG

class Pseudo:
    def __init__(self):
        pass
    def generate_rand_string(self):
        self.rand_num = np.random.randint(low=3,high=10)
        self.rand_pattern = "[A-Z]{"+str(self.rand_num)+"}"
        return SG(self.rand_pattern).render()

pseu_obj = Pseudo()
print(pseu_obj.generate_rand_string())
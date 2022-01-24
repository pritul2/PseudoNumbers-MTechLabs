'''
Copyright Version: BETA
Developer: Pritul Dave
Organization: Maruti Tech Labs
This software is free to reuse
'''


import numpy as np
import os
import asyncio
from strgen import StringGenerator as SG
import time
import aiofiles


STRING = "MARUTI" #Fixed String#
START_TIME, END_TIME = time.time(), None #Time to activate monitor#
BREAK_SIGNAL = False


'''
Pseudo Class manipulates random strings
It generates and return psuedo strings
'''
class Pseudo:

    #Constructor#
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

    #Gives either random string or MARUTI string#
    def obtain_cndntn_string(self):
        self.choice = self.binary_clock()
        # 50-50% Probability Logic #
        if self.choice:
            self.pseu_string = STRING
        else:
            self.pseu_string = self.generate_rand_string()

        return self.pseu_string

'''
File class for file manipulation
'''
class file:

    #Constructor#
    def __init__(self):
        self.file1_desc = open(os.getcwd()+"/fil1.txt","w") #File 1 Descriptor#
        self.file2_desc = open(os.getcwd()+"/fil2.txt","w") #File 2 Descriptor#
        self.logfile_desc = open(os.getcwd()+"/counts.log","w") #Log file descriptor#
        self.pseu_obj_file1 = Pseudo() #Pseudo object for file 1#
        self.pseu_obj_file2 = Pseudo() #Pseudo object for file 2#
        self.fptr_pos1,self.fptr_pos2  = None, None #File pointer position to track and monitor#
        self.cntr1, self.cntr2 = 0, 0 #Counter to track MARUTI keyword#

    '''
    File Logger module
    It monitor and write MARUTI count in logger file
    '''
    async def logger(self):

        await asyncio.sleep(0.01)

        print("[INFO:] Inside logger")

        #Open both the files#
        self.read_file1 = open(os.getcwd()+"/fil1.txt","r")
        self.read_file2 = open(os.getcwd() + "/fil2.txt", "r")

        #Setting file pointer based on tracker#
        if self.fptr_pos1 is not None and self.fptr_pos2 is not None:
            print("Not none input")
            self.read_file1.seek(self.fptr_pos1)
            self.read_file2.seek(self.fptr_pos2)
        else:
            self.read_file1.seek(0)
            self.read_file2.seek(0)

        #Read the file 1#
        for lines in self.read_file1.readlines():
            print("[INFO:] Reading File 1 ")
            if lines[:-1] == STRING: #-1 because of \n#
                self.cntr1+=1
        await asyncio.sleep(0.01)

        #Set the file pointer to track#
        self.fptr_pos1 = self.read_file1.tell()

        #Read the file 2#
        for lines in self.read_file2.readlines():
            print("[INFO:] Reading File 2 ") #-1 because of \n#
            if lines[:-1] == STRING:
                self.cntr2+=1
        await asyncio.sleep(0.01)

        #Set the file pointer to track#
        self.fptr_pos2 = self.read_file2.tell()

        #Writing ino logger#
        self.logfile_desc.write("File1 count values are {} \n".format(self.cntr1))
        self.logfile_desc.write("File2 count values are {} \n".format(self.cntr2))

        self.logfile_desc.seek(0)
        self.logfile_desc.flush()

        await asyncio.sleep(0.01)


    async def read_data(self):
        while True:
            await asyncio.sleep(5)
            await self.logger()

    '''
    File Writing module
    Write the random strings through Asynchronous Programming
    '''

    async def write_data(self,file_descriptor,file_name):
        global START_TIME

        while True:

            try:

                print(f"Writing for {file_name}")

                #Writing the string#
                file_descriptor.write(self.pseu_obj_file1.obtain_cndntn_string()+"\n")
                file_descriptor.flush()
                await asyncio.sleep(0.5)

            #Handle the keyboard interrupt#
            except asyncio.CancelledError as error:
                global BREAK_SIGNAL
                if BREAK_SIGNAL:
                    return
                BREAK_SIGNAL=True
                print("Keyboard interrupt received")
                print("Closing the connections and files ... ")
                await asyncio.sleep(2) #To finish all threading operations#
                await self.logger()
                self.file1_desc.close()
                self.file2_desc.close()
                self.logfile_desc.close()
                return

            #Handle if anyother exception#
            except Exception as e:
                print("Something else exception occured")
                print(e.__class__.__name__)
                await asyncio.sleep(1.0)
                break


'''
Caller module
Main Asynchronous program caller
'''
async def caller():
    f = file()

    #Creating asynchronous tasks#
    task1 = loop.create_task(f.write_data(f.file1_desc,"File 1"))
    task2 = loop.create_task(f.write_data(f.file2_desc,"File 2"))
    task3  = loop.create_task(f.read_data())
    await asyncio.wait([task1,task2,task3])


if __name__ == '__main__':

    try:
        #Starting the async loop#
        loop = asyncio.get_event_loop()
        loop.run_until_complete(caller())

    except Exception as e:
        print("exception occured in asyncio")
        print(e)

    finally:
        #Handling the pending tasks#
        pending = asyncio.all_tasks(loop=loop)
        for tasks in pending:
            tasks.cancel()

        # Throw exception error in tasks #
        group = asyncio.gather(*pending, return_exceptions=True)
        loop.run_until_complete(group)
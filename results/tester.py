import os
import sys
from termcolor import colored, cprint



# frees, allocations only



frees_alloc = ["11", "7", "6", "5", "4", "3", "2"]
realloc = ["1"]
no_input = ["10"]
grow_heaps = ["9", "8"]

list_type = "implicit"
fit = "first"

test = False

def main():
    n = len(sys.argv)
    test = False


   # there are no warning signs if args are wrong
    i = 1
    while i < n:
        # i += 1
        global fit
        global list_type
        if sys.argv[i] == "best":
            fit = "best"
            i += 1
            continue
        elif sys.argv[i] == "first":
            fit = "first"
            i += 1
            continue
        elif sys.argv[i] == "implicit":
            list_type = "implicit"
            i += 1
            continue
        elif sys.argv[i] == "explicit":
            list_type = "explicit"
            i += 1
            continue
        elif sys.argv[i] == "test":
            test = True
            i += 1
            continue
        else:
            i += 1
    print(list_type, fit)



    if test:
        check_test()
        return



    execute_files(frees_alloc)
    execute_files(realloc)
    execute_files(no_input)
    execute_files(grow_heaps)



   # os.system("clear")
    print()
    print("FREES & ALLOCATIONS")
    check_results(frees_alloc)
    print()
    print("REALLOCS")
    check_results(realloc)
    print()
    print("NO INPUTS")
    check_results(no_input)
    print()
    print("GROW/SHRINK HEAPS")
    check_results(grow_heaps)



def check_test():
    cmd = 'python3 memoryalloc.py -o results.txt --free-list={} --fit={} test.txt'
    cmd = cmd.format(list_type, fit)
    os.system(cmd)



    cmd = "./A3-ref -o results2.txt --free-list={} --fit={} test.txt"
    cmd = cmd.format(list_type, fit)
    os.system(cmd)
    
    try:
        ref_path = "results2.txt"
        result_path = "results.txt"



        reference = open(ref_path)
        result = open(result_path)



        ref_out = reference.read()
        res_out = result.read()



        if ref_out == res_out:
            cprint("result matches answer", "green")
        else:
            cprint("result does not match answer", "yellow")
        reference.close()
        result.close()



    except:
        cprint("something went wrong", "red")



def execute_files(files):
    for i in files:
        cmd = 'python3 memoryalloc.py -o results/{}.txt --free-list={} --fit={} examples/{}.in'
        cmd = cmd.format(i,list_type, fit, i)
        os.system(cmd)



def check_results(files):
    for i in files:
        try:
            ref_path = "examples/{}.{}.{}.out".format(i, list_type, fit)
            result_path = "results/{}.txt".format(i)



            reference = open(ref_path)
            result = open(result_path)



            ref_out = reference.read()
            res_out = result.read()



            if ref_out == res_out:
                cprint("result matches references for file {}.in".format(i), "green")
            else:
                cprint("result does not match reference for file {}.in".format(i), "yellow")
            reference.close()
            result.close()
        except:
            cprint("something went wrong with file {}.in".format(i), "red")



main()
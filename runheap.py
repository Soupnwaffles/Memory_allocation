import memoryalloc as m 
def runlines(input,output): 
    # Run for each line in input 
    for line in input: 
        theline=line.split(",")
        if theline[0].strip()=="a": 
            theline[2] = m.myalloc()

    return 
def addNumbers(a:int,b:int)->str:
    '''addition of two numbers'''
    return f"{a}+{b}={(a+b)}"


def multiNumbers(a:int,b:int)->str:
    '''multiplication of 2 numbers'''
    return f"{a}*{b}={(a*b)}"

def subNumbers(a:int,b:int)->str:
    '''substraction of 2 numbers'''
    return f"{a}-{b}={(a-b)}"

def divNumbers(a:int,b:int)->str:
    '''division of 2 numbers'''
    return f"{a}/{b}={(a/b)}"

def saveFile(content:str)->str:
    '''saving content to a file i.e hello.txt'''
    with open("./hello.txt","w+") as file:
        file.write(content)
        file.close()
        return 'File Created Successfully'

def readFile(fileName:str)->str:
    '''reading from a file i.e hello.txt'''
    with open(f"./{fileName}","r+") as file:
        data = file.read()
        file.close()
        return data
    
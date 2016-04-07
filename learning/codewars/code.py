#Function Composition
add1  = lambda *a : sum(a)+1
this = lambda *a : sum(a)

#add1(1) 
#this(1)

def compose(f, g):    
    return lambda x: f(g(x))
    
compose(add1,this)(5)
compose(add1,this)(3,1)
##########################################################
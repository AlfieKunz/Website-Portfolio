# ~~~~~~~~~~ VSCODE THEMES ~~~~~~~~~~
#  1) Ayu Mirage
#  2) Moonlight I Italic
#  3) GitHub Dark Dimmed
#  4) Noctis Azureus
#  5) Beautiful Dracula Darker
#  Visual Studio Theme: Zero LCH SB 1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



def General_Info():
    #CTRL+L = Clear Terminal
    #String Concatination with +, not &! Cannot combine two different variable types.
    LargeNumber = 2.0e12
    ComplexNumber = 3 + 4j
    print(np.conjugate(ComplexNumber))
    #MUST REFER TO NUMBER AS "a = 2." TO REFER AS DECIMAL!! NOT "a = 2"!!!!!!!!!!!!!!!!!!!!!!!!!
    
    testVar = 23.141
    if isinstance(testVar, (float, int)):
        return None

    np.arctan2(4, 3) #arctan(4/3) but for the correct quadrant :).
    
    #Try-Catch shenanigans
    try:
        x = np.sqrt(-3)
    except:
        x = "lol nope"
    print(x)
    
    #Functions can return multiple variables!!! Return x1,x2,x3
    
    #MAKE SURE YOU USE \n WHEN WRITING TO FILES!!!!!!!!!!
    
    #Variables in functions can be optional! Just use Function(x, y=12, z=0), where these are default values if they are not provided.







def ListsTuples():
    emptyList = [] #square brackets.
    myList = ["apple", "banana", "alfredo", 21893, True, 1j, [1,2,3]]
    myList[2] = "jo"
    print(myList[-2]) #WTF THAT IS NOT ALLOWED AGHAGAGHGAHAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH im scared
    print("banana" in myList)

    myList.append("hippity hoppity")
    print(myList[6][1])
    del myList[3]
    print(myList)
    print("apple" in myList) #returns True / False.
    print("\n")

    print(myList.index(True))
    print(len(myList))
    print("\n")

    ListTwo = ["AGHHHH", False, [myList]]
    print(myList + ListTwo)
    print(myList * 2)
    print("\n")
    
    for i, a in enumerate(ListTwo):
        print(str(a) + " is at index " + str(i))
    print("\n")
    
    CoolList = [i**2 for i in range(1,13)]
    print(CoolList)
    
    CoolListTwo = [(1/n if n%2 == 0  else  -1/n) for n in range(1,10)]
    print(CoolListTwo)
    
    odds = [1,3,5,7,9,11]
    evens = [0,2,4,6,8,10]
    combination = [oddNo + evenNo for oddNo,evenNo in zip(odds, evens)]
    print(combination)
    







def SetsDictionaries():
    #Tuples, defined via (), are faster, must only contain the same variable type.
    setOne = {1,2,3,4,5}
    setTwo = {1,3,5,7,9}
    print(setOne.intersection(setTwo))
    print("\n")
    
    avgavg = 0
    for v1,v2 in zip(setOne, setTwo):
        avg = (v1 + v2) / 2
        avgavg += avg
    avgavg /= len(setOne)
    print(avgavg)
    print("\n")
    
    
    particleOne = {
        "mass":34.2,
        "position":[0,0,0], #integer
        "velocity":[0.,0.,0.] #decimal!!!
    }
    particleOne["spin"] = "0.5"
    print(particleOne)
    print(particleOne["mass"])
    print("\n")
    
    print(particleOne.keys())
    print(particleOne.values())
    print("\n")
          
    for Key,Value in particleOne.items():
        print(str(Key) + " is: " + str(Value))
    print("\n")
    







def Substrings():
    testString = "Rory is a big annoying pleb."
    print(testString)
    epicString = testString[:4] #Characters START-3.
    epicString += testString[9:14] #9th - 13th character, 5 TOTAL!! (1 less than usual)
    epicString += testString[23:] #Characters 23-END.
    print(epicString)
    print(testString[0:len(testString):2]) #STEP 2!!
    
    months = ["January","February","March","April",
          "May","June","July","August",
          "September","October","November","December"]
    print(months[1::2]) #1-end, step 2.
    
    








def Loops():
    #Variales must be pre-defined, and colons must be used!!!
    NumToDivide = 1356
    Divisor = 7
    TempVar = NumToDivide
    while TempVar >= Divisor:
        TempVar -= Divisor  
    print(str(NumToDivide) + " Mod " + str(Divisor) + " = " + str(TempVar))
    print("Control: " & NumToDivide % 7) #// = int divider, % = mod.

    months = ["January","February","March","April",
          "May","June","July","August",
          "September","October","November","December"]
    
    #end=" " is very useful!!
    for m in range(0,len(months)): # 0 to len(months) - 1!!!
        print(months[m], end=" ")
    print()
    for m in months:
        print(m, end=" ")
    print()
    
    for i in range(1,3):
        print(i)
        if i == 1:
            continue
        else:
            break
        print("no")







def NumpyThings():
    x = np.linspace(-7,5,100) #100 evenly spaced numbers from -7 to 5.
    #np.logspace() = np.linespace(), but for logarithmic spacing :D.    
    
    startVal = 0.0
    endVal = 1.0
    stepVal = 0.05
    Values = np.arange(startVal, endVal + stepVal, stepVal)
    print(Values)
    
    
    #Difference between np.array() and regular array?
    list_one = np.arange(0, 100, 5) #Numbers from 0 to 100, step 5 (default start = 0, step = 1)
    list_two = list_one ** 2
    list_two = np.append(list_two, 12) #returns new list! D:
    print(list_two)
    
    #Note: for a numpy list, when assigning b = myList, this is copied byRef!!! To copy byVal use b = myList.copy()
    
    numbers = np.array([0,1,2,3,4,-1,-3,100,-3])
    sortednumbers = np.sort(numbers)
    print(sortednumbers)
    print(np.unique(numbers)) #calculates all of the variables, minus repetitions (note that -3 is still outputted! but only one of them.)
    
    print(np.sum(numbers))
    print(np.mean(numbers))
    #Root Mean Square:
    print(np.sqrt(np.mean(numbers)))
    
    print(np.zeros_like(numbers)) #returns n number of 0s, where n is the length of the input array.
    
    a = np.array([1,2,3,4,5])
    b = np.array([6,7,8,9,10])
    a += b
    print(str(a) + "\n")
    
    
    
    
    #Loading Files with NumPy.
    data = np.loadtxt("data00.txt") #stores data into a matrix.
    print(data)
    #To write to files, use np.savetxt(FileName, data)
    
    
    #Polynomials.
    x = np.linspace(-5,5,100)
    fx = [0.5,-1,0.1,0,-0.4] #Represents polynomial of the form c0 + c1*x + c2*x^2 + ...
    y = poly.polyval(x,fx) #Val: Evaluates all x in the function fx, then returns the result as an array.
    plt.plot(x,y)
    #plt.show()
    
    x = np.array([0,2.2,-1.2,5,3,7,-4,-3.2,6.3,-9.6])
    y = 2*x
    fx = poly.polyfit(x, y, 1) #Fit: Calculates the 'best fit' polynomial that best represents a set of data in the form [x0,x1,x2,...],[y0,y1,y2,...]. Returns polynomials.
    plt.scatter(x, y)
    plt.plot(x, poly.polyval(x,fx), "r") #r = red.
    plt.show()
    
    
    
    #Calculus.
    x = np.linspace(-10,10,100)
    fx = [5, 2, 3]
    y1 = poly.polyval(x, fx)
    
    derivative = poly.polyder(fx)
    y2 = poly.polyval(x, derivative)
    
    integral = poly.polyint(fx) #Automaticlly sets constant of integration C = 0.
    y3 = poly.polyval(x, integral)
    
    plt.ylim(-50, 50)
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.plot(x, y3)
    plt.plot([-10, 10], [0,0])
    plt.legend(["f(x)", "f'(x)", "integral"])
    plt.show()


    
    
    
def Matrices():
    import numpy as np
    #Matrices:
    M = np.array([
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ])
    print(M)
    print(M[0,:]) #1st row.
    print(M[:,2]) #3rd column.
    print(str(M[1,0]) + "\n") #2nd row, 1st column.
    
    row1 = np.arange(5)
    row2 = np.zeros(5)  
    row3 = np.ones(5)
    M = np.array([row1, row2, row3]) #Arranges a set of numbers into a matrix.
    print(M)
    print(str(M.shape) + "\n") #Returns tuple in the form (RowCount, ColumnCount).
    
    print(np.zeros((4,3))) #4x3 Zero Matrix
    print(np.eye(4)) #4x4 Identity Matrix
    dValues = np.arange(4)
    print(np.diag(dValues)) #Diagonal Matrix, containing values in the input array. CAN BE REVERSED (ie: dValues = np.diag(D) converts diagonal matrix into its values).
    print("\n")
    
    
    #Matrix & Vector Algebra.
    import numpy as np
    vector = np.array([0,-1,1])
    vector2 = 3 * vector
    Matrix = np.array([
        [2,1,0],
        [-1,-3,2],
        [0,0,-3]
    ])
    TransposeMatrix = Matrix.T #Transposition of Matrix.
    Dot = np.dot(vector, vector2) #Dot Product.
    Cross = np.cross(vector, vector2) #Cross Product.
    print(Dot, Cross)
    Product = np.dot(Matrix, vector) #Multiplying matrices / vectors together.
    print(str(Product) + "\n")
    
    Normalised = np.linalg.norm(Matrix) #Normalised form of matrix (also for calculating length of vector).
    Det = np.linalg.det(Matrix) #Determinant of matrix.
    Trace = np.trace(Matrix) #Sum of leading diagonal elements.
    outprod = np.outer(Matrix, vector) #Outer Product of two matrices - forms new, longer matrix by multiplying a given element of Matrix by each element in Vector to form a new row.
    print(Matrix, vector)
    print(str(outprod) + "\n")
    Inverse = np.linalg.inv(Matrix) #Calculates inverse of matrix.
    print(str(Inverse) + "\n")
    
    Eigenvalues = np.linalg.eigvals(Matrix) #Calculates eigenvalues of matrix.
    Eigenvalues, Eigenvectors = np.linalg.eig(Matrix) #Calculates eigenvalues AND eigenvectors of matrix (tuples).
    for e, ev in zip(Eigenvalues, Eigenvectors):
        print(e, ev)
    
    #Soling Linear Algebra equations in the form Ax=b:
    A = np.array([
    [1,1],
    [1,-1]
    ])
    b = np.array([1,2])
    x = np.linalg.solve(A,b)
    print(x) #(where x is the vector [x1,x2], stored as a tuple).
    
    x0 = np.linspace(-2,2,100)
    y0 = np.linspace(-2,2,100)
    x,y = np.meshgrid(x0,y0) #Produces a matrix, containing the set of coordinates [x,y], in matrix form.
    
    
    
        
    






def Casting():
    print(type("Hello!"))
    a = 2.124
    if type(a) == float:
        print("tis float")
    
    #Casting - list(), dict(), tuple(), set()
    myList = list("Hello World!")
    print(myList)
    print(set(myList))
    
    XCoor = ["A", "B", "C", "D"]
    YCoor = [1, 2, 3, 4]
    Coordinates = dict(zip(XCoor, YCoor))
    print(Coordinates)
    
    
def PrintCommands():
    #{} used as placeholder. Uses 'String'.format() operation.
    print("This is an epic {:s} fruit thing.".format("Orange"))   
    #{:s} = String, {:d} = Integer, {:f} = FLoat, {:e} = Scientific.
    
    #Extra formatting.
    print("Test: {:6d} End.".format(23)) #integer, of width 6 (left pad) - padding character = " ".
    print("Test: {:06d} End.".format(23)) #integer, of width 6 (left pad) - padding character = 0.
    
    print("Test: {:10f} End.".format(np.pi)) #float, of width 10 (left pad) - padding character = " ".
    print("Test: {:010f} End.".format(np.pi)) #float, of width 10 (left pad) - padding character = 0.
    print("Test: {:10.3f} End.".format(np.pi)) #float, of width 10 (left pad - character: " "), 3 dp.
    print("Test: {:010.5f} End.".format(np.pi)) #float, of width 10 (left pad - character: 0), 5 dp.
    
    #Multi-variable formatting.
    print("This is an epic {:s} {:s} thing.".format("Orange", "Fruit?"))   
    
    
def Files():
    #Reading file. r = read-only, w = write, a = append.
    File = open("testfile.txt", "r")
    FirstLine = File.readline()
    
    FileData = File.readlines()
    FormattedList = []
    
    for Data in FileData:
        FormattedData = Data.split() #Split command separates a string into a list of words (" " is splitting character).
        print(FormattedData)
        FormattedList.append([float(d) for d in FormattedData]) #Can be replaced with int(), str(), float().
    
    File.close()
    print(FormattedList)
    
    File = open("testfile.txt", "a")
    File.write("0.00000    0.00001\n") #Note: \n IS REQUIRED WHEN WRITING TO FILES for carriage return!!!! 
    File.close()
    
    with open("testfile.txt", "a") as File:
        File.write("0.00002    0.00003\n")
    #Closes automatically.




def MatplotlibThings():
    #Plotting Functions.
    x = np.linspace(0, 2*np.pi, 100)
    y1 = np.sin(-0.5*x ** 2)
    y2 = np.cos(-0.5*x ** 2)
    plt.plot(x,y1) #Plot = Line Graph.
    plt.plot(x,y2)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Intro Graph :D")
    plt.legend(["sin", "cos"]) #Adds labels to graphs.
    plt.show()
    
    #Plotting Scatter Graphs.
    x = np.array([0,2.2,-1.2,5,3,7,-4,-3.2,6.3,-9.6])
    y1 = np.cos(x)
    y2 = np.sqrt(x)
    plt.scatter(x,y1, s=[10]) #Scatter = Scatter Graph. s=[10] refers to the scale of each dot ([10] for all dots, [1, 2, 6, 3] for individual dots).
    plt.scatter(x,y2)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend(["Set 1", "Set 2"]) #Adds labels to graphs.
    plt.show()
    
    #Plotting Bar Charts.
    Fruits = ["apple","pear","orange"]
    Quantity = [10,20,5]
    plt.bar(Fruits,Quantity)
    plt.xlabel("Fruit Types")
    plt.ylabel("Quantity")
    plt.show()
    
    #Customising Plots:
    #colours: ["b","g","r","c","m","y","k","w"] (blue,green,red,cyan,magenta,yellow,black,white).  DENOTED 'c'.
    #line styles: ["-","--",":","-."] (solid,dashed,dotted,dash-dot).                              DENOTED 'ls'.
    #marker styles: ["o","+","s","v","^","*","x"]                                                  DENOTED 'marker'.
    #Built-in Legend (useful for subplots, where legend cannot be defined).                        DENOTED 'label'.
    x = np.linspace(-5,5,100)
    fx = [0.5,-1,0.1,0,-0.4] #Represents polynomial of the form c0 + c1*x + c2*x^2 + ...
    y = poly.polyval(x,fx) #Val: Evaluates all x in the function fx, then returns the result as an array.
    plt.plot(x,y, c="b", ls=":", marker="o")
    plt.errorbar(x,y, xerr = 0.5, yerr = np.sqrt(x)) #ERROR BARS!!!!!!!
    plt.show()
    
    #Setting Limits on plots:
    plt.xlim([10,20]) #Range of x values.
    plt.ylim([-5,100]) #Range of y values.
    plt.semilogx() #x-axis converted to logarithmic form.
    plt.semilogy() #y-axis converted to logarithmic form.
    plt.loglog() #Both axis converted to logarithmic form.
    
    
    
    plt.clf()
    #Heatmaps - images where each pixel is determined via a specific value.
    A = np.eye(10) #identity matrix of size 10x10.
    plt.imshow(A) #imshow = heatmap config. 1=Yellow, 0 = Purple.
    plt.show()
    
    #"entent"=[xmin,xmax, ymin,ymax] can be used to specify x-y range.
    
    
    



def f(x):
    polynomial = np.array([ 0, 0,  1.95119048e+00, 0, -2.84226190e-01, 0,  1.16071429e-02])
    return poly.polyval(x,polynomial)
def rosenbrock(x,y):
    return (1 - x)**2 + 100*(y - x**2)**2

def func(x, a, b, c):
    polynomial = np.array([a,b,c])
    return poly.polyval(x,polynomial)
def Buckingham(x):
    return 3895*np.exp(-3.146*x) - 395.8/x**6

def ScipyFunctions():
    from scipy.optimize import minimize #Solves numerical problems (eg: non-linear equations), data processing, etc.
    
    #Finding Global Minima / Maxima.
    min_1 = minimize(f,x0=-4)
    min_2 = minimize(f,x0=2)
    min_3 = minimize(f,x0=3) #optional parameter jac=df/dx, to use gradient function in optimising result.
    
    print(min)
    x = np.linspace(-4,4)
    plt.plot(x,f(x))
    plt.scatter(min_1["x"],min_1["fun"],color="r")
    plt.scatter(min_2["x"],min_2["fun"],color="r")
    plt.scatter(min_3["x"],min_3["fun"],color="r")
    plt.show()
    
    x0 = np.linspace(-2,2,100)
    y0 = np.linspace(-2,2,100)
    r = np.array([[rosenbrock(x,y) for x in x0] for y in y0])

    from matplotlib.colors import LogNorm
    plt.imshow(r,origin="lower",cmap="hot",extent=(x0.min(),x0.max(),y0.min(),y0.max()),norm=LogNorm(vmin=1e-6, vmax=1e4))
    plt.colorbar()
    plt.show()
    
    
    #Fitting data to a curve.
    from scipy.optimize import curve_fit
    x = np.linspace(0,20,10)
    y0 = func(x, 2.3, 4.6, -0.2)
    plt.plot(x,y0,color="g")
    
    y = np.array([2.3, 11.5, 18.8, 24.1, 27.4, 28.7, 28.1, 25.5, 20.9, 14.3])
    plt.scatter(x,y, color="b")
      
    p,_ = curve_fit(func,x,y) #only interested in the first variable, so set 2nd variable to blank. p = set of parameters of func (apart from x, ofc).
    print(p)
    
    x0 = np.linspace(0,20,100)
    plt.plot(x0,func(x0, *p),color="r") #where p is the set of parameters. We use *p rather than p to break up all the elements of p into a single variable (separated by spaces, so that the function can understand it).
    
    plt.show()
    
    
    
    #Finding roots of equation.
    from scipy.optimize import root
    x0 = 2.75
    rootValue = (root(Buckingham, x0))["x"]
    print("root is at x=" + str(rootValue))
    
    x = np.linspace(1.45,10,500)
    plt.plot(x,Buckingham(x))
    
    plt.plot(x,np.zeros_like(x),"k--") #dotted line representing the y=0 line.
    plt.scatter(x0, Buckingham(x0), color="r")
    plt.scatter(rootValue, Buckingham(rootValue), color="g")
    
    plt.xlabel("x")
    plt.ylabel("V(x)")
    plt.show()
    
    



def RandomDistributions():
    #Integrated random numbers:
    myArray = ["A","B","C","D","E","F","G"]
    RND = random.random() #Returns random float in the range [0,1).
    print(RND)
    RND = random.randint(1,6) #Returns random integer in the range [1,6].
    print(RND)
    RND = random.choice(myArray) #Returns random member from an array.
    print(RND)
    
    print()
    
    #Numpy random numbers:
    RNDGen = np.random.default_rng() #optional parameter for a fixed seed.
    RND = RNDGen.random(size=10) #Returns 10 random float in the range [0,1). If the "size" attribute is given, all numbers stored in an array.
    print(RND)
    RND = RNDGen.integers(1, 6, size=10)  #Returns 10 random integer in the range [1,6).
    print(RND)
    RND = RNDGen.choice(myArray, size=2, replace=False) #Returns random member from an array. "replace" attribute specifies whether duplicate choices aer allowed or not.
    print(RND)
    
    print()
    
    #Distributions & histogram plotting.
        #Binomial: RNDGen.binomial(n, p, Size=?)
        #Normal: RNDGen.normal(Mean, SD, Size=?)
        #Poisson: RNDGen.poisson(lambda, Size=?)
    
    MEAN = 0.0
    SD = 1.0
    ITERATIONS = 500000
    RNDGen = np.random.default_rng() #optional parameter for a fixed seed.
    p = RNDGen.normal(MEAN, SD, size=ITERATIONS) #Standard normal distribution, with mean of 0, standard deviation of 1. 10 samples generated.
    Count,Edges = np.histogram(p, bins=50, density=True) #"bins" represents how many 'bands' of x-coordinates there are (ie: categories), density scales between 0-1.
    #Count = number of p values in each band,   Edges = x-bounds of each bin.
    
    x = (Edges[1:] + Edges[:-1]) / 2 # finds the centre of each of the bins, to act as x-coordinates.
    plt.plot(x, np.exp(-1/2*x**2) / np.sqrt(2*np.pi)) #Plots reference curve, of mathematical normal curve.
    plt.plot(x,Count) #Plots the histogram.
    plt.legend(["Reference","RND"])
    plt.show()


    #Can implement rejection sampling (ergo, accept-reject algorithm), where we generate two random numbers: x in the domain of interest, and u in the interval (0,1).
    #We then accept x if P(x) > u, and reject it otherwise.    #not sure why this works, but it's pretty cool I think haha#.
    
    #calculating mean, variance, etc.
    x = RNDGen.random(size=1000)
    mean = np.mean(x)
    var = np.var(x)
    print(mean, var)








def NumericalMethods():
    #Numerical Differentiation.
    #Notes: if we have an array of f values, and an array of corresponding x values, if those x values are at a constant interval then we can use
    #first principles to differentiate it (or, better yet, use an average of x+dx & x-dx). If not, we use the concept of Taylor expansions:
    #f(x+dx) = f(x) + df/dx|x * dx + ...
    
    x = np.linspace(0, 2*np.pi, 500)
    f = np.sin(x)
    df = np.gradient(f,x) #Evaluates all points. Calculates df/dx evaluated at each value in x. Doesn't matter whether points are equally spaced or not.
                          #Note: if you know the interval size beforehand, you can replace x with 0.005, for example. 0.005 = dx.
    
    plt.plot(x,f)
    plt.plot(x,df)
    plt.legend(["f(x)", "f'(x)"])
    plt.show()
    
    
    #Numerical Integration:
    #Notes: trapezoidal rule is often used (instead of limit, use sum: sigma { f(x[i]) - f(x[i-1]) / 2  * dx }. Replace dx with (x[i]) - x[i-1])
    #for when interval size is not constant).
    
    int_f = np.trapz(f, x) #Integrates the curve f, then evaluates using the bounds set by x (ie: [x(-1) x(0)] ∫ f dx).
                           #Again, if the interval size is known, x --> 0.005, for example. 0.005 = dx.
    actual = -np.cos(2*np.pi) - -np.cos(0)
    print(int_f, actual)
    
    
    
    #Masks:
    #Bitwise operators: & == AND, | == OR, ^ == XOR, ~ == NOT, << = Left Shift, >> = Right Shift.
    x = np.linspace(0, 10, 20)
    mask = ~ (( 3 < x ) & (x < 8)) #Returns an array of size x of booleans, where each entry is set to either True / False, depending on whether this
                               #entry matches the mask or not. Computing x[mask], or x[boolArray()] returns only the elements in x,
                               #whose corresponding element in mask is set to true.
    print(mask)
    print(x[mask]) #Returns all the numbers in x in the range x < 3, and x > 8.
    print()
    
    #This is very useful for when calculating the integration bounds via int_f. For example.
    x = np.linspace(-5, 5, 10000) #need a lot of points!!!
    fx = np.exp(x)
    
    mask = (x >= 0) & (x <= 3)
    x_mask = x[mask]
    fx_mask = fx[mask] #Computes all values of fx, whose x values are in the range 0<=x<=3. This allows us to calculate e^3 - e^0 via integration bounds.
    int_fx = np.trapz(fx_mask, x_mask)
    actual = np.exp(3) - 1
    print(int_fx, actual)
    
    
    
    #Interpolation:
    #Given an array of f values, and an array of corresponding x values, we estimate f(x[i]), where x[i] is not in x.
    #Whilst we could use techniques such as polyfit, or scipy optimise stuff, interpolation preserves the function values at the data point :D.
    x = np.linspace(-5, 5, 10)
    fx = x ** 2 - 3
    xPointToPredict = 0.75
    interp = np.interp(xPointToPredict, x, fx)
    
    plt.plot(x, fx, color="r")
    plt.scatter(xPointToPredict, interp, color="b")
    plt.plot(np.linspace(-5, 5, 100), np.zeros(100), ls="--", color="k")
    plt.show()
    
    #Cubic Splines - produces a polynomial in the form s(x), that can then be evaluated at any point - allows for differentiation, numerical methods, etc etc.
    from scipy.interpolate import CubicSpline
    interp = CubicSpline(x, fx)
    plt.scatter(x, fx, color="r")
    x2 = np.linspace(-5, 5, 50)
    plt.plot(x2, interp(x2))
    plt.plot(np.linspace(-5, 5, 100), np.zeros(100), ls="--", color="k")
    plt.show()
    
    
    
    








#~~~~~Main~~~~~
import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly
import random

#~~Functions~~

#General_Info()
#ListsTuples()
#SetsDictionaries()
#Substrings()
#Loops()
#NumpyThings()
#Matrices()
#Casting()
#PrintCommands()
#Files()
#MatplotlibThings()
#ScipyFunctions()
RandomDistributions()
#NumericalMethods()
# ~~~~~~~~~~ VSCODE THEMES ~~~~~~~~~~
#    Dark Themes:
#  1) Moonlight Italic
#  2) Ayu Mirage
#  3) GitHub Dark Dimmed
#  4) Noctis Azureus
#  5) Beautiful Dracula Darker
#
#    Light Themes:
#  1) Noctis Lux
#  2) Ayu Light
#
#  Visual Studio Theme: Zero LCH SB 1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Comment Colouring:
#* wow look green this is so cool.
#! AHHHHHHH I DID SOMETHING WRONG!
#? hmmmm did i do something wrong?
#TODO get better at coding.
#NOTE beep TODO boop XXX hi BUG stefan FIXME :D HACK.


#Common Imports:
import numpy as np
import numpy.random as RND

# import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt

import scipy as sp
# from scipy.optimize import curve_fit
# from scipy.signal import find_peaks
# from scipy.optimize import minimize
# from scipy.optimize import root
# from scipy.integrate import quad
# from scipy.integrate import solve_ivp
# from scipy.optimize import root_scalar

import time
from multiprocessing import Pool, cpu_count
# import random




def General_Shenanigans():
    #*args denotes parameters for func, kwargs denotes parameters that have a default assigned value!! Eg: func(x, b=5) has args=x, kwargs=b.
    
    #Error detection.
    TestValue = 3
    if TestValue % 2 == 0:
        raise ValueError("Value is Incorrect.")
        #or, alternatively...
        raise AssertionError("bad")

    #Testing that functions give specific values.
    assert (1 + 3) == 4
    
    #Try-Catch.
    try:
        x = np.sqrt(-3)
    except:
        x = "lol nope"
    print(x)
    
    #np.argmax() returns the index of the largest element in an array; np.max() (or just max()) returns the largest element.
    myArr = np.array([[1,4,3,5], [7,2,1,4]])
    print(max(myArr[0]))
    print(np.max(myArr))
    print(np.max(myArr,axis=1)) #axis=0 return max along rows, axis=1 returns max along columns 9as arrays).
    print(np.argmax(myArr))
    
    wordlist = ["this", "is", "a", "list", "of", "words"]*50
    longstring = "".join(wordlist) # can put anything in the "". This is very speedy :)
    print(longstring)

        
    
    
    
def ListsArraysMatrices():
    #Returning values in array based on function.
    TestArray = np.arange(2,10)
    evens = np.where(TestArray % 2 == 0)[0]  #must specify [0]!!!!!! Returns the indices inside TestArray that follows this rule.
    print(TestArray, evens[0])
    
    #Testing values in array based on function.
    #Eg: Test that all values in an array are > 0:
    TestArray = np.array([3, -4, 1, 5, 0])
    print(np.all(TestArray > 0))
    
    #Finding the indeces of non-zero elements in an array.
    myArray = [1,2,0,0,4,0]
    nz = np.nonzero(myArray)
    print(nz[0]) #must specify [0]!!!!!!
    print("\n")
    
    #Re-shaping arrays to make matrices.
    LineArray = np.arange(16)
    M = LineArray.reshape(4,4)
    print(LineArray)
    print(str(M) + "\n")
    
    #Target specific rows / columns of matrix.
    M = np.arange(16).reshape(4,4)
    row_one = M[0]
    row_two_three = M[[1, 2]]
    column_two = M[:,1]
    column_three_four = M[:,[2, 3]]
    print(row_one)
    print(row_two_three)
    print(column_two)
    print(str(column_three_four) + "\n")
    #More advanced: making all everything but the border of a matrix = 0 (manipulating specific rows & columns of a matrix).
    M = np.ones((6, 6))
    M[1:-1, 2:-2] = 0 #Means target rows elements from index 1 (inclusive) to end (exclusive!! Inclusive would be '1:').
    #Does a similar thing with columns, this time targetting columns 3 to 3rd from end.
    print(str(M) + "\n")
    
    
    #Joining Arrays together:
    ArrayOne = np.arange(4).reshape(2,2)
    ArrayTwo = ArrayOne.copy()
    JoinedArray = np.concatenate((ArrayOne, ArrayTwo))
    print(JoinedArray)
    
    #np.diag turns either a vector into a diagonal matrix (containing the elements in a vector), or turns a matrix into a vector containing the diagonal elements of that matrix!
    #Ie: np.diag is reversible!!! Can be given a vector & a matrix.
    v1 = np.array([1, 6, 3])
    v2 = np.array([2, 3, 9])
    M = np.array([
        [1,2,3],
        [4,5,6],
        [7,8,9]        
    ])
    print(np.diag(v1))
    print(np.diag(M))
    
    #Multiplying vectors:
    v1v2 = np.dot(np.diag(v1), v2)
    v1v2 = v1 * v2
    print("v1v2 = " + str(v1v2))
    


def GaussianDistribution(x, mu=0.0, sigma=1.0, scale=1.0, delta=0.0, normalise=False):
    Gauss = (scale / (sigma * np.sqrt(2 * np.pi)))  *  np.exp(-0.5 * ((x - mu) / sigma)**2)
    return ((delta + (Gauss / np.sum(Gauss))) if normalise else delta + Gauss)
def GaussianDistribution_2D(x, y, mu=0.0, sigma=1.0, scale=1.0, delta=0.0, normalise=False):
    Gauss = (scale / (sigma**2 * 2 * np.pi))  *  np.exp(-((x - mu)**2 + (y - mu)**2) / (2 * sigma**2))
    return ((delta + (Gauss / np.sum(Gauss))) if normalise else delta + Gauss)



def pltPlot():
    #Generating Mesh Values & Displaying as a grid.
    #Eg: Plotting Normalised 2D Gaussian Values.
    NoOfMeshPoints = 20
    x, y = np.meshgrid(np.linspace(-1, 1, NoOfMeshPoints), np.linspace(-1, 1, NoOfMeshPoints))
    Gauss = GaussianDistribution(x, y)
    Gauss_Normalised = Gauss / np.sum(Gauss)
    plt.pcolor(x, y, Gauss_Normalised)
    plt.show()
    
    #Subplots.
    fig, axes = plt.subplots(2, 3) #2 rows, 3 columns. Each plot can then be targetted via axes[row, column].
    x = np.linspace(-10.0, 10.0, 1000)
    y = np.sinc(x)
    axis = axes[1,2] #row 2, column 3
    axis.plot(x, y)
    axis.set_title('Sub-Graph :)')
    axis.set_xlabel('x')
    axis.set_ylabel('y(x)')
    fig.tight_layout()
    plt.show()
    
    #Contour plots.
    x, y = np.meshgrid(np.linspace(0, 4*np.pi, 100), np.linspace(0, 4*np.pi, 100))
    f = np.cos(x) + np.cos(y)
    levels = np.linspace(-1, 1, 8) #Defines levels of contours.
    plt.contourf(x, y, f, levels=levels) #plt.contour & plt.contourf are alike, however f colours in between levels :).
    plt.show()
    
    #3D Graphs.
    x = np.random.random(100)
    y = np.random.random(100)
    z = np.random.random(100)
    fig = plt.figure()
    axis = fig.add_subplot(projection='3d')
    axis.scatter(x, y, z) #Other types available: plot_wireframe, and plot_surface.
    plt.show()
    
    #3D Graphs with sub-plots (demo).
    x, y = np.meshgrid(np.linspace(-3, 3, 400), np.linspace(-3, 3, 400))
    f = np.exp(- (x**2 + y**2) )
    fig, ax = plt.subplots(1, 2, subplot_kw={'projection':'3d'})
    ax[0].plot_wireframe(x, y, f, rstride=20, cstride=20) #rstride & cstride row & column step size to splice, when building the graph (big = smoother).
    ax[1].plot_surface(x, y, f)
    fig.tight_layout()
    plt.show()
    
    #Plotting real data as a histogram to plt.plot.
    #Random data based on normal distribution.
    RNDGen = np.random.default_rng() #optional parameter for a fixed seed.
    DistributionData = RNDGen.normal(0, 1.0, size=10000)
    values, bins, _ = plt.hist(DistributionData, 100) #plots data as a histogram, using 100 bins.
    #Uses the midpoint of each bin to act as x data. We then fit a Gaussian curve to this data, to verify our DistributionData.
    diff = bins[1] - bins[0]
    BinMidpoint = np.array( [(bins[0] + 0.5*diff + (i * diff)) for i in range(len(bins) - 1)] )
    #Use curve_fit to guess the optimal parameters of GaussianDistribution that match: values = GD(BinMidpoints, ...).
    p, error = sp.optimize.curve_fit(GaussianDistribution, BinMidpoint, values) #If needed, the p0=(a, b, c) can be used as initial parameter guesses.
    print(p, error)
    #Plots this data. Note that *array automatically puts the parameters of array into GaussianDistribution.
    plt.plot(BinMidpoint, GaussianDistribution(BinMidpoint, *p))
    plt.show()
    
    
    
    
def Calculus():
    #Integrating e^-x^2 from 0 to infinity. Typically, we use sp.integrate.quad for single integrals, sp.integrate.dblquad for double integrals, etc.
    def f(x):
        return np.exp(-x*x)
    integral, error = sp.integrate.quad(f, 0, np.inf)
    print(integral)
    #Note that we can also use the faster np.trapz, however this does not work for indefinite integrals (we typically use this for simple, continuous, and definite integrals).
    #SCIPY QUAD INTEGRATION TIPS:
    #For functions of multiple variables g(x, a, b, c) we can add args=(a, b, c) to quad).
    #For functions with undefined values, add points=[0] to quad).
    
    #Differentiation using scipy:
    derivative = sp.misc.derivative(f, 1, 0.01, 2) #Uses central difference limit, of dx, to compute the nth derivative at x=1 (note that dx must be set very small to give accurate results).
    print(derivative)




def ConvolutionAndFiltering():
    #Convolve function 'blurrs' between two arrays of length N. This is often used to smooth peaks.
    '''
    •Intuitively, consider two functions f & g. g → g(-x) to flip horizontally, then we move g across the x
    axis towards f. Then, at each x point, convolve(f, g) = the shared area between f & g. Wiki has a good diagram:
    •https://en.wikipedia.org/wiki/Convolution#Visual_explanation
    ◦Mathematically, this is written (f * g)(t) := [∞, -∞] ∫ f(u) * g(t - u) du.
    ◦For discrete data, y[n] = (f * g)[n] := [k from -∞ to ∞] Σ f(k) * g(n - k).
    •This links to Fourier Transforms quite nicely - if y(t) = (f * g)(t), then ^y(ω) = ^f(ω) * ^g(ω).
    '''
    x = np.linspace(-10, 10, 100)
    Peak = np.array([(1 if i==(len(x)/2) else 0) for i in range(len(x))])
    Gauss = GaussianDistribution(x, sigma=3, normalise=True) #Note that we need to normalise Gauss here to give the two
    #arrays the same area - convolve averages the values of the 2 arrays; by normalising we ensure that no scaling occurs.
    ConvolvedPeak = sp.signal.convolve(Peak, Gauss, mode="same") #Blurs between the two arrays. We use the mode 'same' to ensure that
    #the input arrays & the output arrays have the same length. Note that we can also multiply Gauss by some constant to reduce smoothing:
    ConvolvedWeak = sp.signal.convolve(Peak, 20 * Gauss, mode="same")
    plt.plot(x, Peak, label="Peak")
    plt.plot(x, Gauss / max(Gauss), label="Gaussian") #Divide by max(Gauss) for displaying purposes.
    plt.plot(x, ConvolvedPeak, label="Blurred Gaussian (Normal)")
    plt.plot(x, ConvolvedWeak, label="Blurred Gaussian (Weak)")    
    plt.legend()
    plt.show()
 
 
 
    #Filtering:
    '''
    •The standard filtering method uses 'filter coefficients', which define the filtering. The general technique is similar to convolution techniques:
    •Written formally, y[n] = [0 to M] Σ a[i]*x[x-i] + [1 to M] Σ b[i]*y[x-i]     (there are also other types, such as moving average, etc).
    •This is a recursive approach. There are many 'frequency filters' we can add here: low-pass, high-pass, etc.
    ◦Eg: A low-pass filter lets low frequencies pass as normal, but frequencies higher than some cutoff value f[c] are removed.
    ◦Note that this is not just as simple as setting all these frequencies to 0 (ie: sharp cutoff), as this interferes with the signal's domain & stops you from being able to Fourier Transform.
    ◦Hence, this approach gives a smooth transition.
    ◦Eg: low-pass filter has a[0] = 1 - f[c], b[1] = f[c], where f[c] = exp(-2π * f[cut]/f[nyguist]).
    ◦Eg: high-pass filter has a[0] = 1 - f[c], b[1] = f[c], where f[c] = exp(-2π * f[cut]/f[nyguist]).
    
    •Some physical interpretation: let's say we have a big pulse in time (such as a gravitational wave), that has a lot of noise as it had to travel a long way.
     Then, via the Fourier Transform, we know that a big pulse corresponds to lots of sin waves of high frequencies (N needs big to get sharp peak).
     Also, note that noise is just quickly modulating amplitude to the original wave. This is quite important to note:
     *** FREQUENCY CAN BE DEFINED AS THE ABILITY FOR A WAVE'S AMPLITUDE TO MODULATE QUICKLY ***
     So by applying a low-pass filter, we remove the fast-modulating parts of this sound (reducing the noise, and also smoothing the peak).
     Mathematically, as filtering contains convolution, which has links to the Fourier Transform, we are very easily able to reduce high frequencies in k space.
    '''
    def filter(x, a, b):
        convolvedata = np.flip(x,0)
        output = [a[0] * x[0]] # y[0]
        for n in range(1, len(x)):
            if n+1 <= len(a): # border case 1
                term1 = np.sum(a[:n+1] * convolvedata[-n-1:])
            else:
                term1 = np.sum(a * convolvedata[-n-1:-n-1+len(a)])
            if (n-len(b)) < 0: # border case 2
                term2 = np.sum(b[:n] * output[:n])
            else:
                term2 = np.sum(b * output[:len(b)])
            output.insert(0, term1 + term2) # prepend to list
        return np.flip(np.array(output), 0) # normal order
    def pulse(length, amplitude, risetime, decaytime):
        time = np.linspace(0, length, length + 1)
        onset = 0.3 * length # start 30% into the length
        pulse = np.exp(-(time - onset) / risetime) - np.exp(-(time - onset) / decaytime)
        pulse[np.where(time < onset)] = 0.0 # not defined before onset time, set 0
        return -amplitude * pulse

    data = pulse(2000, 10.0, 3.0, 300.0)
    noisy = data + 0.4 * 10.0 * np.random.normal(size = len(data))

    fnyq = 1.0 / (2.0 * 1.0) # time steps in units of 1
    frc  = 1.0 / 100.0       # also try 1.0 / 10.0
    fcut = np.exp(-2.0 * np.pi * frc / fnyq)
    acoeff = np.array([1-fcut]) # make the coefficients
    bcoeff = np.array([fcut])   # here the b coefficient
    filtered = filter(noisy, acoeff, bcoeff) # filter with recursive equation

    plt.plot(noisy)
    plt.plot(filtered, 'r-')
    plt.ylabel('amplitude', fontsize = 14)
    plt.xlabel('samples', fontsize = 14)
    plt.show()
    



def MC_Integration_WithPoints(x, y, NPoints):
        #Creates a tight box which bounds the function.
        x_low, x_high = (min(x), max(x))
        y_low, y_high = (min(y), max(y))
        BoxSize = (x_high - x_low) * (y_high - y_low)
        #Finds index in x, s.t we can create random x values.
        x_low_index, x_high_index = (np.where(x == x_low), np.where(x == x_high))
        
        #Creates random X-Y points in the box.
        RNDx = np.random.randint(x_low_index, x_high_index, NPoints)
        RNDy = np.random.uniform(y_low, y_high, NPoints)
        
        #If the point is under the curve of f(x), we label it as 'accepted'.
        #Note that, unlike the example of Distribution Integration, we also consider negative areas.
        PosIndices, NegIndices = (np.where(RNDy > 0)[0], np.where(RNDy < 0)[0])
        AcceptedPointsPositive = PosIndices[RNDy[PosIndices] <= y[RNDx[PosIndices]]]
        AcceptedPointsNegative = NegIndices[y[RNDx[NegIndices]] <= RNDy[NegIndices]]

        Area = BoxSize * ((len(AcceptedPointsPositive) - len(AcceptedPointsNegative)) / NPoints) #Return the proportion of points that are accepted, * the size of the box.
        return (Area, (x[RNDx[AcceptedPointsPositive]], RNDy[AcceptedPointsPositive]), (x[RNDx[AcceptedPointsNegative]], RNDy[AcceptedPointsNegative]))
def MC_Integration(x, y, NPoints):
    return MC_Integration_WithPoints(x, y, NPoints)[0]

def RandomAndMonteCarlo():
    #Note that for all LB, UB values in numpy, the LB is INCLUDED, and the UB is EXCLUDED.
    #Random values via numpy.random.XXX:
    '''
    .random(count) (0-1 decimal).
    .randint(lb, ub, count).
    .rand(n,m) (returns array of n rows, m columns, of random values from 0-1).
    .choice(myArray, count, Replace, p=[...]) (random value in array. If Replace = False, then each chosen item is removed from the array.
                                                p represents the probability attached with each value in myArray).
    .shuffle(myArray) (shuffles an array randomly)
    '''
    #PDF = Probability Distributiuon Function. All have total integral of 1, and are implemented via numpy.random.XXX:
    '''
    .uniform(lb, ub, count)
    .exponential(scale, count) (exponential decay, where scale = 1/λ, for some decay rate λ).
    .uniform(mu, sigma, count) (gaussian distribution)
    .poisson(lam, count) (returns !!integers!! based on the poisson distribution - lam means the expected number of occurances).
    '''
    
    NCount = 5000
    fig, axes = plt.subplots(2, 2)
    axes[0,0].set_title("Uniform Distribution")
    axes[0,0].hist(np.random.uniform(0, 1, NCount), bins=50)
    axes[0,1].set_title("Exponential Distribution")
    axes[0,1].hist(np.random.exponential(2, NCount), bins=50)
    axes[1,0].set_title("Normal Distribution")
    axes[1,0].hist(np.random.normal(0, 1, NCount), bins=50)
    axes[1,1].set_title("Poisson Distribution")
    axes[1,1].hist(np.random.poisson(100, NCount), bins=50) 
    fig.tight_layout()
    plt.show()
    
    #Note that when repeating a simulation many times, we often use RealValue = np.random.gauss(Value, ErrorInMeasuringValue) to get more varied, realistic results.
    
    #Fitting functions to an experiment, containing a noise & signal.
    UB = 40
    signal = np.random.normal(15, 2.1, 420)
    background = np.random.uniform(0, UB, 400)
    ExperimentData = np.concatenate([signal, background]) #When adding signal to a background, we often concatensate the data together (as this will be plotted
    #using a histogram, it doesn't matter that the array of data is weirdly composed.)
    hist, bins = np.histogram(ExperimentData, 40, range=(0, UB))
    bincentres = np.array([(bins[0] + (bins[1]-bins[0])/2 + i * (bins[1]-bins[0])) for i in range(len(bins)-1)])
    initguess = (15, 2, 300, 5)
    #Model curve_fit with Gaussian + uniform, to match experimental data of mass (with some uncertainty), + random noise. VERY IMPORTANT!!
    bestfit, error = sp.optimize.curve_fit(GaussianDistribution, bincentres, hist, p0=initguess)
    plt.hist(ExperimentData, 40)
    plt.plot(GaussianDistribution(bincentres, *bestfit))
    plt.show()    
    
    
    #Using Monte-Carlo to integrate functions (concept of accept-reject). Useful for integrating functions of high-dimensions.
    '''
    Process:
     1) Wrap the object in a 'box' of known size (as tightly as possible).
     2) General random points in this box via the uniform distribution, and accept / reject them if the points are inside / outside the object.
     3) The integral (area, volume, etc) is then = size of box * percentage of points accepted.
    '''
    #Circle example. Define a box of size (2r)*(2r), centred on the circle.
    r = 2
    NPoints = 1000
    RNDx = np.random.uniform(-r, r, NPoints)
    RNDy = np.random.uniform(-r, r, NPoints)
    AcceptedPoints = np.where(RNDx**2 + RNDy**2 <= r**2)[0] #Returns positions inside RNDx that are accepted.
    Area = 4*r*r * (len(AcceptedPoints) / NPoints)
    
    print(str(np.round(Area / np.pi, 3)) + "π.")
    #Beware the CURSE OF DIMENSIONALITY!! :OOOO Basically, as we move into higher and higher dimensions, we need en exponentially increasing number of sample points to capture the same δdistance between two given points (ie: we need 1000 points to represent some cube as points that are all 0.1m apart from one another. For 5D, we need like 75 bjillion. Essentially, as we increase the number of dimensions, the Ntrails must increase by an exponential amount.)

    #This technique is also very useful for sampling from weird PDFs that numpy does not have :(. Imagine we have some probability function f(x) = e^-x² (wow very unique). Then, to 'sample' via this PDF we can bound f in a box, then use the same process of Monte-Carlo integration to sample points inside this box, for some x value. If the uniformly random value of y lies below the curve f(x), then we accept x, and reject it otherwise. This allows us to sample f! :D
    #For a general function...
    def MC_Distribution(x, y, N):
        #Creates a tight box which bounds the function.
        x_low, x_high = (min(x), max(x))
        y_low, y_high = (0, 1) #IMPORTANT NOTE!!!!!!! FOR DISTRIBUTION FUNCTIONS, [0,1] SHOULD ALWAYS BE THE BOUNDS!!!!
        BoxSize = (x_high - x_low) * (y_high - y_low)
        #Finds index in x, s.t we can create random x values.
        x_low_index, x_high_index = (np.where(x == x_low), np.where(x == x_high))
        
        #Creates random X-Y points in the box.
        RNDx = np.random.randint(x_low_index, x_high_index, N)
        RNDy = np.random.uniform(y_low, y_high, N)
        
        #If the point is under the curve of f(x), we label it as 'accepted'.
        AcceptedPoints = np.where(RNDy <= y[RNDx])[0]

        Area = BoxSize * ((len(AcceptedPoints)) / N) #Return the proportion of points that are accepted, * the size of the box.
        return (Area, (x[RNDx[AcceptedPoints]], RNDy[AcceptedPoints]))
    
    x = np.linspace(0, np.pi, 1000)
    y = np.sin(x)
    
    Area, AccPointsPos = MC_Distribution(x, y, 1000)
    print(str(Area) + "\n")
    plt.plot(x,y)
    plt.scatter(AccPointsPos[0], AccPointsPos[1], color="g")
    plt.show()
    
    
    #Integrating via MonteCarlo:
    x = np.linspace(0, np.pi, 10000)
    def f(x):
        return np.sin(x**x)
    N = 5000000
    SPIntegral = sp.integrate.quad(f, 0, np.pi)[0]
    MCIntegral, AccPointsPos, RejPointsPos = MC_Integration_WithPoints(x, f(x), N)
    print("Real Integration: " + str(SPIntegral))
    print("Monte-Carlo Integration: " + str(MCIntegral))
    print("Delta (with " + str(N) + " data points): " + str(round(abs(SPIntegral - MCIntegral), 4)))
    
    plt.plot(x,f(x))
    plt.plot([min(x),max(x)], [0,0], ls="--", color="k")
    plt.scatter(AccPointsPos[0], AccPointsPos[1], color="g", s=1)
    plt.scatter(RejPointsPos[0], RejPointsPos[1], color="r", s=1)
    plt.title("Area under the graph of f(x) = sin(x²)")
    plt.show()
    
    
    x = np.linspace(0, np.pi, 1000)
    y = np.sin(x)
    
    #To turn a given function f(x) into a PDF, we must normalise it!! (Area under curve = 1)
    #Eg: for a histogram...
    hist, bin_edges = np.histogram(y, 30, density=True)
    norm = hist * np.diff(bin_edges) #Normalisation.
    print(np.sum(norm))
    
    #Finding Bespoke Probabilities, given a general PDF, using cumulative sums!
    cumulative = np.cumsum(hist * np.diff(bin_edges)) #Creates Cumulative Probability Function.
    #To plot histograms on plt, we must calculate an array containing the middle values in each bin, - very important!!
    BinMidpoints = np.array([(bin_edges[0] + (bin_edges[1]-bin_edges[0])/2.0 + i * (bin_edges[1]-bin_edges[0])) for i in range(len(bin_edges)-1)])
    plt.plot(BinMidpoints, cumulative)
    
    #Then, to calculate a random value using this PDF, we generate a uniformly random y value, then map this to an x-value via the cumulative sum!!
    RNDy = np.random.uniform(0.0, 1.0)
    idx = (np.where(cumulative >= RNDy)[0])[0] #Finds the first y index that corresponds to that value of RNDy.
    RNDx = BinMidpoints[idx] #Finds the corresponding x value. RNDx then gives the random bespoke probability!
    print(RNDx)
    plt.scatter(RNDx, RNDy, color="r")
    plt.show()
    
    
    
    
def ODEs():
    '''
    •Typical ODE IVP: dN/dt = -λN, given N(t₀) = N₀.
    •Runge-Kutta ~ order of ODE used to approximate y[n+1] ≈ y[n] + k[1], given f(y,t) = dy/dt.
    ◦RK1: Euler's Method: k[1] = Δt * f(y[n],         t[n]).
    ◦RK2:                 k[2] = Δt * f(y[n] + ½k[1], t[n] + ½Δt).
    ....
    ◦We typically use RK4 (good balance).
    
    •Implement via sp.integrate.solve_ivp(function, [LB,UB], IC, t_eval=XXX, args=(XXX,))
    where [LB,UB] relates to time bounds, that contains t₀, IC ~ y(t₀), t_eval = time values to solve over (optional).
    If we don't specify t_eval, solve_ivp will makes its own points, and return them in solve_ivp.t.
    '''
    def Decay(t, y, l):
        return -l * y[0] #Note that solve_ivp can solve systems of ODEs (we will see this later :D). Hence, as y does not
                         #need to be defined when we call solve_ivp, y[0] refers to there only being one ODE to solve.
                         #This is also why IC is given as an array containing 1 value.
    IC = (1000,) #Tuple of ICs. Should this be a numpy array? hmmmmmm.
    ySolve = sp.integrate.solve_ivp(Decay, [0,100], IC, t_eval=np.linspace(0, 100, 51), args=(1.32e-2,))
    print("1st Order ODE results:")
    print(ySolve)
    #This gives an array containing arrays of y values (corresponding with t_eval). In this case, ySolve.y[0] gives us our array
    #(recall that solve_ivp can handle many ODEs).
    plt.scatter(ySolve.t, ySolve.y[0])
    plt.show()
    
    '''
    •To solve 2nd Order ODEs, we split into multiple 1st order ODEs, that can each be solved via solve_ivp:
    ◦eg: d²x/dt² = -kx  ⇒  {dx/dt = v(t)   ,   dv/dt = -kx(t)}. Hence 2 ICs required.
    •Euler's Method then gives: d²y(t)/dt² = f(y, dy/dt, t) becomes {dy/dt = s(t)  ,  ds/dt = f(y,s,t)}
    ◦Then, we feed func the LHS of the two above equations via y: y[0] denotes y(t), y[1] denotes dy/dt.
     And return the RHS of the two above equations (in this case, [y[1], f(y[0], y[1], t)])
    ''' 
    def Pendulum(t, y, g, l, beta, torque, omega):
        dffdtt = -(g / l) * np.sin(y[0])  -  beta * y[1]  +  torque * np.cos(omega*t)
        return np.array([y[1], dffdtt])
    IC = (np.pi/6.0, 0.0) #ICs of y(t), folllowed by dy/dt.
    omega=0.9
    t = np.linspace(0, 20*np.pi/omega, 500)
    ySolve = sp.integrate.solve_ivp(Pendulum, [0,max(t)], IC, t_eval=t, args=(9.81, 10, 0.5, 1.5, omega))
    print("2nd Order ODE results:")
    print(ySolve)
    fig,(axisone, axistwo) = plt.subplots(1,2)
    axisone.plot(ySolve.t, ySolve.y[0])
    axistwo.plot(ySolve.y[0], ySolve.y[1])
    plt.show()
    
    '''
    •For Coupled equations (eg: equations with dx/dt & dθ/dt, each defined in terms of one another), we have:
    ◦y  →  y[0] = x(t),  y[1] = θ(x).
    ◦Then, we return (s1, s2)  →  (dx/dt, dθ/dt).
    •For d²x/dt² & d²θ/dt²:
    ◦y  →  y[0] = x(t),  y[1] = dx(t)/dt,  y[2] = θ(x),  y[3] = dθ(t)/dt.
    ◦Then, we return (s1, ds1/dt, s2, ds2/dt)  →  (y[1], d²x/dt², y[3], d²θ/dt²).
    •This is essentially the same thing as before; its just that we add the θ equations at the end :).    
    '''
    
    
    '''
    •If we have many bodies of motion, we may have to solve many many ODEs simultaneously (this is beyond the reach of sp.solve_ivp).
    •Instead, we use techniques such as the Verlet Algorithm, where we solve ODEs in discrete time steps (eg: Euler's Method):
    ◦x(t + Δt)    = x(t)         +      Δt * x'(t + ½Δt).
    ◦x'(t + Δt)   = x'(t + ½Δt)  +  ½ * Δt * x''(t+Δt).
    ◦x'(t₀ + Δt₀) = x'(t)        +  ½ *      x''(t).    (this denotes the Starter Value!)
    ◦Where x'' is typically given :). Ie: we find some initial time step x'(t₀ + ½Δt₀), then loop through to find x(t+Δt),
     then use this to calculate the next value of x'(t + Δt), then use this to find x(t + 3/2 Δt), etc etc :).
    •This, from a single initial / starting value of x & v, and some acceleration function, builds up the solution for the ODE.
    '''
    def VerletMethod(x0, v0, Nsteps, timestep):
        def acc(x):
            return x * (1.4/2) #x'' = -omega² * x
        x, v = (np.zeros(Nsteps), np.zeros(Nsteps))
        x[0], v[0] = (x0, v0)
        vhalf = v0 + 0.5 * timestep * acc(x)
        for i in range(Nsteps - 1):
            x[i+1] = x[i] + timestep * vhalf
            accelstep = timestep * acc(x[i+1])
            v[i+1] = vhalf + 0.5 * accelstep
            vhalf += accelstep
        return x, v
    #This technique becomes very powerful when calculating many many solutions for particles interacting in some field due to some ODE.
    #(Eg: if 1000 close particles create some gravity field, which exerts a unique force on each particle). We then use the Verlet Method to solve this rather easily :).
    #TODO THIS IS SO INCREDIBLY COOL AND USEFUL FOR PRETTY MUCH ALL PARTICLE SIMULATIONS!!!! Please do some research on this :DDDDDD.
    
    #Final Note on this: these family of ODE solvers are inherantly energy conservators! (Ie: solutions generated adhere perfectly to the conseration of energy).
    #Solve_ivp gets close, but it does not convserve energy. This will be (maybe) very important!    


      
      
def SpeedAndCompiling():
    '''
    General Tips for Speedy Programs:
    •Be space efficient!! Don't make the computer create loads of unnecessary data
     (ie: making a new array of results, then summing to get the final value, is a lot slower than making & summing value as you go).
    •NUMPY!!! Uses vectorisation (written in C - already compiled!)
    •Python is single-threaded - uses something called the Global Interpreter Lock. This is disabled for NumPy :D
     (however, switching this off & on constantly uses time - try not to mix NumPy & Python functions too much - just use NumPy for the crunching).
    •Use Built-In Functions instead of creating your own (bad idea for VB.net, C#, good idea for Python becuase of how badly its written :D).
     (when solving a very well-known / simple problem (eg: intersection between sets), Google if there is a built-in function - there probably is!!).
    •Imports are expensive! 'from scipy.optimize import curve_fit' is much faster than 'import scipy; scipy.optimize.curve_fit(...)'.
    •Python is an interpreted language (vvvv slow). We can often use languages like C++ to do the heavy-lifting, then use python wrappers to link everything together.
    •We use Numba to compile python code: 'from numba import njit ; add the decorator @njit before each function to have it be compiled'.
    ◦Note that Numba code does not understand scipy functions!! (cannot compile) To get around this, we compile the _input_ function that sp accepts,
     then chuck this compiled function into, for example, curve_fit(f, ...).
    '''
    
    #Using Dictionaries insetad of lists. These are great (uses hash tables :O)
    AddressBook = {
        "Alice": "123-456-7890",
        "Charlie": "555-555-5555",
        "Bob": "987-654-3210"
    }
    print(AddressBook["Bob"])
    print("\n")
    
    #We use Profiling to get specific time-stats on some function. For more inforamtion, see Set 5/Profiling Test.ipynb
    
    
    '''
    General Tips for Cleaner Code:
    •Tuples are bloody amazing:   'firstName, lastName, city = "John", "Henry", "Manchester"'
    •f-strings for print(): 'a, b = 5, 6; print(f"Value of a is {a} and value of b is {b}")'.
    '''
    
    #Docstrings. Used to provide some information about a function. This can be accessed! Very useful for decribing functions - use all the time!!
    def addfunc(a, b):
        """This function adds two numbers"""
        return a + b
    print(f"Function Name : {addfunc.__name__}")
    print(f"Function Docstring : {addfunc.__doc__}")
    print("\n")
    
    
    #Decorator functions:
    def timer(func):                    ### Decorator
        def wrapper(*args, **kwargs):   ### Wrapper. *args denotes parameters for func, kwargs denotes parameters that have a default assigned value!! Eg: func(x, b=5) has args=x, kwargs=b.
            start_time = time.time()
            result = func(*args, **kwargs) #Runs the function.
            end_time = time.time()
            print(f"Function {func.__name__} took {end_time - start_time:.2f} seconds to execute")
            return result
        return wrapper
    #Then, by invoking the decorator timer before a function, my_function is automatically passed into the wrapper for timer.
    #This performs the function, but does some things before & after (such as performing diagnostics). This makes code a lot more concise.
    @timer
    def some_func():
        vector = list(range(1000000))
        sumsq=0
        for entry in vector:
            sumsq += entry**2
        return
    some_func()




def MultiIntegrationExample(NPoints):
    x = np.linspace(0, np.pi, 10000)
    y = np.sin(x)
    return MC_Integration(x,y,NPoints)

def MultiProcessing():
    '''
    Multiprocessing:
    •Note that this is slightly weird for Jupyter Notebooks! When implementing multiprocessing in this case, we make a separate file (eg: funcs),
     then in the notebook call "from funcs import some_cool_function".
    •We call a parallel approach 'embarrassingly parallel' if all program instances solve the same problem independently. If threads need to
     communicate, complexities arise. In this module, we ignore the sharing of resources between threads and consider 'embarrassing' problems only.
    •This is very useful for when you want to 'scan' though a set of parameters (ie: different thread for each parameter).
    •For some reason, when I run this in its own .py file it runs like 5x faster?!?! This is weird; I think the more things you import at the
     start of the program, the more that multithreading performance is affected. How strange...
    '''    
    
    if __name__ == '__main__': #!! THIS LINE MUST BE SPECIFIED !! Also, must encapsulate _everything_ (if it does not, the previous lines will be repeated for each thread).
        NIterations = 100_000_000
        
        #Single Thread Example.
        st = time.time()
        AreaSingle = MultiIntegrationExample(NIterations)
        ft = time.time()
        print(f"Single Thread: {ft-st} seconds. Area = {AreaSingle}.")
        
        npu = cpu_count() #Processor Count.
        print(f'You have {npu} cores :O')
        
        #Multi Thread Example.
        st = time.time()
        data_part = [NIterations // npu for _ in range(npu)] #Split Computation equally between npu threads (~62500 each),
        #The values in this array will be passed into MIE (one value for each thread)
        
        with Pool(processes=npu) as pool: #npu threads created.
            count = pool.map(MultiIntegrationExample, data_part) #Feeds each data value into each thread, calls all threads, then waits until all
            #threads have finished. Note that the function (eg: MultiIntegrationExample) must be defined on a GLOBAL LEVEL!!
            #This returns an array of computed values.
        AreaMulti = np.mean(count) #Average over all thead computed values to find the total area.
        ft = time.time()
        print(f"Mutli Thread: {ft-st} seconds. Area = {AreaMulti}.")
        
        from numba import njit, int32, float64, prange
        #We can combine this with a compiling technique such as numba, for some really speedy programs :D.
        #To do this,invoke '@njit(float64(int32), parallel=True)' before a function call, then instead of using:
        #'range(n)' in a for loop, use 'prange(n)'!! This automatically invokes numba's parallel processing.
        #Eg: without @njit(float64(int32), parallel=True) call...
        nIterations = 100_000 #100_000_000
        count = 0 #Again, count must be global, s.t all threads can access it.
        for _ in prange(nIterations): # Note Numba keyword prange for parallel range
            x, y = RND.random(), RND.random()
            r = np.sqrt(pow(x, 2) + pow(y, 2))
            if r < 1:
                count += 1
        print(count)
        #~~~~~ This will be very slow without this call, but it's here for completion anyway :D. ~~~~~
    
    
    
            






#~~~~~Main~~~~~
#General_Info()
#ListsArraysMatrices()
#pltPlot()
#Calculus()
#ConvolutionAndFiltering()
#RandomAndMonteCarlo()
#ODEs()
#SpeedAndCompiling()
MultiProcessing()
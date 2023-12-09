from Shor import *

N = 35

shor = Shor()
results = shor.compute(N)
if isinstance(results, list) or isinstance(results, tuple):
    print_correct("The results are the numbers "+ str(results[0]) + " and " + str(results[1]))
else:
    print_correct("The result is the number: " + str(results))

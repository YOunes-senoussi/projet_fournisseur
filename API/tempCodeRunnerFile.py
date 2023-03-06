def fruits_func():
    fruits = [1, 3, 2, 3, 3, 4, 3, 4]

    f1 = None
    f2 = None
    nbr_f = 0
    max_nbr_f = 0

    nbr_consecutive = 0
    i = 0

    for f in fruits:

        if f == f1:
            nbr_f += 1
            nbr_consecutive = 1

        elif f == f2:
            nbr_f += 1
            nbr_consecutive += 1
        
        elif f1 is None:
            f1 = f
            nbr_f = 1
            nbr_consecutive = 1
        
        elif f2 is None:
            f2 = f
            nbr_f += 1
            nbr_consecutive = 1

        else:
            if nbr_f > max_nbr_f:
                max_nbr_f = nbr_f
            
            f1 = f2
            f2 = f
            nbr_f = nbr_consecutive
            nbr_consecutive = 1

    if nbr_f > max_nbr_f:
        max_nbr_f = nbr_f

    return max_nbr_f

print(fruits_func())
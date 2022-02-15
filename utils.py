def base62_encode(num):
    BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    arr = []
    #appending the array with the character that is at the index of the remainder of the division of num by 62 in the BASE62 string
    # then assigning num the value of the division until num is equal to 0
    while num:
        num,rem = divmod(num,62)
        arr.append(BASE62[rem])
    arr.reverse()
    #converting the array into a string
    return ''.join(arr)
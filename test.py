def quick_sort(data):
    stack = [(0, len(data)-1)]
    result = []
    step = 1
    
    while stack:
        print(f"Adım {step}: {data}")
        step += 1
        
        left, right = stack.pop()
        print(f"\tleft: {left}, right: {right}")
        if right - left < 1:
            continue
        
        pivot = data[right]
        print(f"\tPivot değerimiz: {pivot}")
        i = left
        for j in range(left, right):
            if data[j] < pivot:
                print(f'\t{data[j]} < {pivot} olduğu için yer değiştirmiyoruz: {data}')
                data[i], data[j] = data[j], data[i]
                i += 1
        data[i], data[right] = data[right], data[i]
        print(f"\tYer değiştiriyor {data[i]} with {data[right]}: {data}")
        
        
        print(f"\tEtrafında bölünmüş {pivot}: {data}")
        
        stack.append((left, i-1))
        stack.append((i+1, right))
    
    print(f"Final sorted dataay: {data}")
    return data




my_list = [3, 7, 1, 9, 2, 8, 5, 0, 12, 14,20]
quick_sort(my_list)

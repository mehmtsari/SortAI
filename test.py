def sort_sort(lst):
    for i in range(len(lst)):
        print('döngü başı')
        for j in range(i+1, len(lst)):
            if lst[j] < lst[i]:
                print([lst[i], lst[j]])
                lst[i], lst[j] = lst[j], lst[i]
                print([lst[i], lst[j]])
                print(lst)
                print('\n')
                
    return lst

print(sort_sort([5,2,4,3,1,7]))

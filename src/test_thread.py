import multiprocessing

def f((x,y)):
    print x + y

if __name__ == '__main__':
    core_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(core_count)

    test = [(1,1), (2,2), (3,3)]

    pool.map(f, test)

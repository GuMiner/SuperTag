import gc

def print_free_mem():
    print('Free memory (kB): {}'.format(gc.mem_free() / 1024))
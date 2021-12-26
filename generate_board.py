import os
def main(path, size):
    row = '0,'*size
    if os.path.exists(path):
        os.remove(path)

    for _ in range(size):
        with open(path, 'a') as f:
            f.write(row[:-1]+'\n')

if __name__=='__main__':
    main('./boards/l_test_2.txt', 20)
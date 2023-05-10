""" Some ideas for getting a file name """

def get_name_from_file(fname):
    """ Generate a name from the first line of a file. """
    return open(fname).readline()

def get_name_from_time():
    from datetime import datetime 
    return datetime.now().strftime('%Y%m%d_%H%M%S.fits')

if __name__ == '__main__':
    print(get_name_from_file("1.txt"))
    print(get_name_from_time())
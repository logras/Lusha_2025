import selenium
def main():
    """
    Return pytest version
    """
    selenium_version = selenium.__version__
    return str(selenium_version)

if __name__ == '__main__':
    main()

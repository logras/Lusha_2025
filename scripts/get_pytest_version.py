import pytest

def main():
    """
    Return pytest version
    """
    pytest_version = pytest.__version__
    return str(pytest_version)

if __name__ == '__main__':
    main()

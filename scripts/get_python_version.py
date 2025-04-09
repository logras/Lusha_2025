import sys

def main():
    """
    Return Python version as MAJOR.MINOR
    """
    python_version = sys.version_info
    python_formated_version = f"{python_version.major}.{python_version.minor}"
    return str(python_formated_version)


if __name__ == '__main__':
    main()

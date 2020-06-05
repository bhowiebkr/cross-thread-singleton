from locker import locker


@locker("test locking")
def main():
    print("\nHello World!")

    # raise Exception("testing exceptions.")  # Test that stacktrace work as we expect them to.

    while True:  # keep alive
        pass


if __name__ == "__main__":
    main()

import sys
from .core import whatfile
from .display import print_results


def main():
    args = sys.argv[1:]

    if not args:
        print("usage: whatfile <file> [file...]", file=sys.stderr)
        sys.exit(1)

    results = []
    for path in args:
        try:
            info = whatfile(path)
            results.append(info)
        except FileNotFoundError:
            results.append({"path": path, "error": "file not found"})
        except Exception as e:
            results.append({"path": path, "error": str(e)})

    print_results(results)


if __name__ == "__main__":
    main()

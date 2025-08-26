from modify_contents_recursive import delete_contents_recursive, copy_contents_recursive
from generate_page import generate_pages_recursive
import sys

def main():
    base_path: str = sys.argv[1] if len(sys.argv) > 1 else "/"

    delete_contents_recursive()
    print("Deleted contents of destination directory.")
    copy_contents_recursive()
    print("Copied contents from source to destination directory.")

    generate_pages_recursive(base_path=base_path)
    generate_pages_recursive()
    print("Generated pages recursively from content directory to destination directory.")

if __name__ == "__main__":
    main()
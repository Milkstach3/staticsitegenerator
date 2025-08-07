from modify_contents_recursive import delete_contents_recursive, copy_contents_recursive
from generate_page import generate_pages_recursive

def main():
    delete_contents_recursive()
    print("Deleted contents of destination directory.")
    copy_contents_recursive()
    print("Copied contents from source to destination directory.")

    generate_pages_recursive()
    print("Generated pages recursively from content directory to destination directory.")

if __name__ == "__main__":
    main()
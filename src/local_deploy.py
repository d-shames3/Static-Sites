from site_generator import copy_static, generate_pages_recursive
import os


def main():
    path_to_repo = os.getcwd()
    source = os.path.join(path_to_repo, "static")
    destination = os.path.join(path_to_repo, "public")
    print(source, destination)
    copy_static(source, destination)

    from_directory = os.path.join(path_to_repo, "content")
    template_path = os.path.join(path_to_repo, "template.html")
    dest_directory = os.path.join(path_to_repo, "public")
    generate_pages_recursive(from_directory, template_path, dest_directory)


if __name__ == "__main__":
    main()

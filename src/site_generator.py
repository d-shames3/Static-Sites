import os
import shutil
import pathlib
from block_text import markdown_to_html_node


def copy_static(source, destination):
    if not os.path.exists(source):
        raise Exception("Invalid source directory path")

    if not os.path.exists(destination):
        os.makedirs(destination)

    destination_object_list = os.listdir(destination)
    if destination_object_list:
        shutil.rmtree(destination)
        os.mkdir(destination)

    source_object_list = os.listdir(source)

    for object in source_object_list:
        if os.path.isfile(os.path.join(source, object)):
            file = os.path.join(source, object)
            shutil.copy(file, destination)
        else:
            target_directory = os.path.join(destination, object)
            os.mkdir(target_directory)
            nested_directory = os.path.join(source, object)
            copy_static(nested_directory, target_directory)


def extract_title(markdown):
    line_split = markdown.split("\n")
    heading_list = list(filter(lambda line: line.strip().startswith("# "), line_split))
    if not heading_list:
        raise Exception("Missing heading 1")
    return heading_list[0].strip().replace("# ", "")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as md:
        markdown_file = md.read()

    with open(template_path, "r") as html:
        html_file = html.read()

    html_nodes = markdown_to_html_node(markdown_file)
    html_strings = html_nodes.to_html()
    title = extract_title(markdown_file)

    html_page = html_file.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_strings
    )

    dest_directory = os.path.dirname(dest_path)

    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    with open(dest_path, "w") as file:
        file.write(html_page)


def generate_pages_recursive(from_directory, template_path, dest_directory):
    if not os.path.exists(from_directory):
        raise Exception("Invalid source directory path")

    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    source_object_list = os.listdir(from_directory)

    for object in source_object_list:
        object_path = pathlib.Path(object)
        from_path = os.path.join(from_directory, object)
        dest_path = os.path.join(dest_directory, object)
        if os.path.isfile(from_path):
            if object_path.suffix == ".md":
                dest_object = object_path.with_suffix(".html")
                dest_path = os.path.join(dest_directory, dest_object)
                generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)

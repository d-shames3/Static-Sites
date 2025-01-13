from site_generator import copy_static, generate_pages_recursive

def main():
    source = "/Users/david/projects/boot/github.com/d-shames3/static-sites/static"
    destination = "/Users/david/projects/boot/github.com/d-shames3/static-sites/public"
    copy_static(source, destination)

    from_directory = "/Users/david/projects/boot/github.com/d-shames3/static-sites/content"
    template_path = "/Users/david/projects/boot/github.com/d-shames3/static-sites/template.html"
    dest_directory = "/Users/david/projects/boot/github.com/d-shames3/static-sites/public"
    generate_pages_recursive(from_directory, template_path, dest_directory)

if __name__ == "__main__":
    main()

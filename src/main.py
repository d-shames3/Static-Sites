from textnode import TextType, TextNode
from site_generator import copy_static, generate_page

def main():
    source = "/Users/david/projects/boot/github.com/d-shames3/static-sites/static"
    destination = "/Users/david/projects/boot/github.com/d-shames3/static-sites/public"
    copy_static(source, destination)

    from_path = "/Users/david/projects/boot/github.com/d-shames3/static-sites/content/index.md"
    template_path = "/Users/david/projects/boot/github.com/d-shames3/static-sites/template.html"
    dest_path = "/Users/david/projects/boot/github.com/d-shames3/static-sites/public/index.html"
    generate_page(from_path, template_path, dest_path)

if __name__ == "__main__":
    main()

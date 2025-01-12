from textnode import TextType, TextNode
from site_generator import copy_static

def main():
    tn = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(tn)
    source = "/Users/david/projects/boot/github.com/d-shames3/static-sites/static"
    destination = "/Users/david/projects/boot/github.com/d-shames3/static-sites/public"
    copy_static(source, destination)

if __name__ == "__main__":
    main()
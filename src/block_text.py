def split_block(text):
    split_newline = text.split("\n\n")
    whitespace_stripped = list(map(lambda string: string.strip(), split_newline))

    return whitespace_stripped

def block_to_block_type(markdown_block):
    split_block_lines = markdown_block.split("\n")
    n_rows = len(split_block_lines) + 1
    if "# " in markdown_block[:7]:
        return "heading"
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return "code"
    elif all(line.startswith(">") for line in split_block_lines):
        return "quote"
    elif all((line.startswith("* ") or line.startswith("- ")) for line in split_block_lines):
        return "unordered_list"
    elif [line[:3] for line in split_block_lines] == [f"{i}. " for i in range(1, n_rows )]:
        return "ordered_list"
    else:
        return "paragraph"
    
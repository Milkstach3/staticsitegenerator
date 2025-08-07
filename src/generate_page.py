import os
import pathlib
from markdown_blocks import markdown_to_html_node
from CONSTANTS import DESTINATION_DIR, TEMPLATE_PATH, DESTINATION_FILE, FROM_PATH, CONTENT_DIR
import re


def generate_page(
        from_path: str = FROM_PATH, 
        template_path: str = TEMPLATE_PATH, 
        dest_path: str = DESTINATION_FILE
        ) -> None:
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}") 

    markdown: str = ""
    template: str = ""
    with open(from_path, 'r') as file:
        markdown = file.read()

    with open(template_path, 'r') as file:
        template = file.read()
    
    markdown_html_node = markdown_to_html_node(markdown)
    markdown_html_str = markdown_html_node.to_html()
    title = extract_title(markdown_html_str)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", markdown_html_str)
    
    with open(dest_path, 'w') as file:
        file.write(template)

def extract_title(markdown: str) -> str:
    if '<h1>' not in markdown:
        raise ValueError("Markdown does not contain a title.")
    output: str = re.findall(r'<h1>(.*?)</h1>', markdown)[0]

    return output.replace('<h1>', '').replace('</h1>', '').strip()

def generate_pages_recursive(
        dir_path_content: str = CONTENT_DIR, 
        template_path: str = TEMPLATE_PATH, 
        dest_dir_path: str = DESTINATION_DIR
        ) -> None:
    list_dir: list[str] = os.listdir(dir_path_content)
    # print(f"LIST OF STUFF IN list_dir::::::::{list_dir}")
    for item in list_dir:
        if os.path.isfile(os.path.join(dir_path_content, item)):
            if item.endswith('.md'):
                from_path = os.path.join(dir_path_content, item)
                dest_path = os.path.join(dest_dir_path, item.replace('.md', '.html'))
                # print(f"FROM PATH: {from_path}")
                # print(f"DEST PATH: {dest_path}")
                generate_page(from_path, template_path, dest_path)
        else:
            new_dir_content = os.path.join(dir_path_content, item)
            new_dest_dir = os.path.join(dest_dir_path, item)
            pathlib.Path(new_dest_dir).mkdir(parents=True, exist_ok=True)
            generate_pages_recursive(new_dir_content, template_path, new_dest_dir)
    
    # pathlib.Path
    
# os.listdir
# os.path.join
# os.path.isfile
# pathlib.Path
from node_conversion import markdown_to_html_node
from extract_title import extract_title
import os

def generate_page(from_path, template_path, dest_path):
    print("Generating page from source to destination using provided template")
    with open(from_path) as file:
        source = file.read()
    with open(template_path) as file:
        template = file.read()
    html_node = markdown_to_html_node(source)
    html_string = html_node.to_html()
    title = extract_title(source)
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(final_html)
import os
import shutil
from pathlib import Path
from node_conversion import markdown_to_html_node
from extract_title import extract_title

def copy_static_recursive(src, dst):
    os.makedirs(dst, exist_ok=True)
    items = os.listdir(src)
    for item in items:
        full_path = os.path.join(src, item)
        if os.path.isfile(full_path):
            src_full_path = os.path.join(src, item)
            dst_full_path = os.path.join(dst, item)
            shutil.copy(src_full_path, dst_full_path)

        elif os.path.isdir(full_path):
                src_subdir = os.path.join(src, item)
                dst_subdir = os.path.join(dst, item)
                copy_static_recursive(src_subdir, dst_subdir)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content = os.listdir(dir_path_content)
    dest_dir_path_obj = Path(dest_dir_path)
    content_dir_path_obj = Path(dir_path_content)
    for file_name in content:
        full_content_path = os.path.join(dir_path_content, file_name)
        content_path_obj = Path(full_content_path)
        if os.path.isfile(full_content_path):
            if full_content_path.endswith(".md"):
                with open(full_content_path) as file:
                    source = file.read()
                with open(template_path) as file:
                    template = file.read()
                html_node = markdown_to_html_node(source)
                html_string = html_node.to_html()
                title = extract_title(source)
                final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
                relative_path = content_path_obj.relative_to(content_dir_path_obj)
                html_relative_path = relative_path.with_suffix(".html")
                dest_path = dest_dir_path_obj / html_relative_path
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with open(dest_path, "w") as file:
                    file.write(final_html)  
        if os.path.isdir(full_content_path):
            current_found_dir_path_obj = Path(full_content_path)
            relative_dir_path = current_found_dir_path_obj.relative_to(content_dir_path_obj)
            new_dest_for_recursive_call = dest_dir_path_obj / relative_dir_path
            os.makedirs(new_dest_for_recursive_call, exist_ok=True)
            generate_pages_recursive(full_content_path, template_path, str(new_dest_for_recursive_call))

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_static_recursive("static", "public")
    generate_pages_recursive(
         "content",
         "template.html",
         "public"
    )

if __name__ == "__main__":
    main()


import os
import sys
import shutil
from pathlib import Path
from generate_page import generate_page

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

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    content = os.listdir(dir_path_content)
    dest_dir_path_obj = Path(dest_dir_path)
    content_dir_path_obj = Path(dir_path_content)
    for file_name in content:
        full_content_path = os.path.join(dir_path_content, file_name)
        content_path_obj = Path(full_content_path)
        if os.path.isfile(full_content_path):
            if full_content_path.endswith(".md"):
                relative_path = content_path_obj.relative_to(content_dir_path_obj)
                html_relative_path = relative_path.with_suffix(".html")
                dest_path = dest_dir_path_obj / html_relative_path
                generate_page(basepath, full_content_path, template_path, dest_path)

        if os.path.isdir(full_content_path):
            current_found_dir_path_obj = Path(full_content_path)
            relative_dir_path = current_found_dir_path_obj.relative_to(content_dir_path_obj)
            new_dest_for_recursive_call = dest_dir_path_obj / relative_dir_path
            os.makedirs(new_dest_for_recursive_call, exist_ok=True)
            generate_pages_recursive(basepath, full_content_path, template_path, str(new_dest_for_recursive_call))

def main():
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    copy_static_recursive("static", "docs")
    generate_pages_recursive(
        basepath,
        "content",
        "template.html",
        "docs"
    )

if __name__ == "__main__":
    main()


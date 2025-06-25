import os
import shutil
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

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_static_recursive("static", "public")
    generate_page(
         "content/index.md",
         "template.html",
         "public/index.html"
    )

if __name__ == "__main__":
    main()


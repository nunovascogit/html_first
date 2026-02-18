import os
import shutil
import sys  # Added for sys.argv
from gencontent import generate_pages_recursive

def main():
    # Grab basepath: sys.argv[0] is the script name, sys.argv[1] is the first argument
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # Updated destination to 'docs' for GitHub Pages
    public_path = "./docs"
    static_path = "./static"
    content_path = "./content"
    template_path = "template.html"

    print(f"Cleaning {public_path} directory...")
    prepare_public_dir(public_path)

    print("Copying static files...")
    copy_files_recursive(static_path, public_path)

    print(f"Generating content with basepath '{basepath}'...")
    # Pass the basepath to the generation function
    generate_pages_recursive(content_path, template_path, public_path, basepath)

    print("Build successful!")

def prepare_public_dir(public):
    if os.path.exists(public):
        shutil.rmtree(public)
    os.mkdir(public)

def copy_files_recursive(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            copy_files_recursive(source_path, dest_path)

if __name__ == "__main__":
    main()
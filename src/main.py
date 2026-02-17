import os
import shutil
from gencontent import generate_pages_recursive

def main():
    public_path = "./public"
    static_path = "./static"
    content_path = "./content"
    template_path = "template.html"

    print("Cleaning public directory...")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)

    print("Copying static files...")
    copy_files_recursive(static_path, public_path)

    print("Generating all content pages recursively...")
    generate_pages_recursive(content_path, template_path, public_path)

    print("Build successful!")
  
        

def prepare_public_dir(public):
    if os.path.exists(public):
        # This deletes the folder and EVERYTHING inside it
        shutil.rmtree(public)
    
    # Recreate the empty directory
    os.mkdir(public)

def copy_files_recursive(source_dir, dest_dir):
    # Ensure the destination exists (for subdirectories)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        print(f" * {source_path} -> {dest_path}")
        
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            # Recursive call for subdirectories
            copy_files_recursive(source_path, dest_path)


if __name__ == "__main__":
    main()

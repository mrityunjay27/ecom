import os
import shutil

# Function to copy content of sub-folder to current folder and then delete it.
def copy_and_delete_subfolders(parent_folder):
    # Ensure the provided path is a valid directory
    if not os.path.isdir(parent_folder):
        print(f"{parent_folder} is not a valid directory.")
        return

    # Iterate through each item in the parent folder
    for item in os.listdir(parent_folder):
        item_path = os.path.join(parent_folder, item)

        # Check if the item is a directory
        if os.path.isdir(item_path):
            # Iterate through each item in the subfolder
            for sub_item in os.listdir(item_path):
                sub_item_path = os.path.join(item_path, sub_item)
                # Copy the subfolder content to the parent folder
                shutil.copy(sub_item_path, parent_folder)
                print(f"Copied: {sub_item_path} to {parent_folder}")

            # Delete the subfolder after copying its contents
            shutil.rmtree(item_path)
            print(f"Deleted: {item_path}")


# Example usage:
parent_folder_path = r"C:\Users\ASUS\Downloads\Django\[FreeCoursesOnline.Me] Code With Mosh - The Ultimate Django Series Part 2\2 Building RESTful APIs with Django REST Framework"
copy_and_delete_subfolders(parent_folder_path)

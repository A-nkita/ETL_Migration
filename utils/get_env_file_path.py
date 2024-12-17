import os

def get_path(env, dir='config'):
    try:
        # Get all files in the specified directory that start with the environment name
        filenames = [file for file in os.listdir(dir) if file.startswith(env)]

        # Check if filenames list is not empty and return the first matching file's path
        if filenames:
            return os.path.join(dir, filenames[0])  # Using os.path.join for better path handling
        else:
            print(f"Warning: No files found starting with '{env}' in the '{dir}' directory.")
            return None  # Return None if no matching file is found

    except FileNotFoundError:
        # Handle case where directory does not exist
        print(f"Error: The directory '{dir}' was not found.")
        return None
    except PermissionError:
        # Handle permission errors when accessing the directory
        print(f"Error: Permission denied when accessing the directory '{dir}'.")
        return None
    except Exception as e:
        # General exception handling for any other errors
        print(f"Error: {e}")
        return None
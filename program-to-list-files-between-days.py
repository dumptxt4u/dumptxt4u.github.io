import os
import sys
import datetime
import tempfile
import subprocess

def list_recent_files(directory, start_date=None, end_date=None):
    """
    List files in the given directory that have been modified within the specified time range.
    
    :param directory: Directory to search for files.
    :param start_date: Start date as a datetime object (optional).
    :param end_date: End date as a datetime object (optional).
    :return: List of files modified within the given time range.
    """
    recent_files = []
    
    try:
        for root, dirs, files in os.walk(directory):
            # Exclude hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                # Exclude hidden files
                if file.startswith('.'):
                    continue
                
                file_path = os.path.join(root, file)
                
                # Check if file path exists and get its modification time
                try:
                    file_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    # Check if the file was modified within the given date range
                    if (start_date and file_modified_time < start_date) or (end_date and file_modified_time > end_date):
                        continue
                    
                    recent_files.append(file_path)
                except (FileNotFoundError, PermissionError):
                    print(f"Warning: Cannot access {file_path}. Skipping.")
                    continue

    except PermissionError as e:
        print(f"PermissionError: {e}. Some folders may be inaccessible.")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return recent_files

def create_symlinks_and_open(files):
    """
    Create symbolic links for the given files in a temporary directory and open that directory in Dolphin.
    
    :param files: List of file paths to create symlinks for.
    """
    if files:
        # Create a timestamped temporary directory
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_dir = os.path.join(tempfile.gettempdir(), f"recent_files_{timestamp}")
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # Create symbolic links for each recent file in the temporary directory
            for file_path in files:
                try:
                    symlink_path = os.path.join(temp_dir, os.path.basename(file_path))
                    os.symlink(file_path, symlink_path)
                except Exception as e:
                    print(f"Error creating symlink for {file_path}: {e}")
            
            # Open the temporary directory in Dolphin
            subprocess.run(["dolphin", temp_dir])
            print(f"Dolphin opened with symlinks in {temp_dir}.")
        
        except FileNotFoundError:
            print("Error: Dolphin is not installed or not found in PATH.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No recent files to process.")

def prompt_for_dates():
    """
    Prompts the user to enter start and end dates to filter files by modification time.
    
    :return: start_date, end_date as datetime objects or None if not provided.
    """
    while True:
        try:
            start_date_str = input("Enter start date (YYYY-MM-DD) or leave blank for no start date: ").strip()
            end_date_str = input("Enter end date (YYYY-MM-DD) or leave blank for no end date: ").strip()

            start_date = None
            end_date = None

            if start_date_str:
                start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
            
            if end_date_str:
                end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")

            return start_date, end_date

        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

def display_menu():
    """
    Displays a menu of options for the user to choose from.
    """
    print("Menu Options:")
    print("1. List files modified in the last N minutes.")
    print("2. List files modified between two dates.")
    print("3. Exit.")

def main():
    """
    Main function to display menu and handle user input for file processing.
    """
    directory = input("Enter the directory to search for files: ").strip()

    if not os.path.isdir(directory):
        print(f"Error: The specified directory '{directory}' does not exist or is not accessible.")
        sys.exit(1)

    while True:
        display_menu()

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            # Option 1: Files modified in the last N minutes
            try:
                minutes = int(input("Enter the number of minutes: ").strip())
                files = list_recent_files(directory, minutes=minutes)
                if files:
                    print(f"Files modified in the last {minutes} minutes:")
                    for file in files:
                        print(file)
                    create_symlinks_and_open(files)
                else:
                    print(f"No files found in the last {minutes} minutes in {directory}.")
            except ValueError:
                print("Error: Invalid input. Please enter an integer value for minutes.")

        elif choice == "2":
            # Option 2: Files modified between two dates
            start_date, end_date = prompt_for_dates()
            files = list_recent_files(directory, start_date, end_date)
            if files:
                print(f"Files modified between {start_date} and {end_date}:")
                for file in files:
                    print(file)
                create_symlinks_and_open(files)
            else:
                print(f"No files found between {start_date} and {end_date}.")

        elif choice == "3":
            # Exit the program
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please choose between 1 and 3.")

if __name__ == "__main__":
    main()


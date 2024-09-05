import json
import os
import argparse
from datetime import datetime
from pathlib import Path
def list_top_level_nonHidden_items(directory):
    """
    creating list of top level non hidden files and folders
    """
    items = []
    if 'contents' in directory:
        for item in directory['contents']:
            if not item['name'].startswith('.'):
                items.append(item['name'])
    return items


def list_top_level_items(directory):
    """
    List the top-level non-hidden files and directories in the given directory structure.

    Args:
    directory (dict): The dictionary containing directory structure information.

    Returns:
    list: A list of dictionaries representing the top-level non-hidden items in the directory.
    """
    items = []
    if 'contents' in directory:
        for item in directory['contents']:
            # Ensure that item is a dictionary and has the required keys
            if isinstance(item, dict) and 'name' in item:
                # Skip hidden files or directories (names starting with '.')
                if not item['name'].startswith('.'):
                    items.append(item)  # Append the whole item dictionary
            else:
                print(f"DEBUG: Unexpected item format: {item}")
    else:
        print("DEBUG: No 'contents' found in the directory structure.")
    return items


def list_top_level_Hidden_items(directory):
    """
    creating list of top level hidden files and folders
    """
    items = []
    if 'contents' in directory:
        for item in directory['contents']:
            items.append(item['name'])
    return items


def format_item_long(item):
    """
    making linux pattern file/folder information
    """
    permissions = item['permissions']
    size = item['size']
    time_modified = datetime.fromtimestamp(item['time_modified'])
    time_str = time_modified.strftime("%b %d %H:%M")
    name = item['name']

    return f"{permissions} {size:>5} {time_str} {name}"


def print_items(items, long_format=False):
    """
    Print the items in either short or long format.

    """
    if long_format:
        for item in sorted(items, key=lambda x: x['name']):
            name = item['name']
            permissions = item.get('permissions', '---------')
            size = item.get('size', 0)
            time_modified = datetime.fromtimestamp(item.get('time_modified', 0)).strftime('%b %d %H:%M')
            print(f"{permissions} {size} {time_modified} {name}")
    else:
        print(" ".join(sorted(item['name'] for item in items)))

def print_items1(items, long_format=False, reverse=False, sort_by_time=False, filter_option=None):
    """
    Print the items in either short or long format.

    """
    if filter_option:
        if filter_option == 'file':
            items = [item for item in items if 'contents' not in item]  # Files do not have 'contents' key
        elif filter_option == 'dir':
            items = [item for item in items if 'contents' in item]  # Directories have 'contents' key

    #sorted_items = sorted(items, key=lambda x: x['name'], reverse=reverse)
    if sort_by_time:
        sorted_items = sorted(items, key=lambda x: x.get('time_modified', 0), reverse=reverse)
    else:
        sorted_items = sorted(items, key=lambda x: x['name'], reverse=reverse)

    if long_format:
        for item in sorted_items:
            name = item['name']
            permissions = item.get('permissions', '---------')
            size = human_readable_size(item.get('size', 0))
            time_modified = datetime.fromtimestamp(item.get('time_modified', 0)).strftime('%b %d %H:%M')
            print(f"{permissions} {size} {time_modified} {name}")
    else:
        print(" ".join(sorted(item['name'] for item in items)))

def navigate_to_path(directory, path):
    """
    Navigate to the specified path in the JSON directory structure.
    """
    if path == '.' or path == './':
        return directory['contents']

    parts = path.strip('/').split('/')
    current_dir = directory

    for part in parts:
        found = False
        for item in current_dir.get('contents', []):
            if item['name'] == part:
                if 'contents' in item:
                    # This is a directory
                    current_dir = item
                    found = True
                    break
                else:
                    # This is a file
                    return [item]
        if not found:
            return None  # Path not found

    return current_dir.get('contents', [])

def human_readable_size(size):
    """
    Convert bytes to a human-readable format.
    """
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f}K"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.1f}M"
    else:
        return f"{size / (1024 * 1024 * 1024):.1f}G"


def main():
    parser = argparse.ArgumentParser(
        description="List directory contents in various formats",
        epilog="Available commands: -l (long format), -r (reverse order), -t (sort by time), --filter=<option> (file or dir)"
    )
    parser.add_argument('-l', action='store_true', help='use a long listing format')
    parser.add_argument('-r', action='store_true', help="Reverse the order of the output")
    parser.add_argument('-t', action='store_true', help="Sort by modification time, oldest first.")
    parser.add_argument('--filter', choices=['file', 'dir'],
                        help="Filter the output to only show files or directories.")
    parser.add_argument('path', nargs='?', default='.', help="Path to list (default is current directory).")
    args = parser.parse_args()

    # locating the JSON file
    # current_dir = os.path.dirname(__file__)
    # json_file_path = os.path.join(current_dir, '..', 'structure.json')
    current_dir = Path(__file__).parent
    json_file_path = current_dir / 'structure.json'

    if not json_file_path.exists():
        print(f"error: cannot access '{json_file_path}': No such file or directory")
        return
    # Read the JSON data from the file
    with open(json_file_path, 'r') as file:
        directory_structure = json.load(file)

    # List and print the top-level items
    top_level_non_hidden_items = list_top_level_nonHidden_items(directory_structure)
    print(top_level_non_hidden_items)
    print(' '.join(sorted(top_level_non_hidden_items)))
    top_level_hidden_items = list_top_level_Hidden_items(directory_structure)
    print(top_level_hidden_items)
    print(' '.join(sorted(top_level_hidden_items)))
    top_level_items = list_top_level_items(directory_structure)

    if args.path == '.' or args.path == './':
        target_items = list_top_level_items(directory_structure)
    else:
        target_items = navigate_to_path(directory_structure, args.path)
        if target_items is None:
            print(f"error: cannot access '{args.path}': No such file or directory")
            return
    print_items(top_level_items, long_format=args.l)
    print_items1(target_items, long_format=args.l, reverse=args.r, sort_by_time=args.t, filter_option=args.filter)


if __name__ == "__main__":
    main()

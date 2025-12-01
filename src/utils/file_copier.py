"""
Recursive file copier that sorts files by extension.

This module provides functionality to recursively copy files from a source
directory to a destination directory, organizing them into subdirectories
based on their file extensions.
"""

import os
import shutil
import sys
from pathlib import Path


def parse_arguments(args: list[str]) -> tuple[Path, Path]:
    """
    Parse command-line arguments for source and destination directories.
    
    Args:
        args: List of command-line arguments (excluding script name)
        
    Returns:
        Tuple of (source_path, destination_path) as Path objects
        
    Raises:
        ValueError: If source directory is not provided or doesn't exist
    """
    if len(args) < 1:
        raise ValueError("Source directory is required")
    
    source_dir = Path(args[0])
    destination_dir = Path(args[1]) if len(args) > 1 else Path("dist")
    
    if not source_dir.exists():
        raise ValueError(f"Source directory does not exist: {source_dir}")
    
    if not source_dir.is_dir():
        raise ValueError(f"Source path is not a directory: {source_dir}")
    
    return source_dir, destination_dir


def get_file_extension(file_path: Path) -> str:
    """
    Get the file extension without the dot.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File extension in lowercase without the dot, or 'no_extension' if none
    """
    extension = file_path.suffix.lstrip('.')
    return extension.lower() if extension else 'no_extension'


def copy_file_to_destination(file_path: Path, destination_base: Path) -> None:
    """
    Copy a file to the destination directory, organizing by extension.
    
    Args:
        file_path: Path to the source file
        destination_base: Base destination directory path
        
    Raises:
        OSError: If there's an error copying the file
    """
    try:
        extension = get_file_extension(file_path)
        extension_dir = destination_base / extension
        
        extension_dir.mkdir(parents=True, exist_ok=True)
        
        destination_file = extension_dir / file_path.name
        
        # Handle duplicate filenames
        counter = 1
        original_stem = file_path.stem
        while destination_file.exists():
            new_name = f"{original_stem}_{counter}{file_path.suffix}"
            destination_file = extension_dir / new_name
            counter += 1
        
        shutil.copy2(file_path, destination_file)
        print(f"Copied: {file_path} -> {destination_file}")
        
    except OSError as e:
        print(f"Error copying file {file_path}: {e}", file=sys.stderr)
        raise


def process_directory_recursive(source_dir: Path, destination_dir: Path) -> None:
    """
    Recursively process directory and copy all files to destination.
    
    Args:
        source_dir: Source directory to process
        destination_dir: Destination base directory
        
    Raises:
        OSError: If there's an error accessing directories
    """
    try:
        for item in source_dir.iterdir():
            if item.is_file():
                copy_file_to_destination(item, destination_dir)
            elif item.is_dir():
                process_directory_recursive(item, destination_dir)
    except OSError as e:
        print(f"Error accessing directory {source_dir}: {e}", file=sys.stderr)
        raise


def main() -> None:
    """
    Main function to execute the file copying script.
    
    Parses command-line arguments and initiates the recursive file copying process.
    """
    try:
        source_dir, destination_dir = parse_arguments(sys.argv[1:])
        
        print(f"Source directory: {source_dir}")
        print(f"Destination directory: {destination_dir}")
        print("Starting file copying process...")
        
        process_directory_recursive(source_dir, destination_dir)
        
        print("\nFile copying completed successfully!")
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Usage: python file_copier.py <source_directory> [destination_directory]")
        sys.exit(1)
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


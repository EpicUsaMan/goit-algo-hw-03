"""
Tests for file_copier module.
"""

import os
import shutil
import sys
import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch

from src.utils.file_copier import (
    parse_arguments,
    get_file_extension,
    copy_file_to_destination,
    process_directory_recursive,
    main,
)


class TestParseArguments:
    """Tests for parse_arguments function."""
    
    def test_parse_arguments_with_both_paths(self, tmp_path):
        """Test parsing with both source and destination paths."""
        source = tmp_path / "source"
        source.mkdir()
        dest = tmp_path / "dest"
        
        result_source, result_dest = parse_arguments([str(source), str(dest)])
        
        assert result_source == source
        assert result_dest == dest
    
    def test_parse_arguments_with_source_only(self, tmp_path):
        """Test parsing with only source path (default destination)."""
        source = tmp_path / "source"
        source.mkdir()
        
        result_source, result_dest = parse_arguments([str(source)])
        
        assert result_source == source
        assert result_dest == Path("dist")
    
    def test_parse_arguments_no_arguments(self):
        """Test parsing with no arguments raises ValueError."""
        with pytest.raises(ValueError, match="Source directory is required"):
            parse_arguments([])
    
    def test_parse_arguments_nonexistent_source(self):
        """Test parsing with non-existent source directory."""
        with pytest.raises(ValueError, match="Source directory does not exist"):
            parse_arguments(["/nonexistent/path"])
    
    def test_parse_arguments_source_is_file(self, tmp_path):
        """Test parsing when source path is a file, not a directory."""
        file_path = tmp_path / "file.txt"
        file_path.touch()
        
        with pytest.raises(ValueError, match="Source path is not a directory"):
            parse_arguments([str(file_path)])


class TestGetFileExtension:
    """Tests for get_file_extension function."""
    
    def test_get_file_extension_with_extension(self):
        """Test getting extension from file with extension."""
        path = Path("document.txt")
        assert get_file_extension(path) == "txt"
    
    def test_get_file_extension_uppercase(self):
        """Test that extensions are converted to lowercase."""
        path = Path("document.PDF")
        assert get_file_extension(path) == "pdf"
    
    def test_get_file_extension_multiple_dots(self):
        """Test file with multiple dots (gets last extension)."""
        path = Path("archive.tar.gz")
        assert get_file_extension(path) == "gz"
    
    def test_get_file_extension_no_extension(self):
        """Test file without extension."""
        path = Path("README")
        assert get_file_extension(path) == "no_extension"
    
    def test_get_file_extension_hidden_file(self):
        """Test hidden file without extension."""
        path = Path(".gitignore")
        assert get_file_extension(path) == "no_extension"


class TestCopyFileToDestination:
    """Tests for copy_file_to_destination function."""
    
    def test_copy_file_creates_extension_directory(self, tmp_path):
        """Test that extension directory is created."""
        source_file = tmp_path / "source.txt"
        source_file.write_text("test content")
        dest_dir = tmp_path / "dest"
        
        copy_file_to_destination(source_file, dest_dir)
        
        assert (dest_dir / "txt" / "source.txt").exists()
        assert (dest_dir / "txt" / "source.txt").read_text() == "test content"
    
    def test_copy_file_handles_duplicate_names(self, tmp_path):
        """Test handling of duplicate file names."""
        source1 = tmp_path / "file.txt"
        source1.write_text("content 1")
        source2 = tmp_path / "subdir" / "file.txt"
        source2.parent.mkdir()
        source2.write_text("content 2")
        dest_dir = tmp_path / "dest"
        
        copy_file_to_destination(source1, dest_dir)
        copy_file_to_destination(source2, dest_dir)
        
        assert (dest_dir / "txt" / "file.txt").exists()
        assert (dest_dir / "txt" / "file_1.txt").exists()
        assert (dest_dir / "txt" / "file.txt").read_text() == "content 1"
        assert (dest_dir / "txt" / "file_1.txt").read_text() == "content 2"
    
    def test_copy_file_no_extension(self, tmp_path):
        """Test copying file without extension."""
        source_file = tmp_path / "README"
        source_file.write_text("readme content")
        dest_dir = tmp_path / "dest"
        
        copy_file_to_destination(source_file, dest_dir)
        
        assert (dest_dir / "no_extension" / "README").exists()
    
    def test_copy_file_preserves_metadata(self, tmp_path):
        """Test that file metadata is preserved during copy."""
        source_file = tmp_path / "file.txt"
        source_file.write_text("content")
        original_mtime = source_file.stat().st_mtime
        dest_dir = tmp_path / "dest"
        
        copy_file_to_destination(source_file, dest_dir)
        
        copied_file = dest_dir / "txt" / "file.txt"
        assert copied_file.stat().st_mtime == original_mtime
    
    def test_copy_file_handles_permission_error(self, tmp_path):
        """Test handling of permission errors during copy."""
        source_file = tmp_path / "file.txt"
        source_file.write_text("content")
        dest_dir = tmp_path / "dest"
        dest_dir.mkdir()
        
        # Make destination read-only on Unix systems
        if os.name != 'nt':
            dest_dir.chmod(0o444)
            
            with pytest.raises(OSError):
                copy_file_to_destination(source_file, dest_dir)
            
            dest_dir.chmod(0o755)


class TestProcessDirectoryRecursive:
    """Tests for process_directory_recursive function."""
    
    def test_process_single_level_directory(self, tmp_path):
        """Test processing directory with files only."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "file1.txt").write_text("content1")
        (source_dir / "file2.pdf").write_text("content2")
        dest_dir = tmp_path / "dest"
        
        process_directory_recursive(source_dir, dest_dir)
        
        assert (dest_dir / "txt" / "file1.txt").exists()
        assert (dest_dir / "pdf" / "file2.pdf").exists()
    
    def test_process_nested_directories(self, tmp_path):
        """Test processing nested directory structure."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "file1.txt").write_text("content1")
        
        subdir = source_dir / "subdir"
        subdir.mkdir()
        (subdir / "file2.jpg").write_text("content2")
        
        nested_dir = subdir / "nested"
        nested_dir.mkdir()
        (nested_dir / "file3.png").write_text("content3")
        
        dest_dir = tmp_path / "dest"
        
        process_directory_recursive(source_dir, dest_dir)
        
        assert (dest_dir / "txt" / "file1.txt").exists()
        assert (dest_dir / "jpg" / "file2.jpg").exists()
        assert (dest_dir / "png" / "file3.png").exists()
    
    def test_process_empty_directory(self, tmp_path):
        """Test processing empty directory."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        dest_dir = tmp_path / "dest"
        
        process_directory_recursive(source_dir, dest_dir)
        
        assert not dest_dir.exists() or len(list(dest_dir.iterdir())) == 0
    
    def test_process_directory_with_mixed_extensions(self, tmp_path):
        """Test processing directory with various file types."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        
        extensions = ['txt', 'pdf', 'jpg', 'png', 'doc', 'xls']
        for i, ext in enumerate(extensions):
            (source_dir / f"file{i}.{ext}").write_text(f"content{i}")
        
        dest_dir = tmp_path / "dest"
        
        process_directory_recursive(source_dir, dest_dir)
        
        for ext in extensions:
            ext_dir = dest_dir / ext
            assert ext_dir.exists()
            assert len(list(ext_dir.iterdir())) == 1
    
    def test_process_directory_handles_special_characters(self, tmp_path):
        """Test processing files with special characters in names."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "file with spaces.txt").write_text("content")
        (source_dir / "file-with-dashes.txt").write_text("content")
        
        dest_dir = tmp_path / "dest"
        
        process_directory_recursive(source_dir, dest_dir)
        
        assert (dest_dir / "txt" / "file with spaces.txt").exists()
        assert (dest_dir / "txt" / "file-with-dashes.txt").exists()
    
    def test_process_directory_handles_oserror(self, tmp_path):
        """Test that OSError is properly raised when directory access fails."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "file.txt").write_text("content")
        dest_dir = tmp_path / "dest"
        
        # Make source directory unreadable on Unix systems
        if os.name != 'nt':
            source_dir.chmod(0o000)
            
            with pytest.raises(OSError):
                process_directory_recursive(source_dir, dest_dir)
            
            source_dir.chmod(0o755)


class TestMain:
    """Tests for main function."""
    
    @patch('sys.argv', ['file_copier.py', 'test_source', 'test_dest'])
    def test_main_with_valid_arguments(self, tmp_path, capsys):
        """Test main function with valid arguments."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "file.txt").write_text("content")
        dest_dir = tmp_path / "dest"
        
        with patch('sys.argv', ['file_copier.py', str(source_dir), str(dest_dir)]):
            main()
        
        captured = capsys.readouterr()
        assert "File copying completed successfully!" in captured.out
        assert (dest_dir / "txt" / "file.txt").exists()
    
    @patch('sys.argv', ['file_copier.py'])
    def test_main_without_arguments(self):
        """Test main function without arguments exits with error."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
    
    @patch('sys.argv', ['file_copier.py', '/nonexistent/path'])
    def test_main_with_nonexistent_source(self):
        """Test main function with non-existent source exits with error."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
    
    @patch('sys.argv', ['file_copier.py', 'source'])
    def test_main_with_single_argument(self, tmp_path):
        """Test main function with only source argument."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "file.txt").write_text("content")
        
        with patch('sys.argv', ['file_copier.py', str(source_dir)]):
            main()
        
        assert Path("dist/txt/file.txt").exists()
        # Cleanup
        shutil.rmtree("dist")
    
    @patch('sys.argv', ['file_copier.py', 'test_source'])
    def test_main_with_generic_exception(self, tmp_path, capsys):
        """Test main function handles generic exceptions."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "file.txt").write_text("content")
        dest_dir = tmp_path / "dest"
        
        with patch('sys.argv', ['file_copier.py', str(source_dir), str(dest_dir)]):
            with patch('src.utils.file_copier.process_directory_recursive', 
                      side_effect=RuntimeError("Unexpected error")):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Unexpected error" in captured.err


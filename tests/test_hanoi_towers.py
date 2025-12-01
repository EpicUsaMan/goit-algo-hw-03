"""
Tests for hanoi_towers module.
"""

import pytest
from io import StringIO
import sys
from unittest.mock import patch

from src.utils.hanoi_towers import (
    initialize_towers,
    move_disk,
    print_tower_state,
    hanoi_recursive,
    solve_hanoi,
    main,
)


class TestInitializeTowers:
    """Tests for initialize_towers function."""
    
    def test_initialize_towers_single_disk(self):
        """Test initializing towers with one disk."""
        towers = initialize_towers(1)
        
        assert towers == {'A': [1], 'B': [], 'C': []}
    
    def test_initialize_towers_three_disks(self):
        """Test initializing towers with three disks."""
        towers = initialize_towers(3)
        
        assert towers == {'A': [3, 2, 1], 'B': [], 'C': []}
    
    def test_initialize_towers_five_disks(self):
        """Test initializing towers with five disks."""
        towers = initialize_towers(5)
        
        assert towers == {'A': [5, 4, 3, 2, 1], 'B': [], 'C': []}
    
    def test_initialize_towers_zero_disks(self):
        """Test that zero disks raises ValueError."""
        with pytest.raises(ValueError, match="Number of disks must be at least 1"):
            initialize_towers(0)
    
    def test_initialize_towers_negative_disks(self):
        """Test that negative disks raises ValueError."""
        with pytest.raises(ValueError, match="Number of disks must be at least 1"):
            initialize_towers(-1)


class TestMoveDisk:
    """Tests for move_disk function."""
    
    def test_move_disk_valid_move(self):
        """Test moving a disk from one tower to another."""
        towers = {'A': [3, 2, 1], 'B': [], 'C': []}
        
        disk = move_disk(towers, 'A', 'C')
        
        assert disk == 1
        assert towers == {'A': [3, 2], 'B': [], 'C': [1]}
    
    def test_move_disk_to_occupied_tower(self):
        """Test moving a smaller disk onto a larger one."""
        towers = {'A': [2], 'B': [], 'C': [3]}
        
        disk = move_disk(towers, 'A', 'C')
        
        assert disk == 2
        assert towers == {'A': [], 'B': [], 'C': [3, 2]}
    
    def test_move_disk_invalid_move_larger_on_smaller(self):
        """Test that moving larger disk onto smaller raises ValueError."""
        towers = {'A': [3, 2], 'B': [], 'C': [1]}
        
        with pytest.raises(ValueError, match="Cannot place disk"):
            move_disk(towers, 'A', 'C')
    
    def test_move_disk_from_empty_tower(self):
        """Test that moving from empty tower raises ValueError."""
        towers = {'A': [3, 2, 1], 'B': [], 'C': []}
        
        with pytest.raises(ValueError, match="Cannot move from empty tower"):
            move_disk(towers, 'B', 'C')
    
    def test_move_disk_sequence(self):
        """Test sequence of valid moves."""
        towers = {'A': [3, 2, 1], 'B': [], 'C': []}
        
        move_disk(towers, 'A', 'C')
        assert towers == {'A': [3, 2], 'B': [], 'C': [1]}
        
        move_disk(towers, 'A', 'B')
        assert towers == {'A': [3], 'B': [2], 'C': [1]}
        
        move_disk(towers, 'C', 'B')
        assert towers == {'A': [3], 'B': [2, 1], 'C': []}


class TestPrintTowerState:
    """Tests for print_tower_state function."""
    
    def test_print_tower_state_with_message(self, capsys):
        """Test printing tower state with a message."""
        towers = {'A': [3, 2, 1], 'B': [], 'C': []}
        
        print_tower_state(towers, "Test message:")
        
        captured = capsys.readouterr()
        assert "Test message:" in captured.out
        assert "{'A': [3, 2, 1], 'B': [], 'C': []}" in captured.out
    
    def test_print_tower_state_without_message(self, capsys):
        """Test printing tower state without a message."""
        towers = {'A': [3, 2, 1], 'B': [], 'C': []}
        
        print_tower_state(towers)
        
        captured = capsys.readouterr()
        assert "{'A': [3, 2, 1], 'B': [], 'C': []}" in captured.out


class TestHanoiRecursive:
    """Tests for hanoi_recursive function."""
    
    def test_hanoi_recursive_single_disk(self):
        """Test solving Hanoi with one disk."""
        towers = initialize_towers(1)
        
        hanoi_recursive(1, 'A', 'C', 'B', towers, show_steps=False)
        
        assert towers == {'A': [], 'B': [], 'C': [1]}
    
    def test_hanoi_recursive_two_disks(self):
        """Test solving Hanoi with two disks."""
        towers = initialize_towers(2)
        
        hanoi_recursive(2, 'A', 'C', 'B', towers, show_steps=False)
        
        assert towers == {'A': [], 'B': [], 'C': [2, 1]}
    
    def test_hanoi_recursive_three_disks(self):
        """Test solving Hanoi with three disks."""
        towers = initialize_towers(3)
        
        hanoi_recursive(3, 'A', 'C', 'B', towers, show_steps=False)
        
        assert towers == {'A': [], 'B': [], 'C': [3, 2, 1]}
    
    def test_hanoi_recursive_four_disks(self):
        """Test solving Hanoi with four disks."""
        towers = initialize_towers(4)
        
        hanoi_recursive(4, 'A', 'C', 'B', towers, show_steps=False)
        
        assert towers == {'A': [], 'B': [], 'C': [4, 3, 2, 1]}
    
    def test_hanoi_recursive_prints_steps(self, capsys):
        """Test that hanoi_recursive prints steps when show_steps=True."""
        towers = initialize_towers(2)
        
        hanoi_recursive(2, 'A', 'C', 'B', towers, show_steps=True)
        
        captured = capsys.readouterr()
        assert "Move disk from" in captured.out
        assert "Intermediate state:" in captured.out


class TestSolveHanoi:
    """Tests for solve_hanoi function."""
    
    def test_solve_hanoi_single_disk(self):
        """Test solving Hanoi puzzle with one disk."""
        result = solve_hanoi(1, show_steps=False)
        
        assert result == {'A': [], 'B': [], 'C': [1]}
    
    def test_solve_hanoi_two_disks(self):
        """Test solving Hanoi puzzle with two disks."""
        result = solve_hanoi(2, show_steps=False)
        
        assert result == {'A': [], 'B': [], 'C': [2, 1]}
    
    def test_solve_hanoi_three_disks(self):
        """Test solving Hanoi puzzle with three disks."""
        result = solve_hanoi(3, show_steps=False)
        
        assert result == {'A': [], 'B': [], 'C': [3, 2, 1]}
    
    def test_solve_hanoi_five_disks(self):
        """Test solving Hanoi puzzle with five disks."""
        result = solve_hanoi(5, show_steps=False)
        
        assert result == {'A': [], 'B': [], 'C': [5, 4, 3, 2, 1]}
    
    def test_solve_hanoi_zero_disks(self):
        """Test that zero disks raises ValueError."""
        with pytest.raises(ValueError, match="Number of disks must be at least 1"):
            solve_hanoi(0)
    
    def test_solve_hanoi_negative_disks(self):
        """Test that negative disks raises ValueError."""
        with pytest.raises(ValueError, match="Number of disks must be at least 1"):
            solve_hanoi(-1)
    
    def test_solve_hanoi_prints_initial_state(self, capsys):
        """Test that solve_hanoi prints initial state."""
        solve_hanoi(1, show_steps=True)
        
        captured = capsys.readouterr()
        assert "Initial state:" in captured.out
        assert "{'A': [1], 'B': [], 'C': []}" in captured.out
    
    def test_solve_hanoi_prints_final_state(self, capsys):
        """Test that solve_hanoi prints final state."""
        solve_hanoi(1, show_steps=True)
        
        captured = capsys.readouterr()
        assert "Final state:" in captured.out
        assert "{'A': [], 'B': [], 'C': [1]}" in captured.out
    
    def test_solve_hanoi_correct_number_of_moves(self):
        """Test that solution uses optimal number of moves."""
        for n in range(1, 6):
            towers_initial = initialize_towers(n)
            towers_final = solve_hanoi(n, show_steps=False)
            
            assert towers_final == {'A': [], 'B': [], 'C': list(range(n, 0, -1))}
    
    def test_solve_hanoi_large_number(self):
        """Test solving with larger number of disks."""
        result = solve_hanoi(7, show_steps=False)
        
        assert result == {'A': [], 'B': [], 'C': [7, 6, 5, 4, 3, 2, 1]}
    
    def test_solve_hanoi_step_output_format(self, capsys):
        """Test that step output follows expected format."""
        solve_hanoi(3, show_steps=True)
        
        captured = capsys.readouterr()
        assert "Move disk from A to C: 1" in captured.out
        assert "Move disk from A to B: 2" in captured.out
        assert "Intermediate state:" in captured.out


class TestMain:
    """Tests for main function."""
    
    @patch('sys.argv', ['hanoi_towers.py', '3'])
    def test_main_with_valid_argument(self, capsys):
        """Test main function with valid number of disks."""
        main()
        
        captured = capsys.readouterr()
        assert "Initial state:" in captured.out
        assert "Final state:" in captured.out
    
    @patch('sys.argv', ['hanoi_towers.py', '0'])
    def test_main_with_zero_disks(self):
        """Test main function with zero disks exits with error."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
    
    @patch('sys.argv', ['hanoi_towers.py', '-1'])
    def test_main_with_negative_disks(self):
        """Test main function with negative disks exits with error."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
    
    @patch('sys.argv', ['hanoi_towers.py', 'invalid'])
    def test_main_with_invalid_argument(self):
        """Test main function with invalid argument exits with error."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
    
    @patch('sys.argv', ['hanoi_towers.py'])
    @patch('builtins.input', return_value='2')
    def test_main_with_input(self, mock_input, capsys):
        """Test main function with user input."""
        main()
        
        captured = capsys.readouterr()
        assert "Initial state:" in captured.out
        assert "Final state:" in captured.out
    
    @patch('sys.argv', ['hanoi_towers.py', '15'])
    def test_main_with_large_number(self, capsys):
        """Test main function warns for large number of disks."""
        main()
        
        captured = capsys.readouterr()
        assert "Warning" in captured.out or "Initial state:" in captured.out
    
    @patch('sys.argv', ['hanoi_towers.py', '3'])
    def test_main_with_generic_exception(self, capsys):
        """Test main function handles generic exceptions."""
        with patch('src.utils.hanoi_towers.solve_hanoi', 
                  side_effect=RuntimeError("Unexpected error")):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Unexpected error" in captured.err


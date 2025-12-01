"""
Tests for koch_snowflake module.
"""

import sys
from unittest.mock import Mock, patch, MagicMock
import pytest

try:
    import turtle
except ImportError:
    import unittest.mock
    turtle = unittest.mock.MagicMock()
    sys.modules['turtle'] = turtle

from src.utils.koch_snowflake import koch_curve, draw_koch_snowflake, main


class TestKochCurve:
    """Tests for koch_curve function."""
    
    def test_koch_curve_level_0(self):
        """Test Koch curve at recursion level 0 (straight line)."""
        mock_turtle = Mock()
        
        koch_curve(mock_turtle, 100, 0)
        
        mock_turtle.forward.assert_called_once_with(100)
        mock_turtle.left.assert_not_called()
        mock_turtle.right.assert_not_called()
    
    def test_koch_curve_level_1(self):
        """Test Koch curve at recursion level 1."""
        mock_turtle = Mock()
        
        koch_curve(mock_turtle, 90, 1)
        
        assert mock_turtle.forward.call_count == 4
        assert mock_turtle.left.call_count == 2
        assert mock_turtle.right.call_count == 1
    
    def test_koch_curve_level_2(self):
        """Test Koch curve at recursion level 2."""
        mock_turtle = Mock()
        
        koch_curve(mock_turtle, 81, 2)
        
        assert mock_turtle.forward.call_count == 16
    
    def test_koch_curve_calls_with_correct_angles(self):
        """Test that koch_curve uses correct angles."""
        mock_turtle = Mock()
        
        koch_curve(mock_turtle, 90, 1)
        
        mock_turtle.left.assert_any_call(60)
        mock_turtle.right.assert_called_with(120)
    
    def test_koch_curve_divides_length_correctly(self):
        """Test that koch_curve divides length by 3 at each level."""
        mock_turtle = Mock()
        
        koch_curve(mock_turtle, 90, 1)
        
        expected_length = 30.0
        for call in mock_turtle.forward.call_args_list:
            assert call[0][0] == pytest.approx(expected_length)


class TestDrawKochSnowflake:
    """Tests for draw_koch_snowflake function."""
    
    @patch('src.utils.koch_snowflake.turtle.Screen')
    @patch('src.utils.koch_snowflake.turtle.Turtle')
    def test_draw_koch_snowflake_initializes_screen(self, mock_turtle_class, mock_screen_class):
        """Test that draw_koch_snowflake initializes screen correctly."""
        mock_screen = MagicMock()
        mock_screen_class.return_value = mock_screen
        mock_turtle_instance = MagicMock()
        mock_turtle_class.return_value = mock_turtle_instance
        
        mock_screen.mainloop = MagicMock()
        
        draw_koch_snowflake(300, 0)
        
        mock_screen_class.assert_called_once()
        mock_screen.bgcolor.assert_called_once_with("white")
        mock_screen.title.assert_called_once_with("Koch Snowflake - Level 0")
    
    @patch('src.utils.koch_snowflake.turtle.Screen')
    @patch('src.utils.koch_snowflake.turtle.Turtle')
    def test_draw_koch_snowflake_creates_turtle(self, mock_turtle_class, mock_screen_class):
        """Test that draw_koch_snowflake creates and configures turtle."""
        mock_screen = MagicMock()
        mock_screen_class.return_value = mock_screen
        mock_turtle_instance = MagicMock()
        mock_turtle_class.return_value = mock_turtle_instance
        
        mock_screen.mainloop = MagicMock()
        
        draw_koch_snowflake(300, 0)
        
        mock_turtle_class.assert_called_once()
        mock_turtle_instance.speed.assert_called_once_with(0)
        mock_turtle_instance.color.assert_called_once_with("blue")
    
    @patch('src.utils.koch_snowflake.turtle.Screen')
    @patch('src.utils.koch_snowflake.turtle.Turtle')
    def test_draw_koch_snowflake_draws_three_sides(self, mock_turtle_class, mock_screen_class):
        """Test that draw_koch_snowflake draws three sides of triangle."""
        mock_screen = MagicMock()
        mock_screen_class.return_value = mock_screen
        mock_turtle_instance = MagicMock()
        mock_turtle_class.return_value = mock_turtle_instance
        
        mock_screen.mainloop = MagicMock()
        
        draw_koch_snowflake(300, 0)
        
        assert mock_turtle_instance.right.call_count == 3
        for call in mock_turtle_instance.right.call_args_list:
            assert call[0][0] == 120
    
    def test_draw_koch_snowflake_negative_level(self):
        """Test that negative level raises ValueError."""
        with pytest.raises(ValueError, match="Recursion level must be non-negative"):
            draw_koch_snowflake(300, -1)
    
    def test_draw_koch_snowflake_zero_length(self):
        """Test that zero length raises ValueError."""
        with pytest.raises(ValueError, match="Length must be positive"):
            draw_koch_snowflake(0, 3)
    
    def test_draw_koch_snowflake_negative_length(self):
        """Test that negative length raises ValueError."""
        with pytest.raises(ValueError, match="Length must be positive"):
            draw_koch_snowflake(-100, 3)
    
    @patch('src.utils.koch_snowflake.turtle.Screen')
    @patch('src.utils.koch_snowflake.turtle.Turtle')
    def test_draw_koch_snowflake_positions_turtle(self, mock_turtle_class, mock_screen_class):
        """Test that turtle is positioned correctly."""
        mock_screen = MagicMock()
        mock_screen_class.return_value = mock_screen
        mock_turtle_instance = MagicMock()
        mock_turtle_class.return_value = mock_turtle_instance
        
        mock_screen.mainloop = MagicMock()
        
        length = 300
        draw_koch_snowflake(length, 0)
        
        mock_turtle_instance.penup.assert_called_once()
        mock_turtle_instance.goto.assert_called_once()
        expected_x = -length / 2
        expected_y = length / 3
        actual_call = mock_turtle_instance.goto.call_args[0]
        assert actual_call[0] == pytest.approx(expected_x)
        assert actual_call[1] == pytest.approx(expected_y)
        mock_turtle_instance.pendown.assert_called_once()
    
    @patch('src.utils.koch_snowflake.turtle.Screen')
    @patch('src.utils.koch_snowflake.turtle.Turtle')
    def test_draw_koch_snowflake_hides_turtle_at_end(self, mock_turtle_class, mock_screen_class):
        """Test that turtle is hidden at the end."""
        mock_screen = MagicMock()
        mock_screen_class.return_value = mock_screen
        mock_turtle_instance = MagicMock()
        mock_turtle_class.return_value = mock_turtle_instance
        
        mock_screen.mainloop = MagicMock()
        
        draw_koch_snowflake(300, 0)
        
        mock_turtle_instance.hideturtle.assert_called_once()
    
    @patch('src.utils.koch_snowflake.turtle.Screen')
    @patch('src.utils.koch_snowflake.turtle.Turtle')
    def test_draw_koch_snowflake_different_levels(self, mock_turtle_class, mock_screen_class):
        """Test that different recursion levels produce different results."""
        mock_screen = MagicMock()
        mock_screen_class.return_value = mock_screen
        
        mock_screen.mainloop = MagicMock()
        
        for level in range(5):
            mock_turtle_instance = MagicMock()
            mock_turtle_class.return_value = mock_turtle_instance
            
            draw_koch_snowflake(300, level)
            
            mock_screen.title.assert_called_with(f"Koch Snowflake - Level {level}")


class TestMain:
    """Tests for main function."""
    
    @patch('src.utils.koch_snowflake.draw_koch_snowflake')
    @patch('sys.argv', ['koch_snowflake.py', '3'])
    def test_main_with_valid_argument(self, mock_draw):
        """Test main function with valid recursion level."""
        main()
        mock_draw.assert_called_once_with(level=3)
    
    @patch('src.utils.koch_snowflake.draw_koch_snowflake')
    @patch('sys.argv', ['koch_snowflake.py', '0'])
    def test_main_with_zero_level(self, mock_draw):
        """Test main function with zero recursion level."""
        main()
        mock_draw.assert_called_once_with(level=0)
    
    @patch('sys.argv', ['koch_snowflake.py', '-1'])
    def test_main_with_negative_level(self):
        """Test main function with negative recursion level exits with error."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
    
    @patch('sys.argv', ['koch_snowflake.py', 'invalid'])
    def test_main_with_invalid_argument(self):
        """Test main function with invalid argument exits with error."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
    
    @patch('builtins.input', return_value='2')
    @patch('src.utils.koch_snowflake.draw_koch_snowflake')
    @patch('sys.argv', ['koch_snowflake.py'])
    def test_main_with_input(self, mock_draw, mock_input):
        """Test main function with user input."""
        main()
        mock_draw.assert_called_once_with(level=2)
    
    @patch('src.utils.koch_snowflake.draw_koch_snowflake')
    @patch('sys.argv', ['koch_snowflake.py', '10'])
    def test_main_with_large_level(self, mock_draw, capsys):
        """Test main function warns for high recursion levels."""
        main()
        
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        mock_draw.assert_called_once_with(level=10)
    
    @patch('src.utils.koch_snowflake.draw_koch_snowflake')
    @patch('sys.argv', ['koch_snowflake.py', '3'])
    def test_main_with_generic_exception(self, mock_draw, capsys):
        """Test main function handles generic exceptions."""
        mock_draw.side_effect = RuntimeError("Unexpected error")
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Unexpected error" in captured.err


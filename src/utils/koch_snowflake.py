"""
Koch snowflake fractal generator.

This module provides functionality to generate and visualize the Koch snowflake
fractal using recursion and turtle graphics.
"""

import sys
import turtle


def koch_curve(t: turtle.Turtle, length: float, level: int) -> None:
    """
    Draw a Koch curve using recursion.
    
    Args:
        t: Turtle object for drawing
        length: Length of the curve segment
        level: Recursion level (0 = straight line, higher = more detail)
    """
    if level == 0:
        t.forward(length)
    else:
        length /= 3.0
        koch_curve(t, length, level - 1)
        t.left(60)
        koch_curve(t, length, level - 1)
        t.right(120)
        koch_curve(t, length, level - 1)
        t.left(60)
        koch_curve(t, length, level - 1)


def draw_koch_snowflake(length: float = 300, level: int = 3) -> None:
    """
    Draw a Koch snowflake fractal.
    
    Args:
        length: Side length of the initial triangle
        level: Recursion level for the fractal detail
        
    Raises:
        ValueError: If level is negative or length is non-positive
    """
    if level < 0:
        raise ValueError("Recursion level must be non-negative")
    if length <= 0:
        raise ValueError("Length must be positive")
    
    window = turtle.Screen()
    window.bgcolor("white")
    window.title(f"Koch Snowflake - Level {level}")
    
    t = turtle.Turtle()
    t.speed(0)
    t.color("blue")
    t.penup()
    t.goto(-length / 2, length / 3)
    t.pendown()
    
    for _ in range(3):
        koch_curve(t, length, level)
        t.right(120)
    
    t.hideturtle()
    window.mainloop()


def main() -> None:
    """
    Main function to execute the Koch snowflake generator.
    
    Accepts recursion level as command-line argument.
    """
    try:
        if len(sys.argv) > 1:
            level = int(sys.argv[1])
        else:
            level = int(input("Enter recursion level (0-6 recommended): "))
        
        if level < 0:
            raise ValueError("Recursion level must be non-negative")
        
        if level > 6:
            print("Warning: High recursion levels may be slow to render")
        
        print(f"Drawing Koch snowflake with recursion level {level}...")
        draw_koch_snowflake(level=level)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Usage: python koch_snowflake.py [level]")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


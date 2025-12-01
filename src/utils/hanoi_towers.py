"""
Towers of Hanoi solver.

This module provides functionality to solve the classic Towers of Hanoi puzzle
using recursion and visualize the solution steps.
"""

import sys


def initialize_towers(n: int) -> dict[str, list[int]]:
    """
    Initialize the three towers with n disks on tower A.
    
    Args:
        n: Number of disks
        
    Returns:
        Dictionary with tower states
        
    Raises:
        ValueError: If n is less than 1
    """
    if n < 1:
        raise ValueError("Number of disks must be at least 1")
    
    return {
        'A': list(range(n, 0, -1)),
        'B': [],
        'C': []
    }


def move_disk(towers: dict[str, list[int]], source: str, destination: str) -> int:
    """
    Move a disk from source tower to destination tower.
    
    Args:
        towers: Dictionary representing the current state of towers
        source: Source tower name ('A', 'B', or 'C')
        destination: Destination tower name ('A', 'B', or 'C')
        
    Returns:
        The disk number that was moved
        
    Raises:
        ValueError: If source tower is empty or move is invalid
    """
    if not towers[source]:
        raise ValueError(f"Cannot move from empty tower {source}")
    
    disk = towers[source][-1]
    
    if towers[destination] and towers[destination][-1] < disk:
        raise ValueError(f"Cannot place disk {disk} on smaller disk {towers[destination][-1]}")
    
    towers[source].pop()
    towers[destination].append(disk)
    
    return disk


def print_tower_state(towers: dict[str, list[int]], message: str = "") -> None:
    """
    Print the current state of all towers.
    
    Args:
        towers: Dictionary representing the current state of towers
        message: Optional message to print before the state
    """
    if message:
        print(message)
    print(towers)


def hanoi_recursive(n: int, source: str, destination: str, auxiliary: str,
                   towers: dict[str, list[int]], show_steps: bool = True) -> None:
    """
    Solve Towers of Hanoi using recursion.
    
    Args:
        n: Number of disks to move
        source: Source tower name
        destination: Destination tower name
        auxiliary: Auxiliary tower name
        towers: Dictionary representing the current state of towers
        show_steps: Whether to print intermediate steps
    """
    if n == 1:
        disk = move_disk(towers, source, destination)
        if show_steps:
            print(f"Move disk from {source} to {destination}: {disk}")
            print_tower_state(towers, "Intermediate state:")
    else:
        hanoi_recursive(n - 1, source, auxiliary, destination, towers, show_steps)
        
        disk = move_disk(towers, source, destination)
        if show_steps:
            print(f"Move disk from {source} to {destination}: {disk}")
            print_tower_state(towers, "Intermediate state:")
        
        hanoi_recursive(n - 1, auxiliary, destination, source, towers, show_steps)


def solve_hanoi(n: int, show_steps: bool = True) -> dict[str, list[int]]:
    """
    Solve the Towers of Hanoi puzzle for n disks.
    
    Args:
        n: Number of disks
        show_steps: Whether to print intermediate steps
        
    Returns:
        Final state of towers
        
    Raises:
        ValueError: If n is less than 1
    """
    if n < 1:
        raise ValueError("Number of disks must be at least 1")
    
    towers = initialize_towers(n)
    
    if show_steps:
        print_tower_state(towers, "Initial state:")
    
    hanoi_recursive(n, 'A', 'C', 'B', towers, show_steps)
    
    if show_steps:
        print_tower_state(towers, "Final state:")
    
    return towers


def main() -> None:
    """
    Main function to execute the Towers of Hanoi solver.
    
    Accepts number of disks as command-line argument.
    """
    try:
        if len(sys.argv) > 1:
            n = int(sys.argv[1])
        else:
            n = int(input("Enter number of disks: "))
        
        if n < 1:
            raise ValueError("Number of disks must be at least 1")
        
        if n > 10:
            print("Warning: Large number of disks will result in many steps")
            print(f"Total moves required: {2**n - 1}")
        
        solve_hanoi(n)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Usage: python hanoi_towers.py [number_of_disks]")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


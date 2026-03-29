"""PawPal+ System — Backend logic layer for pet care management."""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    time: str  # HH:MM format
    duration_minutes: int
    priority: str = "medium"  # low, medium, high
    frequency: str = "once"  # once, daily, weekly
    is_complete: bool = False
    pet_name: str = ""
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Mark this task as completed."""
        pass

    def __str__(self) -> str:
        """Return a readable string representation."""
        pass


@dataclass
class Pet:
    """Stores pet details and manages its task list."""
    name: str
    species: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        pass

    def remove_task(self, description: str):
        """Remove a task by description."""
        pass

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        pass

    def get_pending_tasks(self) -> list:
        """Return only incomplete tasks."""
        pass


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name: str):
        """Initialize an owner with a name and empty pet list."""
        pass

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's collection."""
        pass

    def remove_pet(self, name: str):
        """Remove a pet by name."""
        pass

    def get_pet(self, name: str) -> Optional[Pet]:
        """Retrieve a pet by name."""
        pass

    def get_all_tasks(self) -> list:
        """Retrieve all tasks across all pets."""
        pass


class Scheduler:
    """The 'brain' — retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        pass

    def get_todays_tasks(self) -> list:
        """Get all tasks due today."""
        pass

    def sort_by_time(self, tasks: list) -> list:
        """Sort tasks chronologically by time (HH:MM)."""
        pass

    def sort_by_priority(self, tasks: list) -> list:
        """Sort tasks by priority (high > medium > low)."""
        pass

    def filter_by_pet(self, tasks: list, pet_name: str) -> list:
        """Filter tasks belonging to a specific pet."""
        pass

    def filter_by_status(self, tasks: list, complete: bool = False) -> list:
        """Filter tasks by completion status."""
        pass

    def detect_conflicts(self, tasks: list) -> list:
        """Detect scheduling conflicts (same pet, same time)."""
        pass

    def handle_recurrence(self, task: Task) -> Optional[Task]:
        """Create next occurrence for recurring tasks."""
        pass

    def mark_task_complete(self, pet_name: str, description: str):
        """Mark a specific task as complete, handling recurrence."""
        pass

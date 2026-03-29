"""PawPal+ System — Backend logic layer for pet care management."""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


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
        self.is_complete = True

    def __str__(self) -> str:
        """Return a readable string representation."""
        status = "Done" if self.is_complete else "Pending"
        return (
            f"[{status}] {self.time} - {self.description} "
            f"({self.duration_minutes}min, {self.priority} priority, {self.pet_name})"
        )


@dataclass
class Pet:
    """Stores pet details and manages its task list."""
    name: str
    species: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, description: str):
        """Remove a task by description."""
        self.tasks = [t for t in self.tasks if t.description != description]

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        return list(self.tasks)

    def get_pending_tasks(self) -> list:
        """Return only incomplete tasks."""
        return [t for t in self.tasks if not t.is_complete]


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name: str):
        """Initialize an owner with a name and empty pet list."""
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, name: str):
        """Remove a pet by name."""
        self.pets = [p for p in self.pets if p.name != name]

    def get_pet(self, name: str) -> Optional[Pet]:
        """Retrieve a pet by name."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_all_tasks(self) -> list:
        """Retrieve all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """The 'brain' — retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def get_todays_tasks(self) -> list:
        """Get all tasks due today."""
        today = date.today()
        return [t for t in self.owner.get_all_tasks() if t.due_date == today]

    def sort_by_time(self, tasks: list) -> list:
        """Sort tasks chronologically by time (HH:MM)."""
        return sorted(tasks, key=lambda t: t.time)

    def sort_by_priority(self, tasks: list) -> list:
        """Sort tasks by priority (high > medium > low)."""
        return sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.priority, 1))

    def filter_by_pet(self, tasks: list, pet_name: str) -> list:
        """Filter tasks belonging to a specific pet."""
        return [t for t in tasks if t.pet_name == pet_name]

    def filter_by_status(self, tasks: list, complete: bool = False) -> list:
        """Filter tasks by completion status."""
        return [t for t in tasks if t.is_complete == complete]

    def detect_conflicts(self, tasks: list) -> list:
        """Detect scheduling conflicts (same pet, same time)."""
        conflicts = []
        seen = {}
        for task in tasks:
            key = (task.pet_name, task.time)
            if key in seen:
                conflicts.append(
                    f"Conflict: '{task.description}' and '{seen[key].description}' "
                    f"are both scheduled at {task.time} for {task.pet_name}"
                )
            else:
                seen[key] = task
        return conflicts

    def handle_recurrence(self, task: Task) -> Optional[Task]:
        """Create next occurrence for recurring tasks."""
        if task.frequency == "daily":
            next_date = task.due_date + timedelta(days=1)
        elif task.frequency == "weekly":
            next_date = task.due_date + timedelta(weeks=1)
        else:
            return None

        return Task(
            description=task.description,
            time=task.time,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            frequency=task.frequency,
            is_complete=False,
            pet_name=task.pet_name,
            due_date=next_date,
        )

    def mark_task_complete(self, pet_name: str, description: str):
        """Mark a specific task as complete, handling recurrence."""
        pet = self.owner.get_pet(pet_name)
        if not pet:
            return

        for task in pet.tasks:
            if task.description == description and not task.is_complete:
                task.mark_complete()
                new_task = self.handle_recurrence(task)
                if new_task:
                    pet.add_task(new_task)
                return

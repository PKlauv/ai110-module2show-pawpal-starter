"""Tests for the PawPal+ system."""

from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


# --- Task Tests ---

def test_task_mark_complete():
    """Verify that marking a task complete changes its status."""
    task = Task("Walk", "08:00", 30)
    assert task.is_complete is False
    task.mark_complete()
    assert task.is_complete is True


def test_task_str():
    """Verify readable string output for a task."""
    task = Task("Walk", "08:00", 30, priority="high", pet_name="Mochi")
    assert "Pending" in str(task)
    assert "Walk" in str(task)
    task.mark_complete()
    assert "Done" in str(task)


# --- Pet Tests ---

def test_pet_add_task():
    """Verify that adding a task increases the pet's task count."""
    pet = Pet("Mochi", "dog", 3)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task("Walk", "08:00", 30))
    assert len(pet.get_tasks()) == 1


def test_pet_add_task_sets_pet_name():
    """Verify that adding a task auto-sets the pet_name field."""
    pet = Pet("Mochi", "dog", 3)
    task = Task("Walk", "08:00", 30)
    pet.add_task(task)
    assert task.pet_name == "Mochi"


def test_pet_remove_task():
    """Verify task removal by description."""
    pet = Pet("Mochi", "dog", 3)
    pet.add_task(Task("Walk", "08:00", 30))
    pet.add_task(Task("Feed", "12:00", 10))
    pet.remove_task("Walk")
    assert len(pet.get_tasks()) == 1
    assert pet.get_tasks()[0].description == "Feed"


def test_pet_get_pending_tasks():
    """Verify filtering for incomplete tasks only."""
    pet = Pet("Mochi", "dog", 3)
    t1 = Task("Walk", "08:00", 30)
    t2 = Task("Feed", "12:00", 10)
    pet.add_task(t1)
    pet.add_task(t2)
    t1.mark_complete()
    pending = pet.get_pending_tasks()
    assert len(pending) == 1
    assert pending[0].description == "Feed"


# --- Owner Tests ---

def test_owner_add_and_get_pet():
    """Verify adding a pet and retrieving it by name."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)
    owner.add_pet(pet)
    assert owner.get_pet("Mochi") is pet
    assert owner.get_pet("Unknown") is None


def test_owner_get_all_tasks():
    """Verify aggregation of tasks across all pets."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog", 3)
    whiskers = Pet("Whiskers", "cat", 5)
    mochi.add_task(Task("Walk", "08:00", 30))
    whiskers.add_task(Task("Feed", "09:00", 10))
    owner.add_pet(mochi)
    owner.add_pet(whiskers)
    assert len(owner.get_all_tasks()) == 2


# --- Scheduler: Sorting Tests ---

def test_sort_by_time():
    """Verify tasks are returned in chronological order."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)
    pet.add_task(Task("Evening walk", "17:00", 30))
    pet.add_task(Task("Morning walk", "07:30", 25))
    pet.add_task(Task("Lunch feed", "12:00", 10))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time(pet.get_tasks())
    times = [t.time for t in sorted_tasks]
    assert times == ["07:30", "12:00", "17:00"]


def test_sort_by_priority():
    """Verify tasks are sorted high > medium > low."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)
    pet.add_task(Task("Low task", "08:00", 10, priority="low"))
    pet.add_task(Task("High task", "09:00", 10, priority="high"))
    pet.add_task(Task("Medium task", "10:00", 10, priority="medium"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_priority(pet.get_tasks())
    priorities = [t.priority for t in sorted_tasks]
    assert priorities == ["high", "medium", "low"]


# --- Scheduler: Filtering Tests ---

def test_filter_by_pet():
    """Verify filtering tasks by pet name."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog", 3)
    whiskers = Pet("Whiskers", "cat", 5)
    mochi.add_task(Task("Walk", "08:00", 30))
    whiskers.add_task(Task("Feed", "09:00", 10))
    owner.add_pet(mochi)
    owner.add_pet(whiskers)
    scheduler = Scheduler(owner)

    all_tasks = owner.get_all_tasks()
    mochi_tasks = scheduler.filter_by_pet(all_tasks, "Mochi")
    assert len(mochi_tasks) == 1
    assert mochi_tasks[0].description == "Walk"


def test_filter_by_status():
    """Verify filtering by completion status."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)
    t1 = Task("Walk", "08:00", 30)
    t2 = Task("Feed", "12:00", 10)
    pet.add_task(t1)
    pet.add_task(t2)
    t1.mark_complete()
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    completed = scheduler.filter_by_status(pet.get_tasks(), complete=True)
    pending = scheduler.filter_by_status(pet.get_tasks(), complete=False)
    assert len(completed) == 1
    assert len(pending) == 1
    assert completed[0].description == "Walk"
    assert pending[0].description == "Feed"


# --- Scheduler: Conflict Detection ---

def test_detect_conflicts_same_pet_same_time():
    """Verify conflicts are flagged for same pet at same time."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)
    pet.add_task(Task("Walk", "09:00", 30))
    pet.add_task(Task("Vet visit", "09:00", 60))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts(pet.get_tasks())
    assert len(conflicts) == 1
    assert "Walk" in conflicts[0]
    assert "Vet visit" in conflicts[0]


def test_no_conflict_different_pets_same_time():
    """Verify no conflict when different pets share a time slot."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog", 3)
    whiskers = Pet("Whiskers", "cat", 5)
    mochi.add_task(Task("Walk", "09:00", 30))
    whiskers.add_task(Task("Feed", "09:00", 10))
    owner.add_pet(mochi)
    owner.add_pet(whiskers)
    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())
    assert len(conflicts) == 0


# --- Scheduler: Recurrence ---

def test_recurrence_daily():
    """Verify daily task creates next-day occurrence when completed."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)
    today = date.today()
    pet.add_task(Task("Walk", "08:00", 30, frequency="daily", due_date=today))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    scheduler.mark_task_complete("Mochi", "Walk")

    tasks = pet.get_tasks()
    assert len(tasks) == 2
    assert tasks[0].is_complete is True
    assert tasks[1].is_complete is False
    assert tasks[1].due_date == today + timedelta(days=1)


def test_recurrence_weekly():
    """Verify weekly task creates next-week occurrence when completed."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)
    today = date.today()
    pet.add_task(Task("Grooming", "10:00", 45, frequency="weekly", due_date=today))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    scheduler.mark_task_complete("Mochi", "Grooming")

    tasks = pet.get_tasks()
    assert len(tasks) == 2
    assert tasks[1].due_date == today + timedelta(weeks=1)


def test_no_recurrence_for_once():
    """Verify one-time tasks don't recur."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)
    pet.add_task(Task("Vet visit", "09:00", 60, frequency="once"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    scheduler.mark_task_complete("Mochi", "Vet visit")
    assert len(pet.get_tasks()) == 1


# --- Edge Cases ---

def test_pet_with_no_tasks():
    """Verify a pet with no tasks returns empty lists."""
    pet = Pet("Mochi", "dog", 3)
    assert pet.get_tasks() == []
    assert pet.get_pending_tasks() == []


def test_owner_with_no_pets():
    """Verify an owner with no pets returns empty task list."""
    owner = Owner("Jordan")
    assert owner.get_all_tasks() == []


def test_scheduler_empty_owner():
    """Verify scheduler handles an owner with no pets."""
    owner = Owner("Jordan")
    scheduler = Scheduler(owner)
    assert scheduler.get_todays_tasks() == []
    assert scheduler.detect_conflicts([]) == []

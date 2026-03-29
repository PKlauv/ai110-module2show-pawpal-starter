"""Tests for the PawPal+ system."""

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

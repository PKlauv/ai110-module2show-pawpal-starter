"""PawPal+ CLI Demo — Verifies backend logic in the terminal."""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # --- Setup: Create an owner with two pets ---
    owner = Owner("Jordan")

    mochi = Pet(name="Mochi", species="dog", age=3)
    whiskers = Pet(name="Whiskers", species="cat", age=5)

    owner.add_pet(mochi)
    owner.add_pet(whiskers)

    # --- Add tasks (intentionally out of order to test sorting) ---
    mochi.add_task(Task("Evening walk", "17:00", 30, priority="medium", frequency="daily"))
    mochi.add_task(Task("Morning walk", "07:30", 25, priority="high", frequency="daily"))
    mochi.add_task(Task("Flea medication", "09:00", 5, priority="high", frequency="once"))

    whiskers.add_task(Task("Breakfast feeding", "08:00", 10, priority="high", frequency="daily"))
    whiskers.add_task(Task("Litter box cleanup", "12:00", 10, priority="medium", frequency="daily"))
    whiskers.add_task(Task("Vet appointment", "09:00", 60, priority="high", frequency="once"))

    # --- Build the scheduler ---
    scheduler = Scheduler(owner)

    # --- Today's schedule (sorted by time) ---
    todays_tasks = scheduler.get_todays_tasks()
    sorted_tasks = scheduler.sort_by_time(todays_tasks)

    print("=" * 60)
    print(f"  PawPal+ Daily Schedule for {owner.name}")
    print(f"  Pets: {', '.join(p.name for p in owner.pets)}")
    print("=" * 60)

    for task in sorted_tasks:
        print(f"  {task}")
    print()

    # --- Conflict detection ---
    conflicts = scheduler.detect_conflicts(todays_tasks)
    if conflicts:
        print("*** Schedule Conflicts ***")
        for warning in conflicts:
            print(f"  WARNING: {warning}")
        print()
    else:
        print("No scheduling conflicts detected.\n")

    # --- Filter by pet ---
    print(f"--- Tasks for Mochi only ---")
    mochi_tasks = scheduler.filter_by_pet(sorted_tasks, "Mochi")
    for task in mochi_tasks:
        print(f"  {task}")
    print()

    # --- Sort by priority ---
    print("--- All tasks by priority ---")
    by_priority = scheduler.sort_by_priority(todays_tasks)
    for task in by_priority:
        print(f"  {task}")
    print()

    # --- Mark a task complete and show recurrence ---
    print("--- Marking 'Morning walk' as complete ---")
    scheduler.mark_task_complete("Mochi", "Morning walk")

    mochi_tasks_after = mochi.get_tasks()
    for task in mochi_tasks_after:
        if "walk" in task.description.lower() and "morning" in task.description.lower():
            print(f"  {task}")
    print()

    # --- Show pending vs completed ---
    pending = scheduler.filter_by_status(scheduler.get_todays_tasks(), complete=False)
    completed = scheduler.filter_by_status(mochi.get_tasks(), complete=True)
    print(f"Pending tasks today: {len(pending)}")
    print(f"Completed tasks (Mochi): {len(completed)}")


if __name__ == "__main__":
    main()

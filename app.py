import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Smart pet care management — track tasks, detect conflicts, and stay on schedule.")

# --- Session State: persist Owner across reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

# --- Sidebar: Owner + Pet Setup ---
with st.sidebar:
    st.header("Setup")

    new_owner_name = st.text_input("Owner name", value=owner.name)
    if new_owner_name != owner.name:
        owner.name = new_owner_name

    st.subheader("Add a Pet")
    pet_name = st.text_input("Pet name", value="")
    pet_species = st.selectbox("Species", ["dog", "cat", "bird", "fish", "other"])
    pet_age = st.number_input("Age", min_value=0, max_value=30, value=2)

    if st.button("Add Pet"):
        if pet_name.strip():
            if owner.get_pet(pet_name.strip()):
                st.warning(f"A pet named '{pet_name}' already exists.")
            else:
                owner.add_pet(Pet(pet_name.strip(), pet_species, pet_age))
                st.success(f"Added {pet_name}!")
                st.rerun()
        else:
            st.warning("Please enter a pet name.")

    if owner.pets:
        st.subheader("Your Pets")
        for pet in owner.pets:
            st.write(f"**{pet.name}** — {pet.species}, {pet.age} yrs, {len(pet.tasks)} tasks")

# --- Main Area ---
if not owner.pets:
    st.info("Add a pet in the sidebar to get started.")
else:
    # --- Add Task Section ---
    st.subheader("Add a Task")

    selected_pet_name = st.selectbox(
        "For which pet?",
        [p.name for p in owner.pets],
    )

    col1, col2 = st.columns(2)
    with col1:
        task_desc = st.text_input("Task description", value="Morning walk")
        task_time = st.time_input("Scheduled time")
    with col2:
        task_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        task_priority = st.selectbox("Priority", ["high", "medium", "low"], index=1)
        task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add Task"):
        time_str = task_time.strftime("%H:%M")
        pet = owner.get_pet(selected_pet_name)
        if pet:
            pet.add_task(Task(
                description=task_desc,
                time=time_str,
                duration_minutes=task_duration,
                priority=task_priority,
                frequency=task_frequency,
            ))
            st.success(f"Added '{task_desc}' for {selected_pet_name} at {time_str}")
            st.rerun()

    st.divider()

    # --- Generate Schedule ---
    st.subheader("Today's Schedule")

    todays_tasks = scheduler.get_todays_tasks()

    if not todays_tasks:
        st.info("No tasks scheduled for today. Add some above!")
    else:
        # Conflict detection
        conflicts = scheduler.detect_conflicts(todays_tasks)
        if conflicts:
            for warning in conflicts:
                st.warning(warning)

        # Sort and display
        sorted_tasks = scheduler.sort_by_time(todays_tasks)

        table_data = []
        for t in sorted_tasks:
            status = "✅" if t.is_complete else "⏳"
            table_data.append({
                "Status": status,
                "Time": t.time,
                "Task": t.description,
                "Pet": t.pet_name,
                "Duration": f"{t.duration_minutes} min",
                "Priority": t.priority.capitalize(),
                "Frequency": t.frequency.capitalize(),
            })

        st.table(table_data)

        # --- Mark Complete ---
        st.subheader("Mark Task Complete")
        pending = scheduler.filter_by_status(todays_tasks, complete=False)
        if pending:
            task_options = [f"{t.pet_name}: {t.description} ({t.time})" for t in pending]
            selected = st.selectbox("Select task to complete", task_options)
            if st.button("Mark Complete"):
                idx = task_options.index(selected)
                task = pending[idx]
                scheduler.mark_task_complete(task.pet_name, task.description)
                st.success(f"Completed '{task.description}'!")
                if task.frequency != "once":
                    st.info(f"Next '{task.description}' scheduled ({task.frequency}).")
                st.rerun()
        else:
            st.success("All tasks completed for today!")

        # --- Filter by Pet ---
        if len(owner.pets) > 1:
            st.subheader("Filter by Pet")
            filter_pet = st.selectbox(
                "Show tasks for",
                ["All"] + [p.name for p in owner.pets],
                key="filter_pet",
            )
            if filter_pet != "All":
                filtered = scheduler.filter_by_pet(sorted_tasks, filter_pet)
                if filtered:
                    filter_data = []
                    for t in filtered:
                        status = "✅" if t.is_complete else "⏳"
                        filter_data.append({
                            "Status": status,
                            "Time": t.time,
                            "Task": t.description,
                            "Duration": f"{t.duration_minutes} min",
                            "Priority": t.priority.capitalize(),
                        })
                    st.table(filter_data)
                else:
                    st.info(f"No tasks for {filter_pet} today.")

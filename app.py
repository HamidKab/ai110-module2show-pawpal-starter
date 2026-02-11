import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Walk, Feed, GiveMedicine
from datetime import datetime, timedelta

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ app - your pet care planning assistant!

This app helps you plan care tasks for your pet(s) based on time, priority, and preferences.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

# Initialize session state vault
if "vault" not in st.session_state:
    st.session_state.vault = {
        "owner": None,
        "pets": {},
        "task_counter": 0
    }

# Owner Section
st.subheader("👤 Owner Information")
owner_name = st.text_input("Owner name", value="Jordan")
contact_info = st.text_input("Contact info (email/phone)", value="jordan@email.com")

# Check if owner exists, if not create one
if st.session_state.vault["owner"] is None:
    if st.button("Create Owner Profile"):
        owner_id = 1
        st.session_state.vault["owner"] = Owner(owner_id, owner_name, contact_info)
        st.success(f"✅ Owner profile created for {owner_name}!")
        st.rerun()
else:
    current_owner = st.session_state.vault["owner"]
    st.info(f"✅ Owner: {current_owner.name} | Contact: {current_owner.contact_info}")

    # Update owner info if changed
    if owner_name != current_owner.name or contact_info != current_owner.contact_info:
        current_owner.name = owner_name
        current_owner.contact_info = contact_info

st.divider()

# Pet Section
st.subheader("🐾 Add Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
breed = st.text_input("Breed", value="Golden Retriever")
medication_type = st.text_input("Medication type (if any)", value="None")

if st.session_state.vault["owner"] is not None:
    if st.button("Add Pet"):
        # Check if pet already exists
        if pet_name not in st.session_state.vault["pets"]:
            pet_id = 100 + len(st.session_state.vault["pets"]) + 1
            new_pet = Pet(pet_id, pet_name, species, breed, medication_type)
            st.session_state.vault["pets"][pet_name] = new_pet
            st.session_state.vault["owner"].add_pet(new_pet)
            st.success(f"✅ Added {pet_name} to {st.session_state.vault['owner'].name}'s pets!")
            st.rerun()
        else:
            st.warning(f"⚠️ Pet {pet_name} already exists!")
else:
    st.info("👆 Please create an owner profile first to add pets.")

# Display current pets
if st.session_state.vault["pets"]:
    st.markdown("### Current Pets:")
    for pet in st.session_state.vault["pets"].values():
        st.write(f"- **{pet.name}** ({pet.species}) - {pet.breed}")

st.divider()

# Tasks Section
st.subheader("📋 Schedule Tasks")
st.caption("Add care tasks for your pets.")

if st.session_state.vault["pets"]:
    selected_pet_name = st.selectbox("Select pet", list(st.session_state.vault["pets"].keys()))

    task_type = st.selectbox("Task type", ["Walk", "Feed", "GiveMedicine"])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        hours_from_now = st.text_input("Schedule Time", value="12:40")
    with col2:
        priority = st.selectbox("Priority", ["low (1)", "medium (2)", "high (3)"], index=2)
    with col3:
        priority_value = int(priority.split("(")[1].strip(")"))
        

    # Recurrence option
    recurrence = st.selectbox("Recurrence", ["none", "daily", "weekly"])
    if recurrence != "none":
        st.info(f"ℹ️ This task will automatically recreate itself {recurrence} when marked complete.")

    # Task-specific fields
    if task_type == "Walk":
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
    elif task_type == "Feed":
        food_type = st.text_input("Food type", value="Dry Kibble")
        portion_size = st.text_input("Portion size", value="1 cup")
    elif task_type == "GiveMedicine":
        medication_name = st.text_input("Medication name", value="PetMed")
        dosage = st.text_input("Dosage", value="5ml")

    if st.button("Add Task"):
        st.session_state.vault["task_counter"] += 1
        task_time = datetime.now().replace(hour=int(hours_from_now.split(":")[0]), minute=int(hours_from_now.split(":")[1]), second=0, microsecond=0)

        # Create appropriate task object with recurrence
        if task_type == "Walk":
            task = Walk(st.session_state.vault["task_counter"], task_time, priority_value, duration, recurrence)
        elif task_type == "Feed":
            task = Feed(st.session_state.vault["task_counter"], task_time, priority_value, food_type, portion_size, recurrence)
        elif task_type == "GiveMedicine":
            task = GiveMedicine(st.session_state.vault["task_counter"], task_time, priority_value, medication_name, dosage, recurrence)

        # Check for conflicts before adding
        selected_pet = st.session_state.vault["pets"][selected_pet_name]
        scheduler = Scheduler(st.session_state.vault["owner"])
        has_conflict = scheduler.check_for_conflicts(task, selected_pet)

        # Add task to selected pet
        selected_pet.add_task(task)

        if has_conflict:
            st.warning(f"⚠️ Warning: This task conflicts with an existing task for {selected_pet_name}!")
        else:
            st.success(f"✅ Added {task_type} task for {selected_pet_name}!")
        st.rerun()
else:
    st.info("👆 Please add at least one pet before scheduling tasks.")

st.divider()

# Display Schedule
st.subheader("📅 Generate Daily Schedule")
st.caption("View all tasks organized by time and priority.")

if st.session_state.vault["owner"] is not None and st.session_state.vault["pets"]:
    # Show current tasks for all pets with completion option
    with st.expander("View all tasks", expanded=True):
        for pet_name, pet in st.session_state.vault["pets"].items():
            if pet.tasks:
                st.markdown(f"**{pet_name}'s tasks:**")
                for idx, task in enumerate(pet.tasks):
                    task_type = task.__class__.__name__
                    recurrence_badge = f"🔄 {task.recurrence}" if task.recurrence != "none" else ""
                    status_badge = "✅" if task.status == "complete" else "⏳"

                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"{status_badge} {task_type} at {task.time_obj.strftime('%H:%M')} [Priority {task.priority}] {recurrence_badge}")
                    with col2:
                        if task.status == "pending":
                            if st.button("Complete", key=f"complete_{pet_name}_{idx}"):
                                st.session_state.vault["task_counter"] += 1
                                next_task = pet.complete_task(task, st.session_state.vault["task_counter"])
                                if next_task:
                                    st.success(f"✅ Task completed! Next {task_type} scheduled for {next_task.time_obj.strftime('%Y-%m-%d %H:%M')}")
                                else:
                                    st.success(f"✅ Task completed!")
                                st.rerun()
                            if st.button("Delete", key=f"delete_{pet_name}_{idx}"):
                                pet.tasks.remove(task)
                                st.success(f"🗑️ Task deleted!")
                                st.rerun()
            else:
                st.write(f"**{pet_name}:** No tasks yet")

    if st.button("Generate Schedule"):
        scheduler = Scheduler(st.session_state.vault["owner"])
        schedule = scheduler.generate_daily_schedule()

        if schedule:
            if "CONFLICT" not in "\n".join(schedule):
                st.success("✅ Schedule generated!")
                st.markdown("### 📅 Today's Schedule")


            # Check if there are any conflicts
            has_conflicts = any("CONFLICT" in line for line in schedule)
            if has_conflicts:
                st.warning("⚠️ Warning: Some tasks have time conflicts!")

            for line in schedule:
                if "CONFLICT" in line:
                    st.error(f"• {line}")
                else:
                    st.write(f"• {line}")
        else:
            st.info("No tasks scheduled yet. Add some tasks first!")
else:
    st.info("👆 Please create an owner and add pets with tasks to generate a schedule.")

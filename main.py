

# main.py

from datetime import datetime, timedelta

# Import classes from your system file
from pawpal_system import Owner, Pet, Scheduler, Walk, Feed, GiveMedicine


def main():
    # ----------------------
    # Create Owner
    # ----------------------
    owner = Owner(1, "Hamid", "hamid@email.com")

    # ----------------------
    # Create Pets
    # ----------------------
    pet1 = Pet(101, "Buddy", "Dog", "Golden Retriever", "Antibiotic")
    pet2 = Pet(102, "Mittens", "Cat", "Tabby", "Vitamin")

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # ----------------------
    # Create Tasks
    # ----------------------
    now = datetime.now()

    task1 = Walk(
        task_id=1,
        time_obj=now.replace(hour=11, minute=30, second=0, microsecond=0),
        time="11:30",
        priority=2,
        duration=30
    )

    task2 = Feed(
        task_id=2,
        time_obj=now.replace(hour=12, minute=45, second=0, microsecond=0),
        time= "12:45",
        priority=1,
        food_type="Dry Kibble",
        portion_size="1 cup"
    )

    task3 = GiveMedicine(
        task_id=3,
        time_obj=now.replace(hour=15, minute=45, second=0, microsecond=0),
        time="15:45",
        priority=3,
        medication_name="PetMed",
        dosage="5ml"
    )
    task4 = Walk(
        task_id=4,
        time_obj=now.replace(hour=12, minute=45, second=0, microsecond=0),
        time="12:45",
        priority=2,
        duration=30,
        recurrence="daily"
    )

    # ----------------------
    # Assign Tasks to Pets
    # ----------------------
    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)
    pet1.add_task(task4)

    # ----------------------
    # Print Today's Schedule
    # ----------------------
    print("\n===== Today's Schedule =====")
    scheduler = Scheduler(owner)
    daily_schedule = scheduler.generate_daily_schedule()
    print ("\n".join(daily_schedule))


if __name__ == "__main__":
    main()


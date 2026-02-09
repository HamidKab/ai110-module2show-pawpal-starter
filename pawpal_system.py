from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


# ----------------------
# Task (Abstract Class)
# ----------------------
class Task(ABC):
    def __init__(self, task_id: int, time: datetime, priority: int):
        self.task_id = task_id
        self.time = time
        self.priority = priority
        self.status = "pending"

    @abstractmethod
    def execute(self):
        pass

    def mark_complete(self):
        self.status = "complete"


# ----------------------
# Concrete Task Classes
# ----------------------
class Walk(Task):
    def __init__(self, task_id: int, time: datetime, priority: int, duration: int):
        super().__init__(task_id, time, priority)
        self.duration = duration

    def execute(self):
        print(f"Walking pet for {self.duration} minutes.")


class Feed(Task):
    def __init__(self, task_id: int, time: datetime, priority: int, food_type: str, portion_size: str):
        super().__init__(task_id, time, priority)
        self.food_type = food_type
        self.portion_size = portion_size

    def execute(self):
        print(f"Feeding pet {self.portion_size} of {self.food_type}.")


class GiveMedicine(Task):
    def __init__(self, task_id: int, time: datetime, priority: int, medication_name: str, dosage: str):
        super().__init__(task_id, time, priority)
        self.medication_name = medication_name
        self.dosage = dosage

    def execute(self):
        print(f"Giving {self.dosage} of {self.medication_name}.")


# ----------------------
# Pet Class
# ----------------------
class Pet:
    def __init__(self, pet_id: int, name: str, species: str, breed: str, medication_type: str):
        self.pet_id = pet_id
        self.name = name
        self.species = species
        self.breed = breed
        self.medication_type = medication_type
        self.appointments: List[str] = []
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_daily_schedule(self):
        return sorted(self.tasks, key=lambda t: t.time)


# ----------------------
# Owner Class
# ----------------------
class Owner:
    def __init__(self, owner_id: int, name: str, contact_info: str):
        self.owner_id = owner_id
        self.name = name
        self.contact_info = contact_info
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        self.pets.remove(pet)

    def view_tasks(self):
        for pet in self.pets:
            print(f"Tasks for {pet.name}:")
            for task in pet.tasks:
                print(f"- {task.__class__.__name__} at {task.time} [{task.status}]")

# ----------------------
# Scheduler Class
# ----------------------

class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_daily_schedule(self):
        all_tasks = []

        for pet in self.owner.pets:
            for task in pet.tasks:
                all_tasks.append((pet, task))

        # Sort tasks by time first, then priority (higher priority first)
        sorted_tasks = sorted(
            all_tasks,
            key=lambda item: (item[1].time, -item[1].priority)
        )

        # Convert to printable strings
        schedule_lines = []
        for pet, task in sorted_tasks:
            schedule_lines.append(
                f"{pet.name} - {task.__class__.__name__} at "
                f"{task.time.strftime('%H:%M')} "
                f"[Priority {task.priority}]"
            )

        return schedule_lines
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List
import warnings


# ----------------------
# Task (Abstract Class)
# ----------------------
class Task(ABC):
    def __init__(self, task_id: int, time_obj: datetime, priority: int, recurrence: str = "none"):
        self.task_id = task_id
        self.time_obj = time_obj
        self.priority = priority
        self.status = "pending"
        self.recurrence = recurrence  # "none", "daily", or "weekly"

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def create_next_occurrence(self, new_task_id: int):
        """Create a new instance of this task for the next occurrence"""
        pass

    def mark_complete(self, next_task_id: int = None):
        """
        Mark task as complete and return a new task if recurring.

        Args:
            next_task_id: ID for the next task instance (required if task is recurring)

        Returns:
            New Task instance if recurring, None otherwise
        """
        self.status = "complete"

        if self.recurrence == "none":
            return None

        if next_task_id is None:
            raise ValueError("next_task_id required for recurring tasks")

        return self.create_next_occurrence(next_task_id)


# ----------------------
# Concrete Task Classes
# ----------------------
class Walk(Task):
    def __init__(self, task_id: int, time_obj: datetime, priority: int, duration: int, recurrence: str = "none"):
        super().__init__(task_id, time_obj, priority, recurrence)
        self.duration = duration

    def execute(self):
        print(f"Walking pet for {self.duration} minutes.")

    def create_next_occurrence(self, new_task_id: int):
        """Create next Walk task based on recurrence"""
        if self.recurrence == "daily":
            next_time = self.time_obj + timedelta(days=1)
        elif self.recurrence == "weekly":
            next_time = self.time_obj + timedelta(weeks=1)
        else:
            return None

        return Walk(new_task_id, next_time, self.priority, self.duration, self.recurrence)


class Feed(Task):
    def __init__(self, task_id: int, time_obj: datetime, priority: int, food_type: str, portion_size: str, recurrence: str = "none"):
        super().__init__(task_id, time_obj, priority, recurrence)
        self.food_type = food_type
        self.portion_size = portion_size

    def execute(self):
        print(f"Feeding pet {self.portion_size} of {self.food_type}.")

    def create_next_occurrence(self, new_task_id: int):
        """Create next Feed task based on recurrence"""
        if self.recurrence == "daily":
            next_time = self.time_obj + timedelta(days=1)
        elif self.recurrence == "weekly":
            next_time = self.time_obj + timedelta(weeks=1)
        else:
            return None

        return Feed(new_task_id, next_time, self.priority, self.food_type, self.portion_size, self.recurrence)


class GiveMedicine(Task):
    def __init__(self, task_id: int, time_obj: datetime, priority: int, medication_name: str, dosage: str, recurrence: str = "none"):
        super().__init__(task_id, time_obj, priority, recurrence)
        self.medication_name = medication_name
        self.dosage = dosage

    def execute(self):
        print(f"Giving {self.dosage} of {self.medication_name}.")

    def create_next_occurrence(self, new_task_id: int):
        """Create next GiveMedicine task based on recurrence"""
        if self.recurrence == "daily":
            next_time = self.time_obj + timedelta(days=1)
        elif self.recurrence == "weekly":
            next_time = self.time_obj + timedelta(weeks=1)
        else:
            return None

        return GiveMedicine(new_task_id, next_time, self.priority, self.medication_name, self.dosage, self.recurrence)


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
        return sorted(self.tasks, key=lambda t: t.time_obj)

    def complete_task(self, task: Task, next_task_id: int):
        """
        Mark a task as complete and handle recurring tasks.

        Args:
            task: The task to mark complete
            next_task_id: ID for the next task instance (if recurring)

        Returns:
            The next task instance if recurring, None otherwise
        """
        next_task = task.mark_complete(next_task_id)
        if next_task:
            self.add_task(next_task)
        return next_task

    def _get_task_time_range(self, task: Task):
        """
        Calculate the start and end time for a task.

        Returns:
            (start_time, end_time) tuple
            For instantaneous tasks, start_time == end_time
        """
        start_time = task.time_obj
        if isinstance(task, Walk):
            end_time = start_time + timedelta(minutes=task.duration)
        else:
            # Feed and GiveMedicine are instantaneous
            end_time = start_time
        return start_time, end_time




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
                print(f"- {task.__class__.__name__} at {task.time_obj.strftime('%H:%M')} [{task.status}]")

# ----------------------
# Scheduler Class
# ----------------------

class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
    
    def check_for_conflicts(self, new_task: Task, pet: Pet):
        new_start, new_end = pet._get_task_time_range(new_task)

        for existing_task in pet.tasks:
            if existing_task.status == "complete":
                continue  # Skip completed tasks

            # Don't compare a task with itself
            if existing_task.task_id == new_task.task_id:
                continue

            existing_start, existing_end = pet._get_task_time_range(existing_task)

            # Check for time overlap (using <= to handle instantaneous tasks)
            # Two time ranges [start1, end1] and [start2, end2] overlap if:
            # start1 <= end2 AND start2 <= end1
            if new_start <= existing_end and existing_start <= new_end:
                warnings.warn(
                    f"Conflict detected for {pet.name}: "
                    f"{new_task.__class__.__name__} at {new_task.time_obj.strftime('%H:%M')} overlaps with "
                    f"{existing_task.__class__.__name__} at {existing_task.time_obj.strftime('%H:%M')}"
                )
                return True  # Conflict detected

        return False  # No conflict

    def generate_daily_schedule(self):
        all_tasks = []

        for pet in self.owner.pets:
            for task in pet.tasks:
                all_tasks.append((pet, task))

        # Sort tasks by time first, then priority (higher priority first)
        sorted_tasks = sorted(
            all_tasks,
            key=lambda item: (item[1].time_obj, -item[1].priority)
        )


        # Convert to printable strings
        schedule_lines = []
        for pet, task in sorted_tasks:
            conflict = self.check_for_conflicts(task, pet)

            line = (
                f"{pet.name} - {task.__class__.__name__} at "
                f"{task.time_obj.strftime('%H:%M')} "
                f"[Priority {task.priority}]"
            )
            if conflict:
                line += " ⚠️ CONFLICT"
            schedule_lines.append(line)


        return schedule_lines
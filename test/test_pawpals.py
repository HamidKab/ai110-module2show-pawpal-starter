import unittest
from datetime import datetime, timedelta
import warnings

from pawpal_system import Pet, Walk, Feed, GiveMedicine, Owner, Scheduler


class TestPawPalSystem(unittest.TestCase):

    def test_mark_complete_changes_status(self):
        """Verify that calling mark_complete() updates the task status."""
        task = Walk(
            task_id=1,
            time_obj=datetime.now(),
            priority=1,
            duration=20
        )

        # Initial state
        self.assertEqual(task.status, "pending")

        # Action
        task.mark_complete()

        # Expected result
        self.assertEqual(task.status, "complete")

    def test_add_task_increases_pet_task_count(self):
        """Verify that adding a task increases the pet's task list size."""
        pet = Pet(1, "Buddy", "Dog", "Golden Retriever", "Antibiotic")

        initial_count = len(pet.tasks)

        task = Walk(
            task_id=2,
            time_obj=datetime.now(),
            priority=2,
            duration=30
        )

        pet.add_task(task)

        self.assertEqual(len(pet.tasks), initial_count + 1)

    def test_pet_with_no_tasks(self):
        """Verify that a new pet has an empty task list."""
        pet = Pet(1, "Max", "Cat", "Persian", "None")

        self.assertEqual(len(pet.tasks), 0)
        self.assertIsInstance(pet.tasks, list)

    def test_pet_with_no_tasks_daily_schedule(self):
        """Verify that get_daily_schedule returns empty list for pet with no tasks."""
        pet = Pet(1, "Luna", "Dog", "Poodle", "None")

        schedule = pet.get_daily_schedule()

        self.assertEqual(len(schedule), 0)
        self.assertIsInstance(schedule, list)

    def test_conflict_detection_overlapping_walks(self):
        """Verify that scheduler detects conflicts between overlapping walk tasks."""
        owner = Owner(1, "John Doe", "john@example.com")
        pet = Pet(1, "Buddy", "Dog", "Golden Retriever", "None")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        # Create two walks that overlap
        base_time = datetime(2026, 2, 11, 10, 0)
        walk1 = Walk(task_id=1, time_obj=base_time, priority=1, duration=30)
        walk2 = Walk(task_id=2, time_obj=base_time + timedelta(minutes=15), priority=1, duration=30)

        pet.add_task(walk1)

        # Check for conflict when adding second walk
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            has_conflict = scheduler.check_for_conflicts(walk2, pet)

            self.assertTrue(has_conflict)
            self.assertEqual(len(w), 1)
            self.assertIn("Conflict detected", str(w[0].message))

    def test_conflict_detection_instantaneous_tasks_same_time(self):
        """Verify that scheduler detects conflicts for instantaneous tasks at the same time."""
        owner = Owner(1, "Jane Doe", "jane@example.com")
        pet = Pet(1, "Whiskers", "Cat", "Siamese", "Insulin")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        # Create two feeds at the same time
        feed_time = datetime(2026, 2, 11, 8, 0)
        feed1 = Feed(task_id=1, time_obj=feed_time, priority=2, food_type="Wet Food", portion_size="1 cup")
        feed2 = Feed(task_id=2, time_obj=feed_time, priority=2, food_type="Dry Food", portion_size="0.5 cup")

        pet.add_task(feed1)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            has_conflict = scheduler.check_for_conflicts(feed2, pet)

            self.assertTrue(has_conflict)
            self.assertEqual(len(w), 1)

    def test_no_conflict_non_overlapping_tasks(self):
        """Verify that scheduler does not detect conflicts for non-overlapping tasks."""
        owner = Owner(1, "Bob Smith", "bob@example.com")
        pet = Pet(1, "Rex", "Dog", "German Shepherd", "None")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        # Create tasks that don't overlap
        base_time = datetime(2026, 2, 11, 9, 0)
        walk = Walk(task_id=1, time_obj=base_time, priority=1, duration=30)
        feed = Feed(task_id=2, time_obj=base_time + timedelta(hours=2), priority=2, food_type="Kibble", portion_size="2 cups")

        pet.add_task(walk)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            has_conflict = scheduler.check_for_conflicts(feed, pet)

            self.assertFalse(has_conflict)
            self.assertEqual(len(w), 0)

    def test_conflict_ignores_completed_tasks(self):
        """Verify that completed tasks are not checked for conflicts."""
        owner = Owner(1, "Alice Johnson", "alice@example.com")
        pet = Pet(1, "Fluffy", "Cat", "Maine Coon", "None")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        # Create two tasks at same time, mark first as complete
        task_time = datetime(2026, 2, 11, 14, 0)
        feed1 = Feed(task_id=1, time_obj=task_time, priority=1, food_type="Tuna", portion_size="1 can")
        feed2 = Feed(task_id=2, time_obj=task_time, priority=1, food_type="Chicken", portion_size="1 can")

        feed1.mark_complete()  # Mark as complete
        pet.add_task(feed1)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            has_conflict = scheduler.check_for_conflicts(feed2, pet)

            # No conflict because feed1 is complete
            self.assertFalse(has_conflict)
            self.assertEqual(len(w), 0)

    def test_daily_schedule_sorting_by_time(self):
        """Verify that get_daily_schedule returns tasks sorted by time."""
        pet = Pet(1, "Charlie", "Dog", "Beagle", "None")

        # Add tasks in random order
        time1 = datetime(2026, 2, 11, 15, 0)
        time2 = datetime(2026, 2, 11, 8, 0)
        time3 = datetime(2026, 2, 11, 12, 0)

        task1 = Walk(task_id=1, time_obj=time1, priority=1, duration=20)
        task2 = Feed(task_id=2, time_obj=time2, priority=2, food_type="Kibble", portion_size="1 cup")
        task3 = GiveMedicine(task_id=3, time_obj=time3, priority=3, medication_name="Painkiller", dosage="1 tablet")

        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)

        schedule = pet.get_daily_schedule()

        # Should be sorted by time: task2 (8:00), task3 (12:00), task1 (15:00)
        self.assertEqual(schedule[0].task_id, 2)
        self.assertEqual(schedule[1].task_id, 3)
        self.assertEqual(schedule[2].task_id, 1)

    def test_recurring_task_creates_next_occurrence(self):
        """Verify that marking a recurring task complete creates the next occurrence."""
        pet = Pet(1, "Daisy", "Dog", "Labrador", "Antibiotic")

        # Create a daily recurring walk
        walk = Walk(
            task_id=1,
            time_obj=datetime(2026, 2, 11, 10, 0),
            priority=1,
            duration=30,
            recurrence="daily"
        )

        pet.add_task(walk)
        initial_count = len(pet.tasks)

        # Complete the task
        next_task = pet.complete_task(walk, next_task_id=2)

        # Should create a new task
        self.assertIsNotNone(next_task)
        self.assertEqual(len(pet.tasks), initial_count + 1)
        self.assertEqual(next_task.time_obj, walk.time_obj + timedelta(days=1))
        self.assertEqual(walk.status, "complete")

    def test_non_recurring_task_no_next_occurrence(self):
        """Verify that non-recurring tasks don't create next occurrence."""
        pet = Pet(1, "Rocky", "Dog", "Bulldog", "None")

        # Create a non-recurring feed
        feed = Feed(
            task_id=1,
            time_obj=datetime(2026, 2, 11, 9, 0),
            priority=1,
            food_type="Wet Food",
            portion_size="1 cup",
            recurrence="none"
        )

        pet.add_task(feed)
        initial_count = len(pet.tasks)

        # Complete the task
        next_task = pet.complete_task(feed, next_task_id=2)

        # Should not create a new task
        self.assertIsNone(next_task)
        self.assertEqual(len(pet.tasks), initial_count)
        self.assertEqual(feed.status, "complete")

    def test_scheduler_empty_schedule(self):
        """Verify that scheduler handles owner with no pets or tasks."""
        owner = Owner(1, "Empty Owner", "empty@example.com")
        scheduler = Scheduler(owner)

        schedule = scheduler.generate_daily_schedule()

        self.assertEqual(len(schedule), 0)
        self.assertIsInstance(schedule, list)

    def test_scheduler_with_multiple_pets(self):
        """Verify that scheduler generates schedule for multiple pets."""
        owner = Owner(1, "Multi Pet Owner", "multi@example.com")
        pet1 = Pet(1, "Spot", "Dog", "Dalmatian", "None")
        pet2 = Pet(2, "Mittens", "Cat", "Tabby", "None")

        owner.add_pet(pet1)
        owner.add_pet(pet2)

        base_time = datetime(2026, 2, 11, 10, 0)
        task1 = Walk(task_id=1, time_obj=base_time, priority=1, duration=20)
        task2 = Feed(task_id=2, time_obj=base_time + timedelta(hours=1), priority=2, food_type="Fish", portion_size="1 can")

        pet1.add_task(task1)
        pet2.add_task(task2)

        scheduler = Scheduler(owner)
        schedule = scheduler.generate_daily_schedule()

        self.assertEqual(len(schedule), 2)
        self.assertIn("Spot", schedule[0])
        self.assertIn("Mittens", schedule[1])


if __name__ == "__main__":
    unittest.main()
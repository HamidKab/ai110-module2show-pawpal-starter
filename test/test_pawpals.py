import unittest
from datetime import datetime

from pawpal_system import Pet, Walk


class TestPawPalSystem(unittest.TestCase):

    def test_mark_complete_changes_status(self):
        """Verify that calling mark_complete() updates the task status."""
        task = Walk(
            task_id=1,
            time=datetime.now(),
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
            time=datetime.now(),
            priority=2,
            duration=30
        )

        pet.add_task(task)

        self.assertEqual(len(pet.tasks), initial_count + 1)


if __name__ == "__main__":
    unittest.main()
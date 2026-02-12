# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

### Testing PawPal+
 run with python -m unittest test/test_pawpals.py
 My test cover:
test_pet_with_no_tasks - Verifies new pets have empty task lists

test_pet_with_no_tasks_daily_schedule - Tests schedule generation for pets without tasks

test_conflict_detection_overlapping_walks - Tests overlapping Walk tasks that conflict

test_conflict_detection_instantaneous_tasks_same_time - Tests Feed/Medicine tasks at the same time

test_no_conflict_non_overlapping_tasks - Ensures non-overlapping tasks don't trigger conflicts

test_conflict_ignores_completed_tasks - Verifies completed tasks are excluded from conflict checking

test_daily_schedule_sorting_by_time - Ensures tasks are sorted chronologically

test_scheduler_empty_schedule - Tests scheduler with no pets/tasks

test_scheduler_with_multiple_pets - Tests schedule generation across multiple pets

test_recurring_task_creates_next_occurrence - Verifies daily recurring tasks create next instance

test_non_recurring_task_no_next_occurrence - Ensures one-time tasks don't recur

 I feel like the system is running at 4.5 stars. I only dont give it 5 stars because theres always might be little bugs that don't break the system or come up in test cases. Users are like little goblins that can find any type of bug so I wont say its fullproof
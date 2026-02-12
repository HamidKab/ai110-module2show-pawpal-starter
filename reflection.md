# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My intial design consist of Owners, pets, and task with the task linking to different method classes.
for owner there's:
owner id
name 
addPet()

Pet:
pet id
name
species 
breed
addTask

Task:
task id
Priority 
time


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
My design didn't change but it expanded on tasks i didnt focus on in my explanation

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

my scheduler sorted by time then priority 
I thought time would be the most important because i don't allow overlapping time tasks so theres no point in sorting by priority 


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
my scheduler does not allow for any time overlaps which may cause issues in situations where pets need to take medicine with there food, but i think its a fair tradeoff because it catches a lot of errors.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I used AI to help me plan and debug some of my mistakes. Originally i tried to write the conflict catcher and ran into some bugs and had claude the bug it

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
Originally claude tried to put the conflict catch in the Pet class but that didnt make sense to me so I rejected the method and moved a similar method the the scheduler class

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
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


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
Im sure that 8/10 times the scheduler runs as designed. I feel like I caught a lot of edge cases but theres always some youre not thinking of

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The changes to the backend and UI that i made without the help of AI

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If i had more time id put dates into consideration not just hours
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned how to use claude and how it differed from  other coding assistants

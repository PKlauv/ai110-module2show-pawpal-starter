# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design has four main classes: Task, Pet, Owner, and Scheduler. I used Python dataclasses for Task and Pet since they're mostly data holders, and regular classes for Owner and Scheduler since they have more complex behavior.

- **Task** holds all the info for a single activity — what it is, when it happens, how long it takes, its priority level, and whether it repeats. It also tracks if it's been completed.
- **Pet** represents a pet with basic info (name, species, age) and keeps a list of all its tasks. It can add/remove tasks and filter for pending ones.
- **Owner** manages multiple pets. It's basically the entry point — you create an owner, add pets to them, and can pull all tasks across every pet at once.
- **Scheduler** is the brain of the system. It takes an Owner and handles all the smart stuff like sorting tasks by time, filtering by pet or status, detecting conflicts, and managing recurring tasks.

The relationships are pretty straightforward: an Owner has many Pets, each Pet has many Tasks, and the Scheduler works through the Owner to access everything. I kept it simple on purpose — didn't want to overcomplicate it with inheritance or anything when composition works fine here.

**b. Design changes**

Yeah, a couple things changed once I started actually building it out. The biggest one was how the Scheduler interacts with tasks. Originally I had the Scheduler storing its own copy of tasks, but that got messy fast — if you marked something complete through the Scheduler, the Pet's task list wouldn't update. So I changed it so the Scheduler always goes through the Owner to get tasks. That way there's one source of truth and everything stays in sync.

I also added a `due_date` field to Task that wasn't in my original UML. I realized I needed it for the recurrence logic — when you mark a daily task complete, the system needs to know what date to schedule the next one for, and just having a time string wasn't enough.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three main constraints: time of day, priority level (high/medium/low), and task frequency (once, daily, weekly). Time is the primary sorting key for the daily schedule since a pet owner needs to see what comes first in the day. Priority is used as a secondary way to view tasks — you can sort by priority to see what's most urgent.

I decided time mattered most because at the end of the day, a schedule needs to be chronological to be useful. Priority helps when you're deciding what to skip if you're short on time, but the default view should just be "what do I do next."

**b. Tradeoffs**

The biggest tradeoff is in conflict detection — my scheduler only flags exact time matches rather than checking for overlapping durations. So if you have a 60-minute vet appointment at 9:00 and a walk at 9:30, the system won't catch that overlap. It only warns you if two tasks for the same pet are both at exactly 9:00.

This is reasonable for a pet care app because most tasks are short (feeding, medication) and owners usually schedule them at distinct times. Implementing full duration-based overlap detection would add a lot of complexity for a case that doesn't come up that often in practice. If I had more time, I'd probably add it, but for now the exact-match approach catches the most common mistake — accidentally double-booking the same time slot.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

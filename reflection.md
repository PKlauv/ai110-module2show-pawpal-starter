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

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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

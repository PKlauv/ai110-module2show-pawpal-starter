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

I used AI pretty heavily throughout this project, mainly through VS Code Copilot. In the design phase, I described what the app needed to do and had Copilot generate a Mermaid.js class diagram, which saved a ton of time compared to drawing one from scratch. I used it to scaffold the initial class skeletons too — just gave it the UML and asked for Python dataclass stubs.

During implementation, I used Copilot's inline suggestions and chat to flesh out methods. The most helpful prompts were specific ones like "how should the Scheduler retrieve all tasks from the Owner's pets?" rather than vague stuff like "write my scheduler." Asking it to explain *how* things should connect was way more useful than just asking it to write code.

I also used separate chat sessions for different phases — one for design brainstorming, one for implementation questions, and one focused entirely on testing. That actually helped a lot because the context didn't get muddied up with unrelated stuff from earlier phases.

**b. Judgment and verification**

When I asked Copilot to generate the conflict detection logic, it initially suggested checking every pair of tasks using nested loops — comparing all tasks against all other tasks regardless of pet. That would've flagged conflicts between tasks for different pets, which doesn't make sense (I can walk Mochi and feed Whiskers at the same time). I modified it to only flag conflicts when two tasks for the *same pet* are at the same time, using a dictionary keyed on `(pet_name, time)` which is also more efficient than the nested loop approach.

I verified the change by adding specific test cases — one where the same pet has two tasks at the same time (should flag), and one where different pets have tasks at the same time (should not flag). Both passed, which confirmed the logic was right.

---

## 4. Testing and Verification

**a. What you tested**

I wrote 20 automated tests covering the main behaviors:

- **Basic operations**: Task completion status toggle, string representation, adding/removing tasks from pets, filtering pending tasks, adding/retrieving pets from an owner, aggregating tasks across pets.
- **Sorting**: Verified that `sort_by_time()` returns tasks in chronological order and `sort_by_priority()` orders them high → medium → low.
- **Filtering**: Tested filtering tasks by pet name and by completion status.
- **Conflict detection**: Confirmed that two tasks at the same time for the same pet get flagged, but two tasks at the same time for different pets don't.
- **Recurrence**: Verified that completing a daily task creates a new one for tomorrow, a weekly task creates one for next week, and a one-time task doesn't recur.
- **Edge cases**: Tested a pet with no tasks, an owner with no pets, and a scheduler with an empty owner — all return empty lists without crashing.

These tests are important because the scheduler has a lot of interconnected logic. Without tests, it'd be easy for a change in one method to silently break something else.

**b. Confidence**

I'd give it a solid 4 out of 5 stars. The core scheduling, sorting, filtering, and recurrence all work correctly based on my tests. The main gap is the conflict detection only catches exact time matches, not overlapping time ranges. If I had more time, I'd test edge cases like tasks at midnight (00:00), tasks with zero duration, and what happens if you try to mark a task complete that doesn't exist.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with how clean the architecture turned out. The separation between the logic layer (`pawpal_system.py`) and the UI (`app.py`) made development really smooth — I could test everything in the terminal with `main.py` before touching the Streamlit side. The CLI-first approach the assignment recommended actually works really well in practice.

**b. What you would improve**

If I had another iteration, I'd redesign the conflict detection to check for overlapping time ranges instead of just exact matches. I'd also add data persistence — right now everything resets when you close the app because it's all in memory. Adding JSON save/load would make it actually usable day-to-day. The UI could also use some work — maybe a calendar view instead of just a table.

**c. Key takeaway**

The biggest thing I learned is that AI is most useful when you already know what you want to build. The UML-first approach forced me to think through the design before writing any code, and that made the AI suggestions way more useful because I could evaluate them against my design. When I just asked AI to "build a scheduler" without a clear plan, the suggestions were generic and often overcomplicated. But when I said "here's my UML, implement this specific method," the output was solid and I could verify it quickly. Being the architect — knowing the *what* and *why* — is what makes AI collaboration actually productive.

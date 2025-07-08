# sat
-  **Website Link**: - https://sat-p36z.onrender.com/
 
# 📚 SAT-Based Student Room Scheduling Solver

This project implements a constraint-based **room scheduling system** using **Boolean Satisfiability (SAT)** — one of the foundational problems in computer science and artificial intelligence.

We reduce the problem of assigning students to quiz rooms (given preferences and room capacities) into a **CNF (Conjunctive Normal Form)** formula, which is then solved using a **custom recursive SAT solver**. The system guarantees valid assignments while respecting student preferences and room capacity limits — or proves that no valid assignment exists.

---

## 🚀 Features

- 🔢 **SAT Reduction Engine**: Converts real-world constraints into Boolean logic.
- 🧮 **Pure-Python SAT Solver**: No external libraries required — a recursive DPLL-style solver implemented from scratch.
- 🎯 **Student Preference Handling**: Ensures students are only assigned to rooms they are willing to attend.
- 🧠 **Capacity Constraints**: Enforces strict room limits using combinatorial logic.
- ❌ **Oversubscription Protection**: Prevents more students than a room can accommodate from being assigned.
- ✅ **Guarantees Valid Assignment**: Returns one possible solution (if any) or proves unsatisfiability.

---

## 📖 Problem Statement

**Given:**

- A dictionary of students, where each student has a set of **preferred rooms**.
- A dictionary of rooms, each with a specified **capacity**.

**Goal:**

- Assign each student to **exactly one** of their preferred rooms, such that:
  - No student is assigned to a room they didn't select.
  - No room exceeds its capacity.
  - If such an assignment exists, return it; otherwise, report unsatisfiability.

---

## 🧪 Example

```python
student_preferences = {
    "Alice": {"session1", "session2"},
    "Bob": {"session3"},
    "Charles": {"session3"},
}

room_capacities = {
    "session1": 1,
    "session2": 1,
    "session3": 3,
}

cnf = boolify_scheduling_problem(student_preferences, room_capacities)
solution = satisfying_assignment(cnf)
print(solution)

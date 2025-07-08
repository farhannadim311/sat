"""
6.101 Lab:
SAT Solver
"""

#!/usr/bin/env python3

# import typing  # optional import
# import pprint  # optional import
import doctest
import sys

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS
def flatten_recursive(lst):
    flat = []
    for item in lst:
        if isinstance(item, list):
            flat.extend(flatten_recursive(item))
        else:
            flat.append(item)
    return flat

def update_formula(formula, assignment):
    """
    Update a CNF formula based on a given variable assignment.

    This function takes a CNF formula (a list of clauses, where each clause is a list of (variable, polarity) tuples)
    and a single variable assignment (a variable name and a Boolean value), and returns a simplified CNF formula
    that reflects the impact of the assignment.

    The function removes any clause that is satisfied by the assignment and removes from the remaining clauses
    any literals that are made false by the assignment. If any clause becomes empty after simplification,
    the formula becomes unsatisfiable.

    Args:
        formula (list[list[tuple[str, bool]]]): The original CNF formula.
        assignment (tuple[str, bool]): A variable assignment to apply (e.g., ('x', True)).

    Returns:
        list[list[tuple[str, bool]]]: The updated CNF formula after applying the assignment.
    """
    updated = []
    for clause in formula:
        if assignment in clause:
            continue
        new_clause = []
        for var, polarity in clause:
            if var == assignment[0] and polarity != assignment[1]:
                continue
            new_clause.append((var, polarity))
        updated.append(new_clause)
    
    return updated
    

def copy_cnf(formula):
    return [[(var, polarity) for var, polarity in clause] for clause in formula]





def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> T, F = True, False
    >>> x = satisfying_assignment([[('a', T), ('b', F), ('c', T)]])
    >>> x.get('a', None) is T or x.get('b', None) is F or x.get('c', None) is T
    True
    >>> satisfying_assignment([[('a', T)], [('a', F)]])
    """
    if not formula:
        return {}
    for clause in formula:
        if not clause:
            return None
    clause = min(formula, key = len)
    for var, val in clause:
        assignment = (var, val)
        simplified = update_formula(formula, assignment)
        result = satisfying_assignment(simplified)
        if result is not None:
            return {var: val} | result
    return None

              



def boolify_scheduling_problem(student_preferences, room_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of room names (strings) that work for that student

    room_capacities: a dictionary mapping each room name to a positive integer
                     for how many students can fit in that room

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up

    We assume no student or room names contain underscores.
    """
    rule_1 = students_in_desired_sessions(student_preferences)
    rule_2 = students_in_one_session(student_preferences, room_capacities)
    rule_3 = no_oversubscribed_rooms(student_preferences, room_capacities)
    cnf = rule_1 + rule_2 + rule_3
    return cnf
def students_in_desired_sessions(student_preferences):
    """
    Given a dictionary mapping students to their preferred rooms, return a CNF formula
    that ensures each student is assigned to at least one of their preferred rooms.

    Each clause in the CNF formula corresponds to one student and contains a disjunction
    of literals, where each literal asserts that the student is assigned to a room they prefer.

    Args:
        student_preferences (dict[str, list[str]]): A dictionary mapping each student name
        to a list of their preferred room names.

    Returns:
        list[list[tuple[str, bool]]]: A CNF formula, where each clause is a list of literals.
        Each literal is a tuple (variable_name, True), indicating the student should be in that room.
    """
    lst = []
    for student in student_preferences:
        preference = []
        for room in student_preferences[student]:
            preference.append((student +"_"+ room, True))
        lst.append(preference)
    return lst

def pairs_of_room(rooms):
    pairs = []
    for i in range(len(rooms)):
        for j in range(i + 1, len(rooms)):
            pairs.append((rooms[i], rooms[j]))
    return pairs
     

def combine(lst, k, start=0, path=None, result=None):
    """
    Recursively generate all combinations of k elements from lst.
    """
    if path is None:
        path = []
    if result is None:
        result = []

    if len(path) == k:
        result.append(path[:])
        return result

    for i in range(start, len(lst)):
        path.append(lst[i])
        combine(lst, k, i + 1, path, result)
        path.pop()

    return result


        


def students_in_one_session(student_preferences, room_capacities):
    """
    Generate a CNF formula ensuring each student is assigned to at most one room.

    For each student, and for every pair of distinct rooms, this function adds a clause
    asserting that the student cannot be assigned to both rooms simultaneously.
    This is expressed in CNF as (¬student_room1 ∨ ¬student_room2).

    Args:
        student_preferences (dict[str, list[str]]): Dictionary mapping each student to their preferred rooms.
        room_capacities (dict[str, int]): Dictionary of all available rooms and their capacities (only keys are used).

    Returns:
        list[list[tuple[str, bool]]]: A CNF formula enforcing mutual exclusivity per student across room pairs.
    """
    lst = []
    room_list = list(room_capacities.keys())
    room_pairs = pairs_of_room(room_list)
    
    for student in student_preferences:
        for room1, room2 in room_pairs:
            clause = [
                (f"{student}_{room1}", False),
                (f"{student}_{room2}", False)
            ]
            lst.append(clause)
    
    return lst


def no_oversubscribed_rooms(students_preferences, room_capacities):
    """
    Generate CNF formula to ensure no room has more students than its capacity.

    Args:
        students (list[str]): List of all student names.
        room_capacities (dict[str, int]): Mapping from room names to their capacities.

    Returns:
        list[list[tuple[str, bool]]]: CNF clauses, each preventing c+1 students from sharing a room.
    """
    cnf = []
    total_students = len(students_preferences)
    students = list(students_preferences.keys())
    for room in room_capacities:
        cap = room_capacities[room]
        if cap >= total_students:
            continue
        student_groups = combine(students, cap + 1)
        for group in student_groups:
            clause = []
            for student in group:
                clause.append((student + "_" + room, False))
            cnf.append(clause)
    return cnf


    

if __name__ == "__main__":
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)

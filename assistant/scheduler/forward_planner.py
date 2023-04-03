from assistant.scheduler.unification import parse, unification, unify
from typing import List, Dict, Set, Union, Tuple
from copy import deepcopy


def composition(result1: Dict[str, str], result2: Dict[str, str]) -> Dict[str, str]:
    """
    composition

    Performs composition of the substitution dictionaries. Given two substitution dictionaries this function will return
     the merged dictionary with some exceptions

    result1 Dict[str, str]: Result1 can be None or a dictionary of substitutions
    result2 Dict[str, str]: Result2 can be None or a dictionary of substitutions
    """
    if result1 is None or result2 is None:
        return None

    merged = {**result1, **result2}

    for key in merged:
        if key in result1 and key in result2:
            if result1[key] != result2[key]:
                # There is a variable being assigned to twice
                return {}

    return merged


def action_successors(state: List[str], preconditions_: List[str], prior_substitutions: Dict[str,str] = {}) -> List[Dict[str, str]]:
    """
    action_successors

    The inner recursion. This function takes an "I want every single valid state!" approach where a path is valid if it
     satisfies all of the preconditions. Given a set of preconditions and the state, this recursive function finds all
     possible paths that satisfy the preconditions through DFS.

    state List[str]: List of predicate facts that describe the state
    preconditions List[str]: List of predicates with variables that describe the preconditions for an action
    prior_substitutions Dict[str, str]: Prior substitution dictionary. Default of {} for first iteration

    returns List[Dict[str, str]]: List of substitution dictionaries. [] for no possible substitutions
    """
    preconditions, substitutions, new_states, res_sub_list = deepcopy(preconditions_), [], [], []
    if len(preconditions) == 0:
        return prior_substitutions
    for s_ in state:
        sub = unify(s_, preconditions[0])
        if sub and sub is not None:
            if composition(prior_substitutions, sub) == {}:
                continue
            substitutions.append(composition(prior_substitutions, sub))
            new_state = deepcopy(state)
            new_state.remove(s_)
            new_states.append(new_state)
    for new_state, sub in zip(new_states, substitutions):
        res = action_successors(new_state, preconditions[1:], sub)
        if type(res) == list:
            res_sub_list.extend(res)
        else:
            res_sub_list.append(res)
    return [sub_list for sub_list in res_sub_list if sub_list != {}]


def successors(state: List[str], actions: Dict[str, str]):
    """
    successors

    For each action, apply it to the state with the action_successors function. This returns a dictionary with a list
    of substitution lists accessible by action names.

    state List[str]: List of predicate facts that describe the state
    actions Dict[str, str]: Dictionary of actions for scenario

    returns List[Dict[str, str]]: List of substitution dictionaries. [] for no possible substitutions
    """
    substitution_lists = {}
    for action_name in actions:
        # print(action_name)
        preconditions = actions[action_name]["conditions"]

        substitution_lists[action_name] = action_successors(state, preconditions)

    return substitution_lists


def sub_expression(expression: Union[List[str], str], sub_list: Dict[str, str]) -> List[str]:
    """
    sub_expression

    Helper function that uses substitution lists to sub strings in for variables in an expression

    expression Union[List[str], str]: List of predicates or a single predicate
    sub_list Dict[str, str]: Substitution dictionary

    returns List[str]: List of predicates that have been filled in with the substitution dictionary
    """
    new_expression = deepcopy(expression)

    if type(expression) == list:
        for sub in sub_list:
            for i in range(len(new_expression)):
                new_expression[i] = new_expression[i].replace(sub, sub_list[sub])
    elif type(expression) == str:
        for sub in sub_list:
            new_expression = new_expression.replace(sub, sub_list[sub])

    return new_expression


def get_add_delete_from_subs(action: Dict[str, str],
                             sub_lists: List[Dict[str, str]]) -> List[Tuple[str, List[str], List[str]]]:
    """
    get_add_delete_from_subs

    Substitutes each substitution list for the variables in add and delete for the action. Relies on sub_expression for
     the substitution.

    action Dict[str, str]: Action dictionary
    sub_lists List[Dict[str, str]]: Lists of substitution dictionaries

    returns List[Tuple[str, List[str], List[str]]]: List actions, adds, and deletes
    """
    add_terms = [sub_expression(action["add"], sub_list) for sub_list in sub_lists]
    delete_terms = [sub_expression(action["delete"], sub_list) for sub_list in sub_lists]
    action_terms = [sub_expression(action["action"], sub_list) for sub_list in sub_lists]

    transition_terms = [(action, add, delete) for action, add, delete in zip(action_terms, add_terms, delete_terms)]

    return transition_terms


def state_score(state: List[str], goal: List[str]) -> int:
    """
    score

    Scores a state based on how many facts it has that also exists in the goal.

    action Dict[str, str]: Action dictionary
    sub_lists List[Dict[str, str]]: Lists of substitution dictionaries

    returns int: score
    """
    score = 0
    state_set = set(state)
    for goal_term in goal:
        if goal_term in state_set:
            score += 1
        else:
            score -= 1
    return score


def revise_state(state: List[str], add: List[str], delete: List[str]) -> List[str]:
    """
    revise_state

    Adds and removes states from the current state list. Also, sorts the state so the less complex terms come first

    state List[str]: The list of facts for the state
    add List[str]: The list of facts to add
    delete List[str]: The list of facts to delete

    returns List[str]: The revised state
    """
    state_ = set(deepcopy(state))
    state_ = state_.union(add)
    state_ -= set(delete)
    state_ = list(state_)
    state_.sort(key=lambda y: len(parse(y)))

    return state_


def forward_planner(start_state: List[str],
                    goal: List[str],
                    actions: Dict,
                    plan: List[str] = [],
                    explored_list: List[Set[str]] = [],
                    debug: bool = False):
    """
    forward_planner

    Recursive forward planning algorithm. The base case for this function is when the current state is the goal state.
    The algorithm uses the successors function to yield the children of this current state, which is essentially all
    of the possible ways that the actions can be validly applied. Those children are given as substitution lists which
    are then substituted into the add/delete lists for each action with the get_add_delete_from_subs function. All of
    those add/delete terms are used to create the child state lists with the revise_state function and sorted a simple
    scorer to sort by the child states that get the closest to the goal. Each child state is added to the explored list
    (or skipped if it has been visited), the action is added to the plan and the recursion continues.

    start_state List[str]: The list of facts for the state
    goal List[str]: The list of facts that describe the goal state
    actions Dict: The dictionary of actions to navigate the states
    plan List[str]: The list of actions to get from the start state to the goal [a1, a2, a3]. if debug is true, this
     includes the states [s0, a1, s1, a2, s2, a3, s3]. Default of [] for starting the algorithm
    explored_list List[Set[str]]: The list of states (as sets) that have been explored. Default []
    debug bool: Whether to include the intermediary states in the plan

    returns List[Union[List[str], str]: The plan. Can include intermediary states actions.
    """
    if all([goal_term in set(start_state) for goal_term in goal]):
        return plan + [start_state] if debug else plan

    successor_sublists, action_names, transitions = successors(start_state, actions), list(actions.keys()), []
    for name in action_names:
        transitions.extend(get_add_delete_from_subs(actions[name], successor_sublists[name]))

    new_transitions = []
    for action, add, delete in transitions:
        revised_state = revise_state(start_state, add, delete)
        # f(n) = g(n) + h(n)
        score = 0 + state_score(revised_state, goal)
        transition = (action, revised_state, add, delete, score)
        new_transitions.append(transition)

    transitions = new_transitions
    transitions.sort(key=lambda y: y[4], reverse=True)

    # print()
    # print([score for _, _, _, _, score in transitions])
    # print()

    for action, new_state, add, delete, score in transitions:
        new_plan, new_explored = deepcopy(plan), deepcopy(explored_list)

        if any(set(new_state) == old_state for old_state in explored_list):
            continue
        if debug:
            new_plan.append(start_state)

        new_plan.append(action)
        new_explored.append(set(new_state))
        resulting_plan = forward_planner(new_state, goal, actions, new_plan, new_explored, debug)

        if resulting_plan is not None:
            return resulting_plan

    return None
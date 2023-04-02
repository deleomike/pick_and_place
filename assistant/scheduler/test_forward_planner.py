import pytest

from assistant.scheduler.forward_planner import *



d1 = {'?from': 'Home'}
d2 = {'?from': 'Store'}
d3 = {'?to': 'Store'}
d4 = {'?to': 'Home'}


@pytest.mark.parametrize("input1,input2,expected", [
    (d1, d2, {}),
    (d1, d3, {'?from': 'Home', '?to': 'Store'}),
    (d1, d4, {'?from': 'Home', '?to': 'Home'})
])
def test_composition(input1, input2, expected):
    assert composition(input1, input2) == expected


actions = {
    "fly":{
        "action": "(fly ?plane, ?from, ?to)",
        "conditions": ["(plane ?plane)", "(airport ?to)", "(airport ?from)", "(at ?plane ?from)"],
        "add": ["(at ?plane ?to)"],
        "delete": ["(at ?plane ?from)"]
    }
}

state1 = ["(plane 1973)", "(airport SFO)", "(airport JFK)","(at 1973 SFO)"]

state2 = ["(plane 1973)", "(plane 2749)", "(airport SFO)", "(airport JFK)", "(airport ORD)", "(at 1973 SFO)", "(at 2749 JFK)", "(at 97 ORD)", "(at 1211 SFO)"]

answer = {'fly': [{'?plane': '1973', '?to': 'JFK', '?from': 'SFO'}, {'?plane': '1973', '?to': 'ORD', '?from': 'SFO'},
  {'?plane': '2749', '?to': 'SFO', '?from': 'JFK'},{'?plane': '2749', '?to': 'ORD', '?from': 'JFK'}]}


@pytest.mark.parametrize("state,_actions,expected", [
    (state1, actions, {"fly":[{'?plane': '1973', '?to': 'JFK', '?from': 'SFO'}]}),
    (state2, actions, answer)
])
def test_successors(state, _actions, expected):
    assert successors(state, _actions) == expected


sub_list = {'?plane': '1973', '?to': 'JFK', '?from': 'SFO'}


@pytest.mark.parametrize("expression,_sub_list,expected", [
    (["(at ?plane ?to)"], sub_list, ['(at 1973 JFK)']),
    (["(at ?plane ?from)"], sub_list, ['(at 1973 SFO)']),
    (["(at ?plane ?from)", "(at ?plane ?to)"], sub_list, ['(at 1973 SFO)', '(at 1973 JFK)'])
])
def test_sub_expression(expression, _sub_list, expected):
    assert sub_expression(expression, _sub_list) == expected


state = ["(plane 1973)", "(airport SFO)", "(airport JFK)","(at 1973 SFO)"]

sample_goal = ["(plane 1973)", "(airport SFO)", "(airport JFK)","(at 1973 SFO)"]


@pytest.mark.parametrize("_state,goal,expected", [
    (state, sample_goal, 4),
    (state, [], 0),
    (state, sample_goal[0:2], 2)
])
def test_state_score(_state, goal, expected):
    assert state_score(_state, goal) == expected

state1 = ["(plane 1973)", "(airport SFO)", "(airport JFK)", "(at 1973 SFO)"]

add1 = ["(plane 2711)"]


@pytest.mark.parametrize("_state,_add1,_add2,expected", [
    (state1, add1, [], set(state1).union(set(add1))),
    (state1, [], state1, set()),
    (state1, add1, add1, set(state1))
])
def test_revise_state(_state, _add1, _add2, expected):
    assert set(revise_state(_state, _add1, _add2)) == expected



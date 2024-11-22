# Rodolph El Khoury - 222199
# Elie Rhayem - 222555

states = ["Cool", "Warm", "OverHeated"]
actions = ["Slow", "Fast"]

gamma = 0.9
threshold = 0.0001

T = {
    "Cool": {
        "Slow": {"Cool": 1.0, "Warm": 0.0, "OverHeated": 0.0},
        "Fast": {"Cool": 0.5, "Warm": 0.5, "OverHeated": 0.0},
    },
    "Warm": {
        "Slow": {"Cool": 0.5, "Warm": 0.5, "OverHeated": 0.0},
        "Fast": {"Cool": 0.0, "Warm": 0.0, "OverHeated": 1.0},
    },
    "OverHeated": {
        "Slow": {"Cool": 0.0, "Warm": 0.0, "OverHeated": 1.0},
        "Fast": {"Cool": 0.0, "Warm": 0.0, "OverHeated": 1.0},
    },
}

R = {
    "Cool": {
        "Slow": {"Cool": 1, "Warm": 0, "OverHeated": 0},
        "Fast": {"Cool": 2, "Warm": 2, "OverHeated": 0},
    },
    "Warm": {
        "Slow": {"Cool": 1, "Warm": 1, "OverHeated": 0},
        "Fast": {"Cool": 0, "Warm": 0, "OverHeated": -10},
    },
    "OverHeated": {
        "Slow": {"Cool": 0, "Warm": 0, "OverHeated": 0},
        "Fast": {"Cool": 0, "Warm": 0, "OverHeated": 0},
    },
}

V = {"Cool": 0, "Warm": 0, "OverHeated": 0}

iteration = 0
while True:
    delta = 0
    new_V = V.copy()

    for state in states:
        if state == "OverHeated":
            continue

        action_values = []
        for action in actions:
            action_value = 0
            for next_state in states:
                transition_prob = T[state][action][next_state]
                reward = R[state][action][next_state]
                future_value = gamma * V[next_state]
                action_value += transition_prob * (reward + future_value)

            action_values.append(action_value)

        new_V[state] = max(action_values)
        delta = max(delta, abs(new_V[state] - V[state]))

    V = new_V
    iteration += 1

    if delta < threshold:
        break

print(f"Converged after {iteration} iterations.")
print("Optimal Value Function:")
for state, value in V.items():
    print(f"  {state}: {value:.4f}")

policy = {}
for state in states:
    if state == "OverHeated":
        policy[state] = None
        continue

    action_values = {}
    for action in actions:
        action_value = 0
        for next_state in states:
            transition_prob = T[state][action][next_state]
            reward = R[state][action][next_state]
            future_value = gamma * V[next_state]
            action_value += transition_prob * (reward + future_value)

        action_values[action] = action_value

    policy[state] = max(action_values, key=action_values.get)

print("\nOptimal Policy:")
for state, action in policy.items():
    print(f"  {state}: {action}")

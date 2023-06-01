import numpy as np


def matrix_to_scalar(matrix):
    result = []
    for m in matrix:
        result.append(np.max(m))
    return result


def switch_func(P, P_prev):
    if P > P_prev or P > 0.25:
        return 1
    return 0


def make_optimal(P_noised):
    plan_forward = []
    plan_backward = []
    for i in range(1, len(P_noised)):
        gamma = switch_func(P_noised[i], P_noised[i-1])
        plan_forward.append(gamma)
    for i in range(len(P_noised)-1, 0, -1):
        gamma = switch_func(P_noised[i-1], P_noised[i])
        plan_backward.append(gamma)

    return plan_forward, plan_backward


def get_plan(P_noised):
    P_scalar = matrix_to_scalar(P_noised)
    plan_f, plan_b = make_optimal(P_scalar)
    for i in range(len(plan_f)):
        if plan_b[i] > plan_f[i]:
            plan_f[i] = plan_b[i]
    return plan_f


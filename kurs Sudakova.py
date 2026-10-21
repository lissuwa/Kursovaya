import sys
import math

def create_function(expr):
    """Превращает строку в функцию f(t, u)"""
    if expr.strip() == "":
        raise ValueError("Пустое выражение")

    math_funcs = {}
    for name in dir(math):
        if not name.startswith("_"):
            math_funcs[name] = getattr(math, name)

    def f(t, u):
        result = eval(expr, {"__builtins__": {}}, {**math_funcs, "t": t, "u": u})
        return float(result)

    f(0, 0)
    return f


def rk4_step(f, t, u, h):
    """Один шаг метода Рунге-Кутты 4-го порядка"""
    k1 = f(t, u)
    k2 = f(t + h/2, u + h*k1/2)
    k3 = f(t + h/2, u + h*k2/2)
    k4 = f(t + h, u + h*k3)
    return u + h * (k1 + 2*k2 + 2*k3 + k4) / 6


def trap_step(f, t, u, h):
    """Один шаг неявного метода Трапеций"""
    f_curr = f(t, u)
    v = u + h * f_curr
    
    for i in range(50):
        f_next = f(t + h, v)
        g = v - u - (h/2) * (f_curr + f_next)
        if abs(g) < 1e-12:
            break
        
        df = (f(t + h, v + 1e-7) - f(t + h, v - 1e-7)) / 2e-7
        v = v - g / (1 - h*df/2)
        
    return v


def solve_ode(f, t0, T, u0, n, method):
    """Считает решение на всем отрезке"""
    h = (T - t0) / n
    ts = [t0]
    us = [u0]
    
    t = t0
    u = u0
    for i in range(n):
        if method == "rk4":
            u = rk4_step(f, t, u, h)
        else:
            u = trap_step(f, t, u, h)
        t += h
        ts.append(t)
        us.append(u)
        
    return ts, us
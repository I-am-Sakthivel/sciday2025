import sympy as sp
import numpy as np
v0, theta, t, g = sp.symbols("v0 theta t g")
x = v0 * sp.cos(theta) * t
y = v0 * sp.sin(theta) * t - (1/2) * g * t**2
t_flight = sp.solve(y, t)[1]
x_func = sp.lambdify((v0, theta, t, g), x, "numpy")
y_func = sp.lambdify((v0, theta, t, g), y, "numpy")
G = 6.67430e-11  
M_sun = 1.989e30  
AU = 1  
def compute_projectile_motion(v0_val, theta_val, g_val):
    t_flight_val = float(t_flight.subs({v0: v0_val, theta: theta_val, g: g_val}))
    h_max = (v0_val**2 * np.sin(theta_val)**2) / (2 * g_val)
    x_range = (v0_val**2 * np.sin(2 * theta_val)) / g_val
    return t_flight_val, h_max, x_range

def get_trajectory_points(v0_val, theta_val, g_val, num_points=100):
    t_flight_val = float(t_flight.subs({v0: v0_val, theta: theta_val, g: g_val}))
    t_vals = np.linspace(0, t_flight_val, num=num_points)
    x_vals = x_func(v0_val, theta_val, t_vals, g_val)
    y_vals = y_func(v0_val, theta_val, t_vals, g_val)
    return x_vals, y_vals
def compute_free_fall(h_initial, g_val):
    t_fall = sp.sqrt((2 * h_initial) / g_val)
    v_final = sp.sqrt(2 * g_val * h_initial)
    return float(t_fall), float(v_final)
def compute_shm(T, A, num_points=100):
    t_vals = np.linspace(0, T, num_points)
    x_vals = A * np.cos((2 * np.pi / T) * t_vals)
    return t_vals, x_vals
def compute_orbit(a, e, num_points=360):
    theta = np.linspace(0, 2 * np.pi, num_points)  
    r = a * (1 - e**2) / (1 + e * np.cos(theta)) 
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y
def energy_comparisons(E):
    if E < 1e-19:
        return f"""
        🔴 **Radio Waves & Microwaves**
        - **With {E:.2e} J, you could barely power a single LED for a nanosecond.**  
        - It would take **~10¹⁹ of these photons** to power a TV for just one second!
        """
    elif 1e-19 <= E < 3e-19:
        return f"""
        🟠 **Infrared & Visible Light**
        - A typical **laser pointer** emits around **1 mW** (10⁻³ W) of power.
        - You'd need **{(1e-3/E):.2e} of these photons per second** to run a laser pointer.
        """
    elif 3e-19 <= E < 1e-16:
        return f"""
        🔵 **Ultraviolet & X-rays**
        - A **single X-ray photon** has enough energy to damage DNA.
        - **{(1e-16/E):.2e} of these photons** equal the energy in an AA battery!
        """
    else:
        return f"""
        🟣 **Gamma Rays & Extreme Energies**
        - A **Gamma Ray Burst** can release **more energy than the Sun will emit in its lifetime**.
        - **{(1e6/E):.2e} photons at this energy** could power an entire city for an hour!
        """

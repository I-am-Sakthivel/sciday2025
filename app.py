import streamlit as st
import numpy as np
from phy import compute_projectile_motion, get_trajectory_points, compute_free_fall, compute_shm,compute_orbit, AU,G, M_sun
from plot import plot_trajectory_interactive, plot_shm_interactive,plot_orbit
st.title("Interactive Physics Simulator")
topic = st.selectbox("Choose a physics concept:", 
                     ["Projectile Motion", "Free Fall", "Simple Harmonic Motion","Celestial Gravitation"])


match topic:
    case "Projectile Motion":
        v0_val = st.slider("Initial Velocity (m/s)", 1, 100, 20)
        theta_val = np.radians(st.slider("Launch Angle (degrees)", 1, 89, 45))
        g_val = 9.81
        t_flight_val, h_max, x_range = compute_projectile_motion(v0_val, theta_val, g_val)
        x_vals, y_vals = get_trajectory_points(v0_val, theta_val, g_val)

        st.write(f"**Time of Flight:** {t_flight_val:.2f} s")
        st.write(f"**Max Height:** {h_max:.2f} m")
        st.write(f"**Range:** {x_range:.2f} m")
        fig = plot_trajectory_interactive(x_vals, y_vals)
        st.plotly_chart(fig)

    case "Free Fall":
        h_initial = st.slider("Initial Height (m)", 1, 100, 10)
        g_val = 9.81
        t_fall, v_final = compute_free_fall(h_initial, g_val)
        st.write(f"**Time to Fall:** {t_fall:.2f} s")
        st.write(f"**Final Velocity Before Impact:** {v_final:.2f} m/s")
    case "Simple Harmonic Motion":
        T = st.slider("Time Period (s)", 1, 10, 5)
        A = st.slider("Amplitude (m)", 1, 10, 3)
        t_vals, x_vals = compute_shm(T, A)
        fig = plot_shm_interactive(t_vals, x_vals)
        st.plotly_chart(fig)
    case "Celestial Gravitation":
        a = st.slider("Semi-Major Axis (AU)", 0.5, 2.0, 1.0)   # Convert AU to meters
        e = st.slider("Eccentricity (0 = Circular, 1 = Parabolic)", 0.0, 0.9, 0.0167)
        T = 2 * np.pi * np.sqrt((a* (1.5e11))**3 / (G * M_sun))  # In seconds
        T_years = np.round(T / (60 * 60 * 24 * 365.25),4) 
        x_vals, y_vals = compute_orbit(a, e)
        st.markdown(f"Orbital Period:~{T_years} Earth years")
        fig = plot_orbit(x_vals, y_vals,a*(1.5e11))
        st.plotly_chart(fig)

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from phy import compute_projectile_motion, get_trajectory_points, compute_free_fall, compute_shm,compute_orbit, AU,G, M_sun,energy_comparisons
from plot import plot_trajectory_interactive, plot_shm_interactive,plot_orbit
st.title("Interactive Physics Simulator")
topic = st.selectbox("Choose a physics concept:", 
                     ["Projectile Motion", "Free Fall", "Simple Harmonic Motion","Celestial Gravitation","Energy Transition","Planck's Constant","E=mc²","Stress and Strain","Entropy","Centripetal & Centrifugal Force","Lens Formula"])

h=6.62607015e-34
c=3e8
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
    case "Energy Transition":
        n_initial = st.slider("Initial Energy Level (n)", 1, 5, 2)
        n_final = st.slider("Final Energy Level (n)", 1, 5, 1)
        if n_final >= n_initial:
            st.warning("Final energy level must be lower than initial energy level.")
        else:
            R_H = 1.097e7  # Rydberg constant (m⁻¹)
            wavelength = 1 / (R_H * (1/n_final**2 - 1/n_initial**2))  # in meters
            st.write(f"**Emitted Photon Wavelength:** {wavelength * 1e9:.2f} nm")

    case "Planck's Constant":
        frequency = st.slider("Frequency of Light (10^xHz)", 12.0,16.0,12.0)
        energy = h * (10**frequency)  # E = hν
        st.write(f"**Photon Energy:** {energy:.2e} Joules")
        st.markdown(energy_comparisons(energy))

    case "E=mc²":
        mass = st.slider("Mass (kg)", 1e-6, 10.0, 1.0)
        energy = mass * c**2  # E = mc²
        st.write(f"**Equivalent Energy:** {energy:.2e} Joules")

    case "Stress and Strain":
        force = st.slider("Applied Force (N)", 1, 1000, 100)
        area = st.slider("Cross-Sectional Area (m²)", 0.0001, 1.0, 0.01)
        original_length = st.slider("Original Length (m)", 0.1, 10.0, 1.0)
        extension = st.slider("Extension (m)", 0.0001, 1.0, 0.01)

        stress = force / area
        strain = extension / original_length

        st.write(f"**Stress:** {stress:.2f} Pa")
        st.write(f"**Strain:** {strain:.6f}")
    case "Entropy":
        Q = st.slider("Heat Energy (J)", 1.0, 1000.0, 100.0)
        T_initial = st.slider("Initial Temperature (K)", 1.0, 1000.0, 300.0)
        T_final = st.slider("Final Temperature (K)", 1.0, 1000.0, 500.0)
        if T_final > T_initial:
            entropy_change = Q * (1/T_initial - 1/T_final)
            st.write(f"**Change in Entropy:** {entropy_change:.2e} J/K")

            T_vals = np.linspace(T_initial, T_final, 100)
            entropy_vals = Q * (1/T_initial - 1/T_vals)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=T_vals, y=entropy_vals, mode="lines", name="Entropy Change"))
            fig.update_layout(title="Entropy vs Temperature", xaxis_title="Temperature (K)", yaxis_title="Entropy Change (J/K)", template="plotly_dark")
            st.plotly_chart(fig)
        else:
            st.warning("Final temperature must be higher than initial temperature for entropy calculation.")

    case "Centripetal & Centrifugal Force":
        mass = st.slider("Mass (kg)", 0.1, 100.0, 5.0)
        radius = st.slider("Radius (m)", 0.1, 50.0, 10.0)
        velocity = st.slider("Velocity (m/s)", 0.1, 100.0, 10.0)
        centripetal_force = mass * (velocity**2) / radius

        st.write(f"**Centripetal Force:** {centripetal_force:.2f} N")

        r_vals = np.linspace(0.1, radius, 100)
        force_vals = mass * (velocity**2) / r_vals
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=r_vals, y=force_vals, mode="lines", name="Centripetal Force"))
        fig.update_layout(title="Centripetal Force vs Radius", xaxis_title="Radius (m)", yaxis_title="Centripetal Force (N)", template="plotly_dark")
        st.plotly_chart(fig)

    case "Lens Formula":
        f = st.slider("Focal Length (m)", -10.0, 10.0, 5.0)
        d_o = st.slider("Object Distance (m)", 0.1, 100.0, 10.0)
        d_i = 1 / ((1/f) - (1/d_o))

        st.write(f"**Image Distance:** {d_i:.2f} m")

        d_o_vals = np.linspace(0.1, 100, 100)
        d_i_vals = 1 / ((1/f) - (1/d_o_vals))
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d_o_vals, y=d_i_vals, mode="lines", name="Lens Formula"))
        fig.update_layout(title="Lens Formula: Object vs Image Distance", xaxis_title="Object Distance (m)", yaxis_title="Image Distance (m)", template="plotly_dark")
        st.plotly_chart(fig)
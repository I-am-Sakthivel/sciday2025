import plotly.express as px
import plotly.graph_objects as go
from phy import AU

def plot_trajectory_interactive(x_vals, y_vals):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines", name="Projectile Path"))
    fig.update_layout(
        title="Projectile Motion",
        xaxis_title="Distance (m)",
        yaxis_title="Height (m)",
        template="plotly_dark",
        hovermode="x unified"
    )
    return fig
def plot_shm_interactive(t_vals, x_vals):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals, y=x_vals, mode="lines", name="SHM Motion", line=dict(color="red")))
    fig.update_layout(
        title="Simple Harmonic Motion",
        xaxis_title="Time (s)",
        yaxis_title="Displacement (m)",
        template="plotly_dark",
        hovermode="x unified"
    )
    return fig
def plot_orbit(x_vals, y_vals, a):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers",
                             marker=dict(size=20, color="yellow"), name="Sun"))
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines",
                             name="Orbit", line=dict(dash="dash")))
    earth_trace = go.Scatter(x=[x_vals[0]], y=[y_vals[0]], mode="markers",
                             marker=dict(size=10, color="blue"), name="Earth")
    fig.add_trace(earth_trace)
    num_frames = len(x_vals)
    frame_duration = 100*(a / (1.0 * (1.5e11)))**1.5 
    frames = [go.Frame(
        data=[go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=20, color="yellow")),  # Sun fixed
              go.Scatter(x=x_vals, y=y_vals, mode="lines", line=dict(dash="dash")),  # Orbit path
              go.Scatter(x=[x_vals[k]], y=[y_vals[k]], mode="markers", marker=dict(size=10, color="blue"))  # Earth moving
             ],
        name=str(k)
    ) for k in range(num_frames)]
    fig.update(frames=frames)
    fig.update_layout(
        title="🌍 Scaled Earth Orbit Animation",
        xaxis_title="X (AU)", yaxis_title="Y (AU)",
        template="plotly_dark",
        xaxis=dict(scaleanchor="y", range=[-2, 2]),
        yaxis=dict(range=[-2, 2]),
         updatemenus=[{
            "type": "buttons",  
            "showactive": False,
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": frame_duration, "redraw": True}, 
                                    "fromcurrent": True, "mode": "immediate"}],
                    "label": "▶ Play", "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False}, 
                                      "mode": "immediate"}],
                    "label": "⏸ Pause", "method": "animate"
                }
            ],
        }]
    )
    return fig

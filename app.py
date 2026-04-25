import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="PID Tuner", layout="wide")
st.title("PID Tuner Simulator")
st.write("Move the sliders and watch how P, I, D affects the system response")

st.sidebar.header("PID Gains")
kp = st.sidebar.slider("Kp - Proportional", 0.0, 5.0, 1.0, 0.1)
ki = st.sidebar.slider("Ki - Integral", 0.0, 2.0, 0.1, 0.05)
kd = st.sidebar.slider("Kd - Derivative", 0.0, 1.0, 0.05, 0.01)

t = np.linspace(0, 10, 500)
setpoint = 1.0
dt = t[1] - t[0]

y = np.zeros_like(t)
error_sum = 0
prev_error = 0

for i in range(1, len(t)):
    error = setpoint - y[i-1]
    error_sum += error * dt
    d_error = (error - prev_error) / dt
    output = kp*error + ki*error_sum + kd*d_error
    y[i] = y[i-1] + output * dt * 0.5
    prev_error = error

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(t, y, label='System Response', linewidth=2)
ax.axhline(setpoint, color='r', linestyle='--', label='Setpoint')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Output')
ax.legend()
ax.grid(True)
st.pyplot(fig)

overshoot = max(0, (max(y) - setpoint) / setpoint * 100)
st.metric("Overshoot", f"{overshoot:.1f}%")
st.caption("Built by Omotoso Odunayo | Control Systems & Robotics")

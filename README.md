# Pendulum Simulation with Nengo

This repository contains implementation of pendulum simulation based on `Euler` (`Euler-Cromer`) method using nengo-gui.


## Pendulum mathematical model
[[Source1]](http://star-www.dur.ac.uk/~tt/MSc/Lecture3.pdf) [[Source2]](https://www.isical.ac.in/~arnabc/numana/diff1.html)

Pendulum bob of mass $m$ attached to a *rigid & massless* rope of length $l$.
$\theta$ is deflection angle from vertical.

![Pendulum scheme](src/simple-pendulum.jpg)

Consider components of gravitational force, $mg$ along and perpendicular to
rope. Component along rope balanced by rope’s tension. Component
perpendicular is $F_{\theta} = -mg sin(\theta)$.

According to the second Newton's law we have the following:

$$
\begin{aligned}
    \tau & = Ia \\
    Lma & = mL^2\theta''(t) \\
    a & = L\theta''(t) \\
    mL\theta''(t)  &= -mgsin(\theta) \\
    \theta''(t) & = -\frac{g}{L}sin(\theta)
\end{aligned}
$$

According to the Euler Method:

$$
\begin{aligned}
    \theta'(t_0) &= \omega_0 \\
    \omega'(t_0) &= -\frac{g}{L}sin(\theta_0) \\
    \theta_t &= \theta_0 + \theta'(t_0)\delta t = \theta_0 + \omega_0 \delta t \\
    \omega_t &= \omega_0 + \omega'(t_0) \delta t = \omega_0 - \frac{g}{L}sin(\theta_0) \delta t
\end{aligned}
$$

We can slightly modify the formulas for $\theta_t$ and $\omega_t$, according to the [Euler-Cromer](https://en.wikipedia.org/wiki/Semi-implicit_Euler_method) method, so the final formulas are:

$$
\begin{aligned}
    \omega_t &= \omega_0 - \frac{g}{L}sin(\theta_0) \delta t \\
    \theta_t &= \theta_0 + \omega_t \delta t
\end{aligned}
$$


## How to set up

### Installation

```
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run nengo

```
nengo pendulum.py
```

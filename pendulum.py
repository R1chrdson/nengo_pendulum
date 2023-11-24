import nengo
import numpy as np


class Pendulum:
    def __init__(
        self,
        init_theta=30 * np.pi / 180,
        length=1,
        g=9.81,
    ):
        self.g = g if g is not None else 9.81
        self.length = length if length is not None and length > 0 else 1

        self.omega = 0
        self.theta = init_theta

        self.prev_t = 0

    def set_length(self, length):
        if length is not None and length > 0:
            self.length = length

    def set_g(self, g):
        if g is not None:
            self.g = g

    def step(self, t):
        dt = t - self.prev_t
        self.prev_t = t

        self.omega += -self.g / self.length * np.sin(self.theta) * dt
        self.theta += self.omega * dt
        self.theta = (self.theta + np.pi) % (2 * np.pi) - np.pi
        print(self.theta, self.omega)

    def update_html(self):
        pivot_x = 50
        pivot_y = 5
        pivot_radius = 2
        bob_x = pivot_x + self.length * 30 * np.sin(self.theta)
        bob_y = pivot_y + self.length * 30 * np.cos(self.theta)
        bob_radius = 8

        return """
            <svg width="100%" height="100%" viewbox="0 0 100 100">
                <circle cx="{pivot_x}" cy="{pivot_y}" r="{pivot_radius}"/>
                <line x1="{pivot_x}" y1="{pivot_y}" x2="{bob_x}" y2="{bob_y}" stroke="black"/>
                <circle cx="{bob_x}" cy="{bob_y}" r="{bob_radius}" fill="yellow"/>
            </svg>
        """.format(
            pivot_x=pivot_x, pivot_y=pivot_y, pivot_radius=pivot_radius, bob_x=bob_x, bob_y=bob_y, bob_radius=bob_radius
        )


class PendulumNetwork(nengo.Network):
    def __init__(self, label=None, **kwargs):
        super().__init__(label=label)
        self.env = Pendulum(**kwargs)

        with self:

            def func(t, x):
                length, g = x
                self.env.set_length(length)
                self.env.set_g(g)
                self.env.step(t)
                func._nengo_html_ = self.env.update_html()
                return (self.env.theta, np.sin(t))

            self.pendulum = nengo.Node(func, size_in=2)

            self.length = nengo.Node(None, size_in=1, label="Length")
            self.g = nengo.Node(None, size_in=1, label="Gravity")
            nengo.Connection(self.length, self.pendulum[0], synapse=None)
            nengo.Connection(self.g, self.pendulum[1], synapse=None)


with nengo.Network() as model:
    env = PendulumNetwork(label="Pendulum")

    length = nengo.Node(1, label="Length")
    g = nengo.Node(9.81, label="Gravity")
    nengo.Connection(length, env.length, synapse=None)
    nengo.Connection(g, env.g, synapse=None)

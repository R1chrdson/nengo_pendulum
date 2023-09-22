import numpy as np
import nengo


class Pendulum:
    def __init__(
        self,
        mass=1,
        length=1,
        g=9.81,
        init_theta=45 * np.pi / 180,
        init_speed=0,
    ):
        self.mass = mass
        self.length = length
        self.g = g
        self.theta = init_theta
        self.speed = init_speed

    def step(self, u):
        pass

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
                self.env.step(x)
                func._nengo_html_ = self.env.update_html()
                return (self.env.theta,)

            self.pendulum = nengo.Node(func, size_in=1)

            self.u = nengo.Node(None, size_in=1, label="Control Signal")
            nengo.Connection(self.u, self.pendulum) # Probably synapse=0



with nengo.Network() as model:
    env = PendulumNetwork()

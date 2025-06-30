import numpy as np
import uaibot as ub
from collections import defaultdict


class LinearInterpolator:
    """Classe para interpolação linear de trajetórias."""
    def __init__(self, robot_controller):
        self.trace_counter = 0
        self.robot_controller = robot_controller

    """Interpolação linear da posição entre dois HTMs."""
    def plan(self, htm_end, t0, objects, steps=100):
        points_center = []
        htm_start = self.robot_controller.robot.fkm(q=self.robot_controller.robot.q, axis='eef')
        for i in range(steps):
            alpha = i / steps
            htm_t = np.matrix(htm_start)
            htm_t[0:3, -1] = (1 - alpha) * htm_start[0:3, -1] + alpha * htm_end[0:3, -1]
            q_inv = self.robot_controller.robot.ikm(
                htm_tg=htm_t,
                p_tol=1,
                a_tol=25,
                q0=self.robot_controller.robot.q,
                no_tries=500
            )
            t = t0 + i * (1 / steps)
            self.robot_controller.robot.add_ani_frame(time=t, q=q_inv)
            points_center.append(self.robot_controller.robot.fkm()[0:3, -1])
        if self.trace_counter < 10:
          pointcloud = ub.PointCloud(points=points_center, color='red', size=0.01)
          objects.append(pointcloud)
          self.trace_counter += 1
        return t

class MinimumJerkInterpolator:
    """
    Interpolador baseado em mínimo jerk para transições suaves entre poses.
    """
    def __init__(self, robot_controller):
        self.trace_counter = 0
        self.robot_controller = robot_controller
        self.memory = defaultdict(dict)

    def _minimum_jerk_scalar(self, s):
        return 10 * s**3 - 15 * s**4 + 6 * s**5

    def plan(self, htm_end, t0, objects, duration=2.0, steps=100, cloud_color='gray'):
        points_center = []
        htm_start = self.robot_controller.robot.fkm(q=self.robot_controller.robot.q, axis='eef')
        for i in range(steps + 1):
            t = i / steps * duration
            s = t / duration
            jerk_s = self._minimum_jerk_scalar(s)

            htm_t = np.matrix(htm_start, copy=True)
            htm_t[0:3, -1] = (1 - jerk_s) * htm_start[0:3, -1] + jerk_s * htm_end[0:3, -1]
            htm_t_key = htm_t.tobytes()

            q0 = self.robot_controller.robot.q
            q0_key = q0.tobytes()


            if htm_t_key in self.memory[q0_key]:
                q_inv = self.memory[q0_key][htm_t_key]
            else:
              q_inv = self.robot_controller.robot.ikm(
                  htm_tg=htm_t,
                  p_tol=0.01,
                  a_tol=5,
                  q0=q0,
                  no_tries=500
              )

              self.memory[q0_key][htm_t_key] = q_inv

            self.robot_controller.robot.add_ani_frame(time=t0 + t, q=q_inv)
            points_center.append(self.robot_controller.robot.fkm()[0:3, -1])

        if self.trace_counter < 20:
          pointcloud = ub.PointCloud(points=points_center, color=cloud_color, size=0.01)
          objects.append(pointcloud)
          self.trace_counter += 1
        return t0 + duration

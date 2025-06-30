import numpy as np
import uaibot as ub


class RobotController:
    """
    Classe responsável por controlar o movimento do robô, calcular trajetórias
    e interagir com a simulação para realizar a pintura.
    """
    def __init__(self, robot, n_joins, a, wtol, dt=0.05, task_movement_timeout=5):
        self.robot = robot
        self.n_joins = n_joins
        self.a = [a] * 6
        self.wtol = [wtol] * 6
        self.dt = dt
        self.task_movement_timeout = task_movement_timeout

    def move_to_initial_position(self, htm_robot_init):
        """Posiciona o robô na posição inicial da simulação."""
        self.robot.add_ani_frame(time=0, q=self.robot.ikm(htm_robot_init))

    def task_function(self, q, htm_d):
        """Calcula o erro e a matriz jacobiana para o controle por tarefas."""
        Jg, htm = self.robot.jac_geo(q)
        jac_v, jac_w = Jg[0:3,:], Jg[3:6,:]
        Se, xe, ye, ze = htm[0:3, 3], htm[0:3, 0], htm[0:3, 1], htm[0:3, 2]
        Sd, xd, yd, zd = htm_d[0:3, 3], htm_d[0:3, 0], htm_d[0:3, 1], htm_d[0:3, 2]

        r = np.zeros((6, 1))
        r[0:3] = Se - Sd
        r[3] = 1 - xd.T @ xe
        r[4] = 1 - yd.T @ ye
        r[5] = 1 - zd.T @ ze

        Jr = np.zeros((6, self.n_joins))
        Jr[0:3, :] = jac_v
        Jr[3, :] = xd.T @ ub.Utils.S(xe) @ jac_w
        Jr[4, :] = yd.T @ ub.Utils.S(ye) @ jac_w
        Jr[5, :] = zd.T @ ub.Utils.S(ze) @ jac_w

        return r, Jr

    def fun_F(self, r):
        """Calcula a função de ativação de controle baseada no erro r."""
        F = np.zeros((6, 1))
        for i in range(6):
            if abs(r[i, 0]) < self.wtol[i]:
                F[i, 0] = -self.a[i] * (r[i, 0] / self.wtol[i])
            elif r[i, 0] >= self.wtol[i]:
                F[i, 0] = -self.a[i]
            else:
                F[i, 0] = self.a[i]
        return F

    def move_to_position(self, htm_target, t0):
        """Move o robô até a pose desejada com interpolação temporal."""
        i = 0
        while True:
            elapsed_time = self.dt * i
            t = elapsed_time + t0
            r, Jr = self.task_function(self.robot.q, htm_target)
            q_dot_d = ub.Utils.dp_inv(Jr, 0.001) @ self.fun_F(r)
            q_next = self.robot.q + q_dot_d * self.dt

            # Verifica se a configuração é válida (sem colisão e dentro dos limites)
            ok, msg, _ = self.robot.check_free_configuration(q=q_next)

            if not ok:
                raise Exception(f"[AVISO] Configuração inválida: {msg}")

            self.robot.add_ani_frame(time=t, q=q_next)

            # Critério de parada: chegar próximo a posição desejada
            # com tolerância de 0.01 ou timeout de 5 segundos
            if np.linalg.norm(r) < 1e-2 or elapsed_time > self.task_movement_timeout:
                break
            i += 1
        return t

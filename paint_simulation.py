import uaibot as ub
import numpy as np
from board import PainterBoard
from robot_controller import RobotController
from interpolators import MinimumJerkInterpolator
import streamlit as st


def run_simulation(board_colors, n, m, num_cores):
    # 1. Configurações iniciais
    objects = []
    robot = ub.Robot.create_kuka_lbr_iiwa()
    objects.append(robot)

    htm_brush_box = ub.Utils.trn([0.4, 0.6, 0.1])
    htm_robot_init = ub.Utils.trn([0.5, 0, 0.8]) * ub.Utils.roty(np.pi/2)
    htm_brush_box_target = ub.Utils.trn([0.4, 0.6, 0.2]) * ub.Utils.roty(np.pi)

    brush_box = ub.Box(color='yellow', width=0.1, depth=0.1, height=0.2, opacity=0.5)
    brush_box.add_ani_frame(time=0, htm=htm_brush_box)
    objects.append(brush_box)

    frame = ub.Frame(htm_brush_box_target, size=0.1)
    objects.append(frame)

    # 2. Tabuleiro
    st.text(f"Simulação iniciada com resolução: {n}x{n}")
    board = PainterBoard(n, board_colors)
    board.create_board(objects)
    st.write(f"Tamanho real de board_colors: {len(board_colors)} x {len(board_colors[0])}")
    st.write(f"Tamanho real de board: {len(board.n)} x {len(board.n)}")

    # 3. Controle e interpolação
    n_joints = robot.q.shape[0]
    robot_ctrl = RobotController(robot, n_joints, a=0.25, wtol=0.01)
    robot_ctrl.move_to_initial_position(htm_robot_init)
    interpolator = MinimumJerkInterpolator(robot_ctrl)

    inicial = ub.simobjects.ball.Ball(htm_robot_init, radius=0.01)
    objects.append(inicial)
    t = 0
    t = interpolator.plan(htm_end=htm_robot_init, t0=t, objects=objects, steps=10)

    # 4. Loop de pintura
    size = 0.4 / n
    colors = np.transpose(board_colors)
    for j in range(n):
        for i in range(n):
            cor = colors[i][j]

            # Use os floats .x, .y, .z em vez de indexar:
            y_pix = board.board_base.y + i*size
            z_pix = board.board_base.z - j*size
            htm_pix = ub.Utils.trn([board.board_base.x, y_pix, z_pix]) * ub.Utils.rotz(np.pi/2)

            pixel = ub.Box(color=cor, width=size, depth=0.01, height=size, opacity=0.9)
            objects.append(pixel)

            if cor == '#ffffff':
                pixel.add_ani_frame(time=t - 0.1, htm=htm_pix)
                continue

            troca = (cor != colors[i-1][j])
            if troca:
                t = interpolator.plan(htm_end=htm_robot_init, t0=t, objects=objects, steps=10)
                t = interpolator.plan(htm_end=htm_brush_box_target, t0=t, objects=objects, steps=10)
                t = interpolator.plan(htm_end=htm_robot_init, t0=t, objects=objects, steps=10)

            htm_start_paint = htm_pix * ub.Utils.trn([0,0,size/2]) * ub.Utils.rotx(np.pi/2)
            t = interpolator.plan(htm_end=htm_start_paint, t0=t, objects=objects, steps=10)
            htm_end_paint = htm_pix * ub.Utils.trn([0,0,-size/2]) * ub.Utils.rotx(np.pi/2)
            t = interpolator.plan(htm_end=htm_end_paint, t0=t, objects=objects, steps=10)

            pixel.add_ani_frame(time=t, htm=htm_pix)

    interpolator.plan(htm_end=htm_robot_init, t0=t, objects=objects, steps=10)

    # 5. Executa simulação
    sim = ub.Simulation(objects, background_color="#FFFFFF", pixel_ratio=1.0, width=1920, height=720)
    sim.run()
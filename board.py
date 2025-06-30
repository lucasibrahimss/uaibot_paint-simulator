from dataclasses import dataclass
import numpy as np
import uaibot as ub
import streamlit as st


@dataclass
class BoardBase:
    x: float
    y: float
    z: float


class PainterBoard:
    """
    Classe responsável por criar o tabuleiro visual de pintura
    baseado na matriz de cores gerada a partir da imagem processada.
    """
    def __init__(self, n, board_colors):
        self.n = n
        self.board_colors = board_colors
        self.matrix = []
        self.size = 0.4 / self.n
        # Agora só guardamos floats, não matriz 4×4:
        self.board_base = BoardBase(
            x=0.6 + 0.01,
            y=-0.2 + self.size/2,
            z=1.0 - self.size/2
        )

    def create_board(self, objects):
        dt_ = 0
        st.text(f"Criando Quadro com {self.n}x{self.n} pixels")
        for j in range(self.n):
            for i in range(self.n):
                # Em cada pixel, chamamos trn(...) usando os floats .x, .y, .z
                htm_pixel = (
                    ub.Utils.trn([
                        self.board_base.x,
                        self.board_base.y + i * self.size,
                        self.board_base.z - j * self.size
                    ]) * ub.Utils.rotz(np.pi/2)
                )
                pixel = ub.Box(
                    color='gray',
                    width=self.size,
                    depth=0.01,
                    height=self.size,
                    opacity=0.6
                )
                pixel.add_ani_frame(time=dt_, htm=htm_pixel)
                self.matrix.append(pixel)
                dt_ += 0.0001
                st.write(f"Tamanho real da matrix: {len(self.matrix)} x {len(self.matrix[0])}")

        objects.extend(self.matrix)

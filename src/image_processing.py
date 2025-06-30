import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

class ImageProcessor:
    """
    Carrega, processa e converte uma imagem em matriz de cores hex.
    Agora aceita tanto caminho (str) quanto arquivo enviado pelo usuário.
    """
    def __init__(self, image_source):
        self.imagem = Image.open(image_source).convert("RGB")

    def reduzir_cores(self, num_cores=3):
        img_np = np.array(self.imagem)
        h, w, _ = img_np.shape
        img_flat = img_np.reshape((-1, 3))
        kmeans = KMeans(n_clusters=num_cores, n_init=10).fit(img_flat)
        cores = kmeans.cluster_centers_.astype(int)
        labels = kmeans.labels_
        img_reduzida = cores[labels].reshape((h, w, 3)).astype(np.uint8)
        self.imagem = Image.fromarray(img_reduzida)

    def redimensionar(self, n, m):
        self.imagem = self.imagem.resize((m, n), Image.NEAREST)

    def para_matriz_hex(self):
        img_np = np.array(self.imagem)
        return [['#{:02x}{:02x}{:02x}'.format(*px) for px in row] for row in img_np]

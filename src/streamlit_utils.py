html_injection = """
    <style>
    div[data-testid="stAppViewContainer"] {
        position: relative;
    }
    #custom-video-bg {
        position: fixed;
        top: 0; left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        object-fit: cover;
        opacity: 0.15;
        pointer-events: none;
    }
    </style>
    <video id="custom-video-bg" autoplay loop muted>
        <source src="https://viniciusmgn.github.io/aulas_manipuladores/presentation/images/aula1/g1.mp4" type="video/mp4">
    </video>
"""

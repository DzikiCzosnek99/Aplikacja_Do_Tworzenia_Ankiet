import matplotlib.pyplot as plt
import base64
from io import BytesIO


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot(answers, votes):
    plt.switch_backend('AGG')
    fiq, ax = plt.subplots(figsize=(7, len(answers)))
    ax.barh(answers, votes, 0.5)
    for index, data in enumerate(votes):
        if data != 0:
            text = ''
            if data == 1:
                text = 'głos'
            elif 1 < data <= 4:
                text = 'głosy'
            else:
                text = 'głosów'
            plt.text(x=data, y=index-0.04, s=f" {data} {text}")
    ax.set_facecolor((0.85, 0.85, 0.85))
    fiq.patch.set_facecolor((0.85, 0.85, 0.85))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_ticks([])
    graph = get_graph()
    return graph

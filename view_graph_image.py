
from PIL import Image as PILImage
import io

def generate_graph_structure(graph):
    try:
        # Get the image bytes from the graph
        image_bytes = graph.get_graph().draw_mermaid_png()

        # Save the image to a file
        with open("graph_output.png", "wb") as f:
            f.write(image_bytes)

        # Open the image with the default system viewer
        img = PILImage.open("graph_output.png")
        img.show()

    except Exception as e:
        print("An error occurred while displaying the image:", e)

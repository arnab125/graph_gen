from datetime import datetime
from math import ceil
import os
from typing import List
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from matplotlib import pyplot as plt
from starlette.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {"request": request, "message": "Hello, FastAPI with SSR!"}
    return templates.TemplateResponse("index.html", context)

@app.get("/create_graph", response_class=HTMLResponse)
async def create_form(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("form.html", context)

@app.post("/submit", response_class=HTMLResponse)
async def handle_form(request: Request,
                      x_array: str = Form(...),
                      y_array: str = Form(...),
                      title: str = Form(...),
                      x_label: str = Form(...),
                      y_label: str = Form(...),
                      x_distance: str = Form(...),
                      y_distance: str = Form(...)):
    context = {
        "request": request,
        "x_array": x_array,
        "y_array": y_array,
        "title": title,
        "x_label": x_label,
        "y_label": y_label,
        "x_distance": x_distance,
        "y_distance": y_distance
    }
    #print(context)

    try:
            # Sample data
        #x = [2.5, 2.6,2.7,2.9,3,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9,5,5.1,5.2,5.3,5.4,5.5,5.6,5.7,5.8,5.9,6,6.1,6.2]

        #y = [90,100,140,85,75,90,130,105,75,65,75,105,80,60,55,70,85,60,50,55,70,65,50,45,55,60,50,40,40,50,55,40,35,35,45,45,35]

        x = [float(i) for i in x_array.split(",")]
        y = [float(i) for i in y_array.split(",")]

        # Get the current directory of the script
        current_directory = os.path.dirname(os.path.realpath(__file__))

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, marker='o', linestyle='-', color='b', label=title)

        # Add title and labels
        plt.title(title)
        plt.xlabel(x_label + ' →')
        plt.ylabel(y_label + ' →')

        # Set axis limits
        max_x = ceil(max(x)/float(x_distance))
        max_y = ceil(max(y)/float(y_distance))
        # Set axis ticks
        plt.xticks([i * float(x_distance) for i in range(max_x)])  # Set x-axis ticks at intervals of 0.25
        plt.yticks([i * float(y_distance) for i in range(max_y)])  # Set y-axis ticks at intervals of 2

        plt.gca().set_xticklabels([str(i * float(x_distance)) if i != 0 else '' for i in range(0, max_x)])# Annotate each point with its coordinate


        # Add grid
        plt.grid(True, linestyle='solid', color='gray', linewidth=0.5)

        # Add legend
        plt.legend()

        # Define the directory path relative to the project directory
        images_directory = os.path.join(current_directory, "static", "images")

        # Create the directory if it doesn't exist
        os.makedirs(images_directory, exist_ok=True)

        unique_id = f"plot-{datetime.now().strftime('%Y%m%d%H%M%S')}.png"

        # Save the plot with high resolution
        plt.savefig(os.path.join(images_directory, unique_id), dpi=1200, bbox_inches='tight')
        # generate the plot link
        context["graph_url"] = f"/static/images/{unique_id}"


        return templates.TemplateResponse("result.html", context)
    except Exception as e:
        context["error"] = str(e)
        return templates.TemplateResponse("form.html", context)

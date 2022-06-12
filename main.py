# import gradio as gr

# def greet(name):
#     return "Hello " + name + "!"

# demo = gr.Interface(
#     fn=greet,
#     inputs=gr.Textbox(lines=2, placeholder="Name Here..."),
#     outputs="text",
# )

# demo.launch()
'''
import gradio as gr

def greet(name, is_morning, temperature):
    salutation = "Good morning" if is_morning else "Good evening"
    greeting = "%s %s. It is %s degrees today" % (salutation, name, temperature)
    celsius = (temperature - 32) * 5 / 9
    return greeting, round(celsius, 2)

demo = gr.Interface(
    fn=greet,
    inputs=["text", "checkbox", gr.Slider(0, 100)],
    outputs=["text", "number"],
)
demo.launch()
'''
#IMAGES
# import numpy as np

# import gradio as gr

# def sepia(input_img):
#     sepia_filter = np.array(
#         [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]]
#     )
#     sepia_img = input_img.dot(sepia_filter.T)
#     sepia_img /= sepia_img.max()
#     return sepia_img

# demo = gr.Interface(sepia, gr.Image(shape=(200, 200)), "image")

# demo.launch()


#dataframes and graphs
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import gradio as gr

def sales_projections(employee_data):
    sales_data = employee_data.iloc[:, 1:4].astype("int").to_numpy()
    regression_values = np.apply_along_axis(
        lambda row: np.array(np.poly1d(np.polyfit([0, 1, 2], row, 2))), 0, sales_data
    )
    projected_months = np.repeat(
        np.expand_dims(np.arange(3, 12), 0), len(sales_data), axis=0
    )
    projected_values = np.array(
        [
            month * month * regression[0] + month * regression[1] + regression[2]
            for month, regression in zip(projected_months, regression_values)
        ]
    )
    plt.plot(projected_values.T)
    plt.legend(employee_data["Name"])
    return employee_data, plt.gcf(), regression_values

demo = gr.Interface(
    sales_projections,
    gr.Dataframe(
        headers=["Name", "Jan Sales", "Feb Sales", "Mar Sales"],
        value=[["Jon", 12, 14, 18], ["Alice", 14, 17, 2], ["Sana", 8, 9.5, 12]],
    ),
    ["dataframe", "plot", "numpy"],
    description="Enter sales figures for employees to predict sales trajectory over year.",
)
demo.launch()
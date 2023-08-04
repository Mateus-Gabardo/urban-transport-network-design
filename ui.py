import gradio as gr

def run_simulation(grafo, demand):
    return 0

def run_scenario(grafo):
    return 0

# Carrega o conteúdo do arquivo CSS
css = "style.css"
with open(css, "r") as f:
    css = f.read()

with gr.Blocks(css=css) as app:
    gr.Markdown("Urban Transport Network Design Problem.")
    with gr.Tab("Singular simulation"):
        with gr.Row(variant='compact'):
            with gr.Column(scale=3):
                text_grafo = gr.Textbox(placeholder="Monte o grafo aqui", show_label=False, lines=3)
                text_demand = gr.Textbox(placeholder="Adicione a demanda", show_label=False, lines=3)
            with gr.Column(scale=1):
                text_button = gr.Button('Simulate', variant='primary', elem_id="simulate")
        with gr.Row(variant='compact'):
            with gr.Column(scale=3):
                text_output = gr.Textbox(label="Modificações", lines=5)
    
    with gr.Tab("Setup simulation"):
        with gr.Row():
            scenario_input = gr.Textbox()
            scenario_output = gr.Textbox()
        scenario_button = gr.Button("Simulate")

        text_button.click(run_simulation, inputs=[text_grafo, text_demand], outputs=text_output)
        scenario_button.click(run_scenario, inputs=scenario_input, outputs=scenario_output)

app.launch(share=True)
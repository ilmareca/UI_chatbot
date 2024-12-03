import gradio as gr

# Define una función que maneje los archivos subidos
def handle_files(files):
    # Devuelve la lista de archivos subidos
    return [file.name for file in files]

def handle_message(message, history):
    # Añade el mensaje al historial
    history.append(( message))
    # Aquí puedes añadir lógica para generar una respuesta del asistente
    response = "Esta es una respuesta automática."
    history.append(response)
    return history

# Function to create the Gradio UI
def create_UI(initial_message: str, action_name: str) -> gr.Blocks:
    """
    Crea una interfaz de usuario para un chatbot utilizando Gradio.
    Args:
        initial_message (str): El mensaje inicial que se mostrará en el chatbot.
        action_name (str): El nombre de la acción extra que se mostrará en el botón correspondiente.
    Returns:
        gr.Blocks: Un objeto de bloques de Gradio que representa la interfaz de usuario del chatbot.
    La interfaz de usuario incluye:
        - Una barra superior con un logo y el nombre de la empresa.
        - Un contenedor principal con instrucciones del chatbot.
        - Un cargador de archivos para contexto adicional (archivos .pdf y .txt).
        - Un chatbot con un mensaje inicial.
        - Una caja de texto para la entrada del usuario.
        - Un botón de envío para enviar mensajes al chatbot.
        - Un botón para reiniciar la conversación.
        - Un botón para una acción extra.
        - Una caja de texto para mostrar un resumen.
    Eventos manejados:
        - Habilitar el botón de envío cuando hay texto en la caja de texto.
        - Resetear el chatbot y el resumen cuando se sube un archivo.
        - Resetear el chatbot y el resumen cuando se hace clic en el botón de limpiar.
        - Manejar el flujo de eventos cuando se envía texto o se hace clic en el botón de envío.
        - Manejar el flujo de eventos cuando se hace clic en el botón de acción extra.
    """
    # Crea un bloque de interfaz de usuario con el título "Tu Asistente Virtual de IA"
    with gr.Blocks(title="Tu Asistente Virtual de IA", css="""
        .gradio-container {background-color: #f0f0f0;}
        .header {background-color: #A100FF; color: white; padding: 10px; text-align: center; width: 100%; position: fixed; top: 0; left: 0; z-index: 1000; box-shadow: 0 4px 20px 2px rgba(0, 0, 0, 0.2);}
        .header img {height: 50px; vertical-align: middle;}
        .header h1 {display: inline; margin-left: 10px;}
        .custom-button {background-color: #004080; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 5px; transition: background-color 0.3s ease;}
        .custom-button:hover {background-color: #003060;}
        .content {padding-top: 70px;} /* Adjust padding to avoid overlap with fixed header */
        .send-button {background-color: #28a745; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 5px; transition: background-color 0.3s ease;}
        .send-button:hover {background-color: #218838;}
    """) as demo:
        # Añade una barra superior con un logo y el nombre de la empresa
        gr.HTML("""
            <div class="header">
            <img src="C:/Users/inesl/OneDrive/Escritorio/ACCENTURE/Gradio/Chatbot/UI_chatbot/files/logo.png" alt="Logo de la Empresa">
            <h1>Nombre de la Empresa</h1>
            </div>
        """)

        # Añade un contenedor para el contenido principal
        with gr.Column(elem_classes="content"):
            # Añade un elemento Markdown con las instrucciones del chatbot
            gr.Markdown("## Instrucciones del chatbot", elem_id="instructions")

            # Crea una fila para organizar los elementos de la interfaz
            with gr.Row():
                # Añade un cargador de archivos para contexto adicional (archivos .pdf y .txt)
                file_uploader_ui = gr.Files(label="Contexto adicional", file_types=[".pdf", ".txt"], scale=1, file_count="multiple")
                
                # Crea una columna para organizar los elementos dentro de la fila
                with gr.Column(scale=4):
                    # Añade un chatbot con un mensaje inicial
                    chatbot_ui = gr.Chatbot(value=[[None, initial_message]], label="Chatbot", elem_id="chatbot")
                    # Crea una fila para organizar los elementos de entrada de texto y botón de envío
                    with gr.Row():
                        # Añade una caja de texto para la entrada del usuario
                        input_text_ui = gr.Textbox(label="Tu entrada de texto", scale=6, elem_id="input_text")
                        # Añade un botón de envío, inicialmente no interactivo
                        submit_btn = gr.Button("Enviar", variant="primary", interactive=False, scale=1, elem_id="submit_btn", elem_classes="send-button")
                    # Crea otra fila para los botones de limpiar y acción extra
                    with gr.Row():
                        # Añade un botón para reiniciar la conversación
                        clear_btn = gr.Button("Empezar de nuevo", variant="secondary", scale=1, elem_id="clear_btn")
                        # Añade un botón para una acción extra, inicialmente no interactivo
                        extra_action_button = gr.Button(action_name, variant="primary", interactive=False, elem_id="extra_action_btn")
            # Añade una caja de texto para mostrar un resumen, inicialmente no interactivo
            summary_ui = gr.Textbox(label=f"Resumen (Haz clic en '{action_name}' para activar)", interactive=False, elem_id="summary")

            # Eventos
            # Habilita el botón de envío cuando hay texto en la caja de texto
            input_text_ui.change(lambda x: gr.Button(interactive=True) if bool(x) else gr.Button(interactive(False)), inputs=input_text_ui, outputs=submit_btn)

            # Resetea el chatbot y el resumen cuando se sube un archivo
            file_uploader_ui.change(lambda: ([[None, initial_message]], None), outputs=[chatbot_ui, summary_ui])

            # Resetea el chatbot y el resumen cuando se hace clic en el botón de limpiar
            clear_btn.click(lambda: ([[None, initial_message]], None), outputs=[chatbot_ui, summary_ui])

            # Maneja el flujo de eventos cuando se envía texto o se hace clic en el botón de envío
            submit_btn.click(handle_message, inputs=[input_text_ui, chatbot_ui], outputs=chatbot_ui) \
                .then(lambda: None, outputs=input_text_ui) \
                .then(lambda: submit_btn.interactive(False), outputs=submit_btn) \
                .then(lambda: extra_action_button.interactive(True), outputs=extra_action_button) \
                .then(lambda: clear_btn.interactive(True), outputs=clear_btn)

            # Maneja el flujo de eventos cuando se hace clic en el botón de acción extra
            extra_action_button.click(lambda: extra_action_button.interactive(False), outputs=extra_action_button) \
                .then(lambda: clear_btn.interactive(False), outputs=clear_btn) \
                .then(lambda conversation: conversation.append(["Acción extra", None]), inputs=chatbot_ui, outputs=summary_ui) \
                .then(lambda: clear_btn.interactive(True), outputs=clear_btn) \
                .then(lambda: extra_action_button.interactive(True), outputs=extra_action_button)

    return demo

# Main function to run the application
if __name__ == "__main__":
    initial_message = "Hola, ¿en qué puedo ayudarte hoy?"
    action_name = "Acción Extra"
    demo = create_UI(initial_message, action_name)
    demo.launch()
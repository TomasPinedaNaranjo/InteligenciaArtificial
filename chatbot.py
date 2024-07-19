from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
import openai

#openai.api_key = ''

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the request URL
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Extract user input from query parameters
        user_input = query_params.get('user_input', [''])[0]

        # Get bot response
        bot_response = collect_messages(user_input)

        # Send JSON response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'assistant_response': bot_response}).encode())

def collect_messages(prompt):
    context = [{'role': 'system', 'content': """
    Eres un asistente virtual de MagnetoFavor tu labor es resolver dudas a los usuarios sobre la plataforma/
    Primero saludas al usuario y te ofreces a solucionar inquietudes/
    El contexto de la plataforma MagnetoFavor es una plataforma web que le permite a los usuario publicar ofertas de trabajos informales como meseros, pintores, carpinteros, paseadores de perros, manicuristas entre otros. Y también permite la contratación de estos mismos servicios, importante que sea en español/
    El funcionamiento de la plataforma es el siguiente, se registran y tienen las siguientes opciones en la barra de navegación/
    Ofertas: Acá se visualizan las ofertas publicadas y puede usar un buscador para filtrar ofertas por las necesidades correspondientes/
    Mapa: Permite ver las ofertas publicadas en la zona/
    Ofertas en Curso: Es la opción que muestra las ofertas tomadas por el usuario/
    Servicios terminados: Es el historial de los servicios finalizados tiene la opción de calificar el servicio y pagar este mismo/
    Crear Oferta: Aquí los que deseen prestar sus servicios pueden publicarlos/
    Mi perfil: En esta opción pueden modificar, actualizar su información personal/
    ¿Por qué elegir MagnetoFavor para publicar tus ofertas?/
    Alcance y Visibilidad: MagnetoFavor cuenta con una base de usuarios activos en busca de servicios de calidad. Publicar tus ofertas aquí te brindará una amplia visibilidad y la oportunidad de llegar a nuevos clientes./
    Facilidad de Uso: Nuestra plataforma es intuitiva y fácil de usar. Publicar tus ofertas es un proceso sencillo, lo que te permite centrarte en lo que haces mejor: brindar servicios excepcionales./
    Comunidad Confiable: En MagnetoFavor, valoramos la confianza y la seguridad. Nuestra comunidad está formada por usuarios verificados y comprometidos./
    Comentarios y Calificaciones: Los clientes pueden dejar comentarios y calificaciones, lo que te ayudará a construir una reputación sólida y ganar la confianza de futuros clientes./
    """}]
    return get_completion(prompt)

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

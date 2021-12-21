import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404, JsonResponse
from base import mods
import os
import requests
from django.views import View


TELEGRAM_URL = "https://api.telegram.org/bot"
TELEGRAM_BOT_TOKEN = '5024206285:AAHIIblX89BBpbQrL5Pu2kA8CkGZ0qLIXqc'
#
#                              Bot de telegram en localhost.
#                                       ¡Atención!  
#   Al completar este tutorial vincularás el bot de Decide a tu localhost y se quitará de heroku.
#
#   Requisitos:
#       1.- Instalar ngrok
#       2.- Tener el servidor corriendo en el puerto 8000
#   Uso:
#       1.- Utilizar el comando "$ ngrok http 8000" en la terminal
#       2.- Apuntar la dirección https creada asociada al puerto 8000
#       3.- Añadir esa dirección a la siguiente url y acceder a ella:
# https://api.telegram.org/bot5024206285:AAHIIblX89BBpbQrL5Pu2kA8CkGZ0qLIXqc/setWebhook?url=<direccionngrok>/webhooks/
#       4.- Hablarle al bot de telegram @DecidePenyagolosaBot
# 
class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        return context

class TelegramBot(View):
    def post(self, request, *args, **kwargs):
        t_data = json.loads(request.body)
        t_message = t_data["message"]
        t_chat = t_message["chat"]

        try:
            text = t_message["text"].strip().lower()
            print(text)
        except Exception as e:
            return JsonResponse({"ok": "POST request processed"})

        command = text.lstrip("/").split()[0]
        if command=="start":
            rtext = "Usa el comando /visualizer <id> - para consultar una votación"
            self.send_message(rtext, t_chat["id"])
        if command=="visualizer":
            try:
                votingid = text.lstrip("/").split()[1]
            
            except Exception as e:
                return JsonResponse({"ok": "POST request processed"})
                
            if votingid.isnumeric():
                rtext = self.returndb(votingid)
            else:
                rtext = "Por favor introduzca un número valido"
            self.send_message(rtext, t_chat["id"])



        return JsonResponse({"ok": "POST request processed"})

    @staticmethod
    def send_message(message, chat_id):
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        response = requests.post(
            "{}{}/sendMessage".format(TELEGRAM_URL,TELEGRAM_BOT_TOKEN), data=data
        )

    @staticmethod
    def returndb(voting_id):
        try:
            r = mods.get('voting', params={'id': voting_id})
            voting = json.dumps(r[0])
        except:
            return "Voto no finalizado"
        voting = json.loads(voting)
        text=' La votación "{}" ha tenido los siguientes resultados:\n\n'.format(voting["name"])
        for option in voting["postproc"]:
            text+= "La opción {} ha recibido {} votos\n".format(option["option"],option["postproc"])        
        return text
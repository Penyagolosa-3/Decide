import os
import discord
import json
import requests
from base import mods
from dotenv import load_dotenv
from discord import Webhook,RequestsWebhookAdapter

TOKEN = os.getenv('DISCORD_TOKEN')
#webhook_url = "https://discord.com/api/webhooks/922301093755633664/PIOHdcWk1OWIjwgdX9QPDntGR9zzrKYpyxy3iecQYUCovs9onMI6tCuCweKov1SYD9_K"
#webhook_id = "922301093755633664"
#webhook_token = "PIOHdcWk1OWIjwgdX9QPDntGR9zzrKYpyxy3iecQYUCovs9onMI6tCuCweKov1SYD9_K"
#webhook = Webhook.partial(webhook_id,webhook_token,\
#    adapter= RequestsWebhookAdapter())
#webhook.send('Webhook enviado.')




load_dotenv()
client = discord.Client()
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "!visualizer" == message.content.lower().split()[0]:
        voting_id = message.content.lower().split()[1]
        if voting_id.isnumeric():
            rtext = devuelveBaseDeDatos(voting_id)
        else:
            rtext = "Por favor introduzca un número valido"
        await message.channel.send(rtext)
    
def devuelveBaseDeDatos(voting_id):
    try:
        r = mods.get('voting', params={'id': voting_id})
        voting = json.dumps(r[0])
    except:
        return "Voto no finalizado"
    voting = json.loads(voting)
    text= "El voto {} ha tenido los siguientes resultados:\n\n".format(voting["name"])
    for option in voting["postproc"]:
        text+= "La opcion {} ha recibido {} votos\n".format(option["option"],option["postproc"])        
    return text

client.run(TOKEN)
import discord
from discord.ext import commands
import datetime

from urllib import parse, request
import re

from decouple import config


# Con esto asignamos el caracter especial para darle instrucciones al bot. description es opcional
bot = commands.Bot(command_prefix=">", description="I am the discord robot :)")

# ------FUNCIONES------
# las funciones tienen que ser async/await
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def suma(ctx, num1: int, num2: int):
    await ctx.send(num1 + num2)

@bot.command()
async def info(ctx):
    """Embed reprecenta un cuadro en discord en donde podemos poner 
        titulos, contenido imagenes fecha etc."""
   
    embed = discord.Embed(title=f"{ctx.guild.name}",    # ctx.guild.name = nombre del servidor
        description="lorem ipsum lo que sea bla bla",
        timestamp=datetime.datetime.utcnow(),           # tiempo 
        color=discord.Color.blue()                      # color de la caja 
        )
    embed.add_field(name="Server Created at", value = f"{ctx.guild.created_at}") # cuando fue creado el server
    embed.add_field(name="Server Owner", value = f"{ctx.guild.owner}")           # quien es el dueño
    embed.add_field(name="Server Region", value = f"{ctx.guild.region}")         # cual es la region
    embed.add_field(name="Server id", value = f"{ctx.guild.id}")                 # cual es el id del server
    embed.set_thumbnail(url = "https://images6.alphacoders.com/523/523425.jpg")  # para mandar una imagen. {ctx.guild.icon} = icono del server
        
    await ctx.send(embed=embed)

@bot.command()
async def youtube(ctx, *, search):
    query_search = parse.urlencode({"search_query": search}) # transforma palabras comunes en direcciones a internet. ejemplo: quita espacios y agrega + etc.
    html_content = request.urlopen("https://www.youtube.com/results?" + query_search)
    search_results = re.findall( r"watch\?v=(\S{11})", html_content.read().decode()) # para obtener los id de los videos
    await ctx.send("https://www.youtube.com/watch?v=" + search_results[0]) # envia una caja con el primer video conseguido :)
    print(query_search)
    print("*****************")
    print(html_content)



@bot.command()
async def wiki(ctx, *, search):
    query_search = search.replace(" ", "_")
    url_completa = "https://es.wikipedia.org/wiki/" + query_search
    await ctx.send(url_completa)


# Events
@bot.event
async def on_ready():
    # podemos cambiar el estado del robot. en este caso a transmitiendo y incluso darle un link para la url 
    await bot.change_presence(activity=discord.Streaming(name="Python-discord", url="https://www.youtube.com/watch?v=05r7WsIXT-A&ab_channel=FaztCode"))

    print("The Robot is alive") # cuando se conecte dirá esto

token_bot = config("TOKEN_BOT")

bot.run(token_bot)
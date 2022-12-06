import discord
import os
import json
import re
from random import randint
from dotenv import load_dotenv


class MyClient(discord.Client):
    async def on_ready(self):
        for guild in self.guilds:
            if str(guild.id) not in data:
                data[str(guild.id)] = {"prefix": "!", "globals": {}}
        await save()
        if em_desenvolvimento:
            await self.change_presence(status=discord.Status.do_not_disturb)
        else:
            await self.change_presence(status=discord.Status.online)
        print(f'Logged on as {self.user.mention}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if str(message.guild.id) not in data:
            data[str(message.guild.id)] = {"prefix": "!", "globals": {}}
        server = data[str(message.guild.id)]
        if str(message.channel.id) not in server:
            server[str(message.channel.id)] = {"locals": {}}
        channel = str(message.channel.id)
        if "locals" not in server[channel]:
            server[channel]["locals"] = {}
        if str(message.author.id) not in server[channel]:
            server[channel][str(message.author.id)] = ""
        user = str(message.author.id)
        prefix = server["prefix"]
        if message.content.startswith(self.user.mention):
            command = message.content[len(prefix):].lower() + " "
            args = command.split(" ")
            if args[1] == "reset":
                server["prefix"] = "!"
                await save()
                await message.reply('O prefixo desse servidor voltou a ser "!".')
            else:
                await message.reply(f'Seu prefixo atual é "{prefix}"!\n'
                                    f'Se quiser resetar o prefixo para "!", digite "{self.user.mention} reset".')
        if message.content.startswith(prefix):
            try:
                command = message.content[len(prefix):].lower() + " "
                lines = command.split("\n")
                args = []
                for line in lines:
                    args += line.split(" ")
                while "" in args:
                    args.remove("")
                if args[0] == "help":
                    await message.reply('- help\n'
                                        'Exibe esse texto\n'
                                        'Exemplo:\n'
                                        '```  !help```\n'
                                        '\n'
                                        '- ping\n'
                                        'Comando simples para checar se o bot ainda funciona. Ele responderá à sua '
                                        'mensagem com "Pong!".\n'
                                        'Exemplo:\n'
                                        '```  !ping```\n'
                                        '\n'
                                        ' - prefix {prefixo}\n'
                                        'O bot mudará o prefixo do servidor para que seja o definido no comando. '
                                        'Mencione o bot caso tenha esquecido o prefixo ou queira resetar ele.\n'
                                        'Exemplo:\n'
                                        '```  !prefix &```\n'
                                        '\n'
                                        ' - ficha {nome}\n'
                                        '   [atrN] ["roll"] [valN]\n'
                                        '   ...          ...        ...\n'
                                        'O bot criará ou atualizará a ficha com o nome especificado. Os atributos '
                                        'mencionados serão criados se ainda não existirem e seus valores serão '
                                        'definidos como os mencionados logo após. Linhas novas entre o nome e os '
                                        'diferentes atributos são obrigatórias e nomes de atributos não podem conter '
                                        'espaços. Também é possível utilizar imagens, gifs ou até vídeos, ao colocar '
                                        'seus links no valor de um atributo. Valores da ficha podem referenciar '
                                        'variáveis locais e outros atributos.\n'
                                        'Exemplo:\n'
                                        '```  !ficha mago\n'
                                        '  inteligencia 17\n'
                                        '  vida 9\n'
                                        '  dano roll 2d4 + (inteligencia / 5)\n'
                                        '  aparencia '
                                        'https://cdn.pixabay.com/photo/2019/03/21/09/03/mage-4070515_960_720.png```\n'
                                        '\n'
                                        ' - local\n'
                                        '   [varN] ["roll"] [valN]\n'
                                        '   ...          ...         ...\n'
                                        'Similar ao comando "ficha", mas, ao invés de atributos, cria variáveis locais '
                                        'que podem ser utilizadas por todos personagens, independente da ficha '
                                        'utilizada. Valores locais podem referenciar atributos de fichas e outras '
                                        'variáveis locais.\n'
                                        'Exemplo:\n'
                                        '```  !local\n'
                                        '  atributo roll 3d6 + 3\n'
                                        '  ataque roll d20 + força```\n'
                                        '\n'
                                        ' - roll {rolagem}\n'
                                        'Rola a rolagem concedida. A rolagem pode ter atributos de ficha ou variáveis '
                                        'locais.\n'
                                        'Exemplos:\n'
                                        '```  !roll d100\n'
                                        '  !roll 2d6+força\n'
                                        '  !roll ataque+3```\n'
                                        '\n'
                                        ' - import ["locals"] {canal}\n'
                                        'Importa todos os atributos de todas fichas de um outro canal. Caso "locals" '
                                        'seja usado, também importa as variáveis locais daquele canal.\n'
                                        'Exemplos:\n'
                                        '```  !import #canal-secreto-com-fichas-de-inimigos\n'
                                        '  !import locals #canal-com-variaveis-locais```\n'
                                        '\n'
                                        ' - copy {original} {nome-da-copia}\n'
                                        'Copia uma ficha.\n'
                                        '```  !copy bandido1 bandido2```\n')
                    await message.reply('- nome-de-atributo-da-ficha-utilizada [valor]\n'
                                        'Ao usar o nome de um atributo como se fosse um comando, é possível ver ou '
                                        'mudar seu valor. Se o atributo foi definido com "roll", seu valor é rolado. '
                                        'Caso um valor não seja fornecido, o valor atual do atributo é mostrado. Caso o'
                                        ' valor recebido pelo comando seja uma operação aritmética, ela é realizada no '
                                        'atual valor do atributo; Caso contrário o valor do atributo é alterado para o '
                                        'valor recebido pelo comando.\n'
                                        'Exemplos:\n'
                                        '```  !força        - Mostra a Força\n'
                                        '  !vida 30      - Torna a vida 30\n'
                                        '  !xp + 100     - Adiciona 100 a xp```\n'
                                        '\n'
                                        ' - nome-de-variavel-local [valor]\n'
                                        'Similar ao comando anterior, mas ao invés de um atributo de ficha, é utilizado'
                                        ' uma variável local.\n'
                                        'Exemplos:\n'
                                        '```  !nivel-inicial 3\n'
                                        '  !atributo roll 3d6+7```\n'
                                        '\n'
                                        ' - nome-de-outra-ficha [atributo] [valor]\n'
                                        'Caso nenhum atributo ou valor seja fornecido, o comando troca a ficha '
                                        'utilizada por você atualmente para a ficha do comando. Caso um atributo e/ou '
                                        'valor seja fornecido, o comando funciona similarmente ao comando ante-anterior'
                                        ', mas ao invés de mostrar/mudar um atributo da ficha atualmente utilizada por '
                                        'você, o comando mostra/muda um atributo de outra ficha.\n'
                                        '```  !bandido1 vida -7     - Diminui 7 da vida de bandido1\n'
                                        '  !guerreiro            - Começa a utilizar a ficha guerreiro```\n'
                                        '\n'
                                        'O nome do comando deve seguir o prefixo do servidor (! por pardrão). '
                                        'Argumentos rodeados por chaves ({}) são obrigatórios, enquanto argumentos '
                                        'rodeados por colchetes ([]) são opcionais. Argumentos rodeados por aspas ("") '
                                        'devem ser escritos como mostrado para serem reconhecidos.)\n')
                if args[0] == "ping":
                    await message.reply("Pong!")
                if args[0] == "prefix":
                    if len(args) > 1:
                        server["prefix"] = args[1]
                        await save()
                        await message.reply(f'Prefixo do Servidor salvo como "{args[1]}"!\n'
                                            f'Caso precise de ajuda, basta me marcar!')
                    else:
                        await message.reply('O novo prefixo é necessário no comando')
                if args[0] == "ficha":
                    if len(lines) > 1:
                        line1 = lines[0].split(" ")
                        if len(line1) > 1:
                            name = line1[1]
                        else:
                            name = self.get_user(int(user)).name
                        if name not in server[channel]:
                            server[channel][name] = {}
                        for line in lines[1:]:
                            words = line.split(" ")
                            server[channel][name][words[0]] = " ".join(words[1:]).replace(";", "\n")
                        server[channel][user] = name
                        await save()
                        await message.reply("Sua ficha foi atualizada")
                    else:
                        char = server[channel][user]
                        if len(args) > 1 and args[1] == "clear":
                            if len(args) > 2:
                                if args[2] in server[channel][char]:
                                    del server[channel][char][args[2]]
                                    await save()
                                    await message.reply(f"{args[2]} foi deletado da sua ficha.")
                                elif args[2] in server[channel]:
                                    del server[channel][args[2]]
                                    await save()
                                    await message.reply(f"A ficha de {args[2]} foi deletada.")
                                else:
                                    await message.reply(f"{args[2]} não existe.")
                            else:
                                del server[channel][char]
                                await save()
                                await message.reply("Sua ficha foi excluída.")
                        elif len(args) > 1 and args[1] == "all":
                            msg = "Essas são todas as fichas desse canal"
                            for value in server[channel]:
                                if value != "locals" and type(server[channel][value]) != str:
                                    msg += f"\n - {value}"
                            await message.reply(msg)
                        else:
                            msg = "Sua ficha atual é:"
                            if len(args) > 1 and args[1] in server[channel]:
                                msg = f"A ficha atual de {args[1]} é:"
                                char = args[1]
                            msg += f"\n---| Nome: {char} |---"
                            if char in server[channel]:
                                for value in server[channel][char]:
                                    msg += f"\n{value} = {server[channel][char][value]}"
                                await message.reply(msg)
                            else:
                                await message.reply("Você não tem uma ficha selecionada neste canal!")
                if args[0] == "local":
                    if len(lines) > 1:
                        for line in lines[1:]:
                            words = line.split(" ")
                            server[channel]["locals"][words[0]] = " ".join(words[1:]).replace(";", "\n")
                        await save()
                        await message.reply("As variáveis locais foram atualizadas.")
                    else:
                        if len(args) > 1 and args[1] == "clear":
                            if len(args) > 2:
                                if args[2] in server[channel]["locals"]:
                                    del server[channel]["locals"][args[2]]
                                    await save()
                                    await message.reply(f"{args[2]} foi deletado das variáveis locais.")
                                else:
                                    await message.reply(f"{args[2]} não é uma variável local.")
                            else:
                                del server[channel]["locals"]
                                server[channel]["locals"] = {}
                                await save()
                                await message.reply("As variáveis locais foram excluídas.")
                        else:
                            msg = "As variáveis locais atuais são:"
                            if len(server[channel]["locals"]) > 0:
                                for value in server[channel]["locals"]:
                                    msg += f"\n{value} = {server[channel]['locals'][value]}"
                                await message.reply(msg)
                            else:
                                await message.reply("Esse canal não tem variáveis locais.")
                if args[0] == "roll":
                    if len(args) > 1:
                        try:
                            cmd = " ".join(args[1:])
                            cmd, rolls = roll(cmd, message)
                            await message.reply(str(eval(cmd)) + rolls)
                        except ZeroDivisionError:
                            await message.reply("É impossível dividir por 0")
                        except Exception as e:
                            await message.reply("Rolagem Inválida")
                            raise e
                    else:
                        await message.reply("Você precisa dizer uma rolagem no comando")
                if args[0] == "import":
                    if len(args) > 1 and len(message.channel_mentions) > 0:
                        mentioned = message.channel_mentions[0]
                        ment = str(mentioned.id)
                        if ment in server:
                            for sheet in server[ment]:
                                if sheet != "locals" and type(server[ment][sheet]) == dict:
                                    if sheet not in server[channel]:
                                        server[channel][sheet] = {}
                                    for value in server[ment][sheet]:
                                        server[channel][sheet][value] = server[ment][sheet][value]
                            if args[1] == "locals":
                                for value in server[ment]["locals"]:
                                    server[channel]["locals"][value] = server[ment]["locals"][value]
                            await save()
                            await message.reply("Importando Informações de " + mentioned.mention)
                        else:
                            await message.reply("O canal mencionada não tem nada a ser importado.")
                    else:
                        await message.reply("Você precisa mencionar um canal.")
                if args[0] == "copy":
                    if len(args) > 2 and args[1] in server[channel] and \
                            args[1] != "locals" and type(server[channel][args[1]]) == dict:
                        if args[2] not in server[channel]:
                            server[channel][args[2]] = {}
                        for value in server[channel][args[1]]:
                            server[channel][args[2]][value] = server[channel][args[1]][value]
                        await save()
                        await message.reply("Ficha copiada.")
                    else:
                        await message.reply("Você precisa fornecer os nomes do original e da cópia, respetivamente.")
                if server[channel][user] in server[channel] and args[0] in server[channel][server[channel][user]]:
                    char = server[channel][user]
                    if len(args) > 1:
                        old_val = server[channel][char][args[0]]
                        try:
                            server[channel][char][args[0]] = str(eval(str(
                                server[channel][char][args[0]]) + " " + " ".join(args[1:])))
                        except SyntaxError:
                            server[channel][char][args[0]] = str(eval(" ".join(args[1:])))
                        await save()
                        await message.reply(f"{args[0]} mudado de {old_val} para {server[channel][char][args[0]]}!")
                    else:
                        val = server[channel][char][args[0]].split(" ")
                        if val[0] == "roll":
                            try:
                                cmd, rolls = roll(" ".join(val[1:]), message)
                                await message.reply(str(eval(cmd)) + rolls)
                            except ZeroDivisionError:
                                await message.reply("É impossível dividir por 0")
                            except Exception as e:
                                await message.reply("Rolagem Inválida")
                                raise e
                        else:
                            await message.reply(" ".join(val))
                if args[0] in server[channel]["locals"]:
                    if len(args) > 1:
                        old_val = server[channel]["locals"][args[0]]
                        try:
                            server[channel]["locals"][args[0]] = str(eval(str(
                                server[channel]["locals"][args[0]]) + " " + " ".join(args[1:])))
                        except SyntaxError:
                            server[channel]["locals"][args[0]] = str(eval(" ".join(args[1:])))
                        await save()
                        await message.reply(f"{args[0]} mudado de {old_val} para {server[channel]['locals'][args[0]]}!")
                    else:
                        val = server[channel]["locals"][args[0]].split(" ")
                        if val[0] == "roll":
                            try:
                                cmd, rolls = roll(" ".join(val[1:]), message)
                                await message.reply(str(eval(cmd)) + rolls)
                            except ZeroDivisionError:
                                await message.reply("É impossível dividir por 0")
                            except Exception as e:
                                await message.reply("Rolagem Inválida")
                                raise e
                        else:
                            await message.reply(" ".join(val))
                if args[0] in server[channel] and args[0] != "locals" and type(server[channel][args[0]]) == dict:
                    if len(args) > 2:
                        if args[1] in server[channel][args[0]]:
                            old_val = server[channel][args[0]][args[1]]
                            try:
                                server[channel][args[0]][args[1]] = str(eval(str(
                                    server[channel][args[0]][args[1]]) + " " + " ".join(args[2:])))
                            except SyntaxError:
                                server[channel][args[0]][args[1]] = str(eval(" ".join(args[2:])))
                            await message.reply(f"{args[1]} mudado de {old_val} para "
                                                f"{server[channel][args[0]][args[1]]}!")
                            await save()
                        else:
                            await message.reply("Não encontrei esse atributo na ficha.")
                    elif len(args) > 1:
                        if args[1] in server[channel][args[0]]:
                            val = server[channel][args[0]][args[1]].split(" ")
                            if val[0] == "roll":
                                try:
                                    cmd, rolls = roll(" ".join(val[1:]), message)
                                    await message.reply(str(eval(cmd)) + rolls)
                                except ZeroDivisionError:
                                    await message.reply("É impossível dividir por 0")
                                except Exception as e:
                                    await message.reply("Rolagem Inválida")
                                    raise e
                            else:
                                await message.reply(" ".join(val))
                        else:
                            await message.reply("Não encontrei esse atributo na ficha.")
                    else:
                        server[channel][user] = args[0]
                        await save()
                        await message.reply("A ficha utilizada foi mudada.")
            except Exception as e:
                if em_desenvolvimento:
                    await message.reply("Um erro inesperado ocorreu. Por favor, contacte meu criador.")
                    raise e


async def save():
    outfile = open("data.json", "w")
    json.dump(data, outfile, indent=4)
    outfile.close()


def roll(old_cmd, message):
    server = data[str(message.guild.id)]
    channel = str(message.channel.id)
    user = str(message.author.id)
    char = server[channel][user]
    rolls = ""
    vals = list(server[channel]["locals"])
    if char in server[channel]:
        vals += list(server[channel][user])
        while any(x in old_cmd for x in vals):
            for local in server[channel]["locals"]:
                loc = server[channel]["locals"][local].split(" ")
                if loc[0] == "roll":
                    loc.pop(0)
                loc = " ".join(loc)
                old_cmd = old_cmd.replace(local, loc)
            for value in server[channel][char]:
                old_cmd = old_cmd.replace(value, str(server[channel][char][value]))
    cmd = old_cmd
    match = re.search(r"(\d*)d(\d+)", cmd)
    while match:
        parts = list(cmd.partition(match[0]))
        result, rolled = dice(int(match[1] or "1"), int(match[2]))
        rolls += f" - {rolled}"
        parts[1] = str(result)
        cmd = "".join(parts)
        match = re.search(r"(\d*)d(\d+)", cmd)
    return cmd, rolls + f" ({old_cmd})"


def dice(amount, sides):
    rolled = []
    result = 0
    for i in range(amount):
        r = randint(1, sides)
        rolled.append(r)
        result += r
    return result, rolled


em_desenvolvimento = False
file = open("data.json")
data = json.load(file)
file.close()
load_dotenv()
token = os.getenv("TOKEN")
client = MyClient()
client.run(token)

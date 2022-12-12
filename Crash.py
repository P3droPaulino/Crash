"""
Desenvolvedor: David Eduardo
GITHUB: https://github.com/davideduardotech
"""


import requests, json, time, telebot, pymongo
from colorama import Fore, init
from datetime import datetime
init(autoreset=True, convert=True)

"""
CODDING: Banco de Dados(https://www.mongodb.com/)
"""
MongoDB = pymongo.MongoClient("mongodb+srv://bcgame:ajyxjCqIegRNs4eM@cluster0.eikrx0n.mongodb.net/?retryWrites=true&w=majority")

"""
CODDING: Webscript
"""
        
def recent_15_history_crash_games():
    """
        Função responsavel por pegar ultimos 15 historicos do crash
        GET: https://blaze.com/api/crash_games/recent
    """
    global MongoDB
    try:
        configuracoes = MongoDB.BlazeApostas.Configuracoes.find_one({'tipo':'crash'})
        if configuracoes['CODDING: link da api crash externa'].strip() != '':
            try:
                request = requests.get(configuracoes['CODDING: link da api crash externa'].strip())
                json_to_dict = json.loads(request.content)
                lista_recent_crash_externo = []
                for crash in json_to_dict['results'][-15:]:
                    lista_recent_crash_externo.append(crash['maxRate'])
                
                return request.content, lista_recent_crash_externo
            except Exception as erro:
                request = requests.get("https://blaze.com/api/crash_games/recent")
                json_to_dict = json.loads(request.content)
                list_recent_15_history_crash_games = []
                for item in json_to_dict:
                    list_recent_15_history_crash_games.append(item['crash_point'])
                list_recent_15_history_crash_games.reverse()
                return request.content,list_recent_15_history_crash_games
            
            
        else:
            request = requests.get("https://blaze.com/api/crash_games/recent")
            json_to_dict = json.loads(request.content)
            list_recent_15_history_crash_games = []
            for item in json_to_dict:
                list_recent_15_history_crash_games.append(item['crash_point'])
            list_recent_15_history_crash_games.reverse()
            return request.content,list_recent_15_history_crash_games
    except Exception as erro:
        print(erro)


"""
CODDING: Resetar
"""
def resetar(grupo):
    """
    CODDING: Resetar Configurações do Banco de Dados
    """
    global MongoDB
    
    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']},{'$set':{'CODDING: Entrada':''}})
    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']},{'$set':{'CODDING: historico da entrada':''}})
    
    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']},{'$set':{'CODDING: historico da blaze':''}})
    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']},{'$set':{'CODDING: mensagem procurando pattern':''}})
    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']},{'$set':{'CODDING: ids mensagens de entrada':''}})



"""
CODDING: Convertendo Mensagens(MongoDB)
"""
def converting_messages(text, grupo, recent_history=None, probabilidade=None):
    global MongoDB
    if "[GAME]" in text or "[GAME Capitalize() Link()]" in text:
        text = text.replace("[GAME Capitalize() Link()]", '<a href="{}">{}</a>'.format(grupo['link do game'], grupo['game'].capitalize() ))
        text = text.replace('[GAME]', grupo['game'])
        
    if "[HORARIO COM DIA DA SEMANA]" in text:
        days = ['Segunda-Feira', 'Terça-Feira', 'Quarta-Feira','Quinta-Feira','Sexta-Feira','Sábado','Domingo']
        text = text.replace('[HORARIO COM DIA DA SEMANA]', '{}, {}'.format(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y %H:%M:%S'), days[datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).weekday()]))

    if "[ULTIMO HISTORICO DA BLAZE Negrito()]" in text:
        text = text.replace('[ULTIMO HISTORICO DA BLAZE Negrito()]','<b>🔺{}x</b>'.format(recent_history[-1]))
    if "[PROBABILIDADE]" in text:
        text = text.replace('[PROBABILIDADE]', '<b>🔺{}x</b>'.format(probabilidade))
    return text

"""
CODDING: Looking(Procurando) Patters(Padrões)
"""
def looking_for_pattern(pattern=None, history_crash=[], grupo={}):
    """
    Função Resposavel por Buscar Padrão Estrategico nos Crashs
    https://blaze.com/api/crash_games/recent
    """
    global MongoDB
    
    
    if pattern == "1.00x, wait 5 candles and enter seeking 3x" or pattern == None:
        if history_crash[-1] == '0':
            MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':'0'}})
            return "1.00x, wait 5 candles and enter seeking 3x"

        elif history_crash[-2] == '0':
            MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':'{};{}'.format(history_crash[-2], history_crash[-1])}})
            return "1.00x, wait 5 candles and enter seeking 3x"
        elif history_crash[-3] == '0':
            MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':'{};{};{}'.format(history_crash[-3], history_crash[-2], history_crash[-1])}})
            return "1.00x, wait 5 candles and enter seeking 3x"
        elif history_crash[-4] == '0':
            MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':'{};{};{};{}'.format(history_crash[-4], history_crash[-3], history_crash[-2], history_crash[-1])}})
            return "1.00x, wait 5 candles and enter seeking 3x"
        elif history_crash[-5] == '0':
            MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':'{};{};{};{};{}'.format(history_crash[-5], history_crash[-4], history_crash[-3], history_crash[-2], history_crash[-1])}})
            return "1.00x, wait 5 candles and enter seeking 3x"
        else:
            print('{}{}{} {}{}x {}x {}x {}x {}x{}'.format(Fore.LIGHTBLACK_EX,grupo['link do game'], Fore.RESET,Fore.RED, history_crash[-5], history_crash[-4], history_crash[-3], history_crash[-2], history_crash[-1], Fore.RESET))
    if pattern == "4 candles abaixo de 2.00x, entrar buscando 2x" or pattern == None:
        if float(history_crash[-4]) < 2.00 and float(history_crash[-3]) < 2.00 and float(history_crash[-2]) < 2.00 and float(history_crash[-1]) < 2.00:
            MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':'{};{};{};{}'.format(history_crash[-4], history_crash[-3], history_crash[-2], history_crash[-1])}})
            return "4 candles abaixo de 2.00x, entrar buscando 2x"
        if float(history_crash[-4]) >= 2.00 and float(history_crash[-3]) < 2.00 and float(history_crash[-2]) < 2.00 and float(history_crash[-1]) < 2.00:
            MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':'{};{};{}'.format(history_crash[-3], history_crash[-2], history_crash[-1])}})
            return "4 candles abaixo de 2.00x, entrar buscando 2x"
    

def Bot(token):
    """
    CODDING: Conectar no Telegram
    """
    bot = telebot.TeleBot(token, parse_mode='HTML')
    
    """
    CODDING: Resetar Configurações do Banco de Dados
    """
    grupos = MongoDB.BlazeApostas.Crash.find({'tipo de grupo':'free'})
    for grupo in grupos:
        MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']},{'$set':{'CODDING: Entrada':''}})
        MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']},{'$set':{'CODDING: historico da entrada':''}})
        
        MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']},{'$set':{'CODDING: historico da blaze':''}})
        MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']},{'$set':{'CODDING: mensagem procurando pattern':''}})
        MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']},{'$set':{'CODDING: ids mensagens de entrada':''}})
        
        
        

    while True:
        try:
            """
            CODDING: Pegar historico 
            https://blaze.com/api/roulette_games/recent
            """
            binary_recent_history,recent_crash = recent_15_history_crash_games()
            
            """
            CODDING: Transmitir 
            """
            grupos = MongoDB.BlazeApostas.Crash.find({'tipo de grupo':'free'})
            for grupo in grupos:
                if grupo['CODDING: Entrada'] == '':
                    """
                    CODDING: Enviar Mensagem de Procurando Patters
                    """
                    if grupo['CODDING: mensagem procurando pattern'] == '':
                        mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text=converting_messages(grupo['MENSAGENS: mensagem procurando pattern'],grupo))
                        MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{"CODDING: mensagem procurando pattern": '{};'.format(mensagem.id) if grupo['CODDING: mensagem procurando pattern'] == '' else grupo['CODDING: mensagem procurando pattern']+str(mensagem.id)+';'}})
                        MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                                    
                        
                    """                                  
                    CODDING: Looking(Procurando) for Pattern(Padrões)
                    https://blaze.com/api/roulette_games/recent                                             
                    """
                    pattern = looking_for_pattern(history_crash=recent_crash, grupo=grupo)
                    if pattern:
                        MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: Entrada':pattern}})
                        MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da blaze':str(recent_crash)}})
                        
                    
                else:
                
                    """
                    CODDING: Aguardar Entrada 
                    """
                    if grupo['CODDING: Entrada'] == '1.00x, wait 5 candles and enter seeking 3x':
                        
                        if len(grupo['CODDING: historico da entrada'].split(';')) == 1:
                            if str(recent_crash) != grupo['CODDING: historico da blaze']:
                                MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':grupo['CODDING: historico da entrada']+';'+str(recent_crash[-1])}})
                                MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da blaze':str(recent_crash)}})
                        elif len(grupo['CODDING: historico da entrada'].split(';')) == 2:
                            if str(recent_crash) != grupo['CODDING: historico da blaze']:
                                MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':grupo['CODDING: historico da entrada']+';'+str(recent_crash[-1])}})
                                MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da blaze':str(recent_crash)}})
                        elif len(grupo['CODDING: historico da entrada'].split(';')) == 3:
                            if str(recent_crash) != grupo['CODDING: historico da blaze']:
                                MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':grupo['CODDING: historico da entrada']+';'+str(recent_crash[-1])}})
                                MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da blaze':str(recent_crash)}})
                        elif len(grupo['CODDING: historico da entrada'].split(';')) == 4:
                            if str(recent_crash) != grupo['CODDING: historico da blaze']:
                                """
                                CODDING: Possivel Patters Detectado, Transmitir Mensagem 
                                """
                                mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text=converting_messages(text=grupo['MENSAGENS: mensagem possivel entrada'], grupo=grupo))
                                MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                                
                                
                                MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':grupo['CODDING: historico da entrada']+';'+str(recent_crash[-1])}})
                                MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da blaze':str(recent_crash)}})
                        elif len(grupo['CODDING: historico da entrada'].split(';')) == 5:
                            if str(recent_crash) != grupo['CODDING: historico da blaze']:
                                """
                                CODDING: Padrão Detectado, Transmitir Mensagem de Entrar 
                                """
                                mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text=converting_messages(text=grupo['MENSAGENS: mensagem de entrada confirmada'], grupo=grupo, recent_history=recent_crash, probabilidade='3.00'))
                                MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                                
                            
                                MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':grupo['CODDING: historico da entrada']+';'+str(recent_crash[-1])}})
                                MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da blaze':str(recent_crash)}})
                        elif len(grupo['CODDING: historico da entrada'].split(';')) == 6:
                            #$ RESULTADO SEM NENHUM MARTINGALE
                            if str(recent_crash) != grupo['CODDING: historico da blaze']:
                                """
                                CODDING: Resultado Sem Martingale
                                """
                                #$ WIN
                                if float(recent_crash[-1]) >= 2.5:
                                    mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text=converting_messages(text=grupo['MENSAGENS: mensagem de win sem martingale'], grupo=grupo, recent_history=recent_crash))
                                    bot.send_sticker(chat_id=int(grupo['id do grupo']), sticker=open('sticks/win-sem-gale.webp','rb'))
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                                    
                                    
                                    #$ REINICIAR
                                    resetar(grupo)
                                    
                                else:
                                    #$ LOSS, REALIZAR MARTINGALE 1
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':grupo['CODDING: historico da entrada']+';'+str(recent_crash[-1])}})
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da blaze':str(recent_crash)}})
                                    
                                    mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text="""RESULTADO(Sem Martingale): <b>🔺{}x</b>\nRealize 1° Martingale buscando atingir <b>🔺3.00x</b> no <a href='https://blaze.com/pt/games/crash'>Crash</a>""".format(recent_crash[-1]))
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                        elif len(grupo['CODDING: historico da entrada'].split(';')) == 7:
                            #$ RESULTADO 1 Martingale
                            if str(recent_crash) != grupo['CODDING: historico da blaze']:
                                """
                                CODDING: Resultado 1° Martingale
                                """
                                #$ WIN
                                if float(recent_crash[-1]) >= 2.5:
                                    mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text=converting_messages(text=grupo['MENSAGENS: mensagem de win no martingale'], grupo=grupo, recent_history=recent_crash))
                                    bot.send_sticker(chat_id=int(grupo['id do grupo']), sticker=open('sticks/win-no-gale.webp','rb'))
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                                    
                                    if grupo['CODDING: excluir mensagens de martingale'] == 'True':
                                        try:
                                            bot.delete_message(chat_id=int(grupo['id do grupo']), message_id=grupo['CODDING: ids mensagens de entrada'].split(';')[-1])
                                        except Exception as erro:
                                            print(erro)
                                            
                                    #$ REINICIAR
                                    resetar(grupo)
                                    
                                else:
                                    #$ LOSS, REALIZAR MARTINGALE 2
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':grupo['CODDING: historico da entrada']+';'+str(recent_crash[-1])}})
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da blaze':str(recent_crash)}})
                                    
                                    mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text="""RESULTADO(1° Martingale): <b>🔺{}x</b>\nRealize 2° Martingale buscando atingir <b>🔺3.00x</b> no <a href='https://blaze.com/pt/games/crash'>Crash</a>""".format(recent_crash[-1]))
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                        elif len(grupo['CODDING: historico da entrada'].split(';')) == 8:
                            #$ RESULTADO 1 Martingale
                            if str(recent_crash) != grupo['CODDING: historico da blaze']:
                                """
                                CODDING: Resultado 2° Martingale
                                """
                                #$ WIN
                                if float(recent_crash[-1]) >= 2.5:
                                    mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text=converting_messages(text=grupo['MENSAGENS: mensagem de win no martingale'], grupo=grupo, recent_history=recent_crash))
                                    bot.send_sticker(chat_id=int(grupo['id do grupo']), sticker=open('sticks/win-no-gale.webp','rb'))
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                                    
                                    if grupo['CODDING: excluir mensagens de martingale'] == 'True':
                                        try:
                                            bot.delete_message(chat_id=int(grupo['id do grupo']), message_id=grupo['CODDING: ids mensagens de entrada'].split(';')[-1])
                                            bot.delete_message(chat_id=int(grupo['id do grupo']), message_id=grupo['CODDING: ids mensagens de entrada'].split(';')[-2])
                                        except Exception as erro:
                                            print(erro)
                                            
                                    #$ REINICIAR
                                    resetar(grupo)
                                    
                                else:
                                    #$ LOSS, REALIZAR MARTINGALE 2
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':grupo['CODDING: historico da entrada']+';'+str(recent_crash[-1])}})
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da blaze':str(recent_crash)}})
                                    
                                    mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text=converting_messages(text=grupo['MENSAGENS: mensagem de loss no martingale'], grupo=grupo, recent_history=recent_crash))
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                                    mensagem = bot.send_sticker(chat_id=int(grupo['id do grupo']), sticker=open('sticks/loss.webp', 'rb'))
                                    grupo = MongoDB.BlazeApostas.Crash.find_one({'id do grupo':grupo['id do grupo']})
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                                    
                                    if grupo['CODDING: excluir mensagens de loss'] == 'True':
                                        """
                                        EXCLUIR MENSAGENS: Procurando Patterns
                                        """
                                        grupo_update = MongoDB.BlazeApostas.Crash.find_one({"id do grupo":grupo['id do grupo']})
                                        if grupo_update['CODDING: mensagem procurando pattern'] != '':
                                            for mensagem in grupo_update['CODDING: mensagem procurando pattern'].split(';'):
                                                try:
                                                    if mensagem != '':
                                                        bot.delete_message(chat_id=int(grupo['id do grupo']), message_id=int(mensagem))
                                                except Exception as erro:
                                                    print(erro)
                                            MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']},{'$set':{'CODDING: mensagem procurando pattern':''}})

                                        """
                                        EXCLUIR MENSAGENS: Loss
                                        """
                                        grupo_update = MongoDB.BlazeApostas.Crash.find_one({"id do grupo":grupo['id do grupo']})
                                        for mensagem in grupo_update['CODDING: ids mensagens de entrada'].split(';'):
                                            try:
                                                if mensagem != '':
                                                    bot.delete_message(chat_id=int(grupo['id do grupo']), message_id=int(mensagem))
                                                    
                                            except Exception as erro:
                                                print(erro)

                                    #$ REINICIAR
                                    resetar(grupo)

                    if grupo['CODDING: Entrada'] == '4 candles abaixo de 2.00x, entrar buscando 2x':
                        if len(grupo['CODDING: historico da entrada'].split(';')) == 3:
                            if str(recent_crash) != grupo['CODDING: historico da blaze']:
                                """
                                CODDING: Possivel Patters Detectado, Transmitir Mensagem 
                                """
                                mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text=converting_messages(text=grupo['MENSAGENS: mensagem possivel entrada'], grupo=grupo))
                                MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                                
                                MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':grupo['CODDING: historico da entrada']+';'+str(recent_crash[-1])}})
                                MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da blaze':str(recent_crash)}})
                        if len(grupo['CODDING: historico da entrada'].split(';')) == 4:
                            if str(recent_crash) != grupo['CODDING: historico da blaze']:
                                if float(recent_crash[-1]) < 2.00: 
                                    """
                                    CODDING: Patters Detectado, Transmitir Mensagem de Entrada
                                    """
                                    
                                    mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text=converting_messages(text=grupo['MENSAGENS: mensagem de entrada confirmada'], grupo=grupo, recent_history=recent_crash, probabilidade='2.00'))
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                                    
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':grupo['CODDING: historico da entrada']+';'+str(recent_crash[-1])}})
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da blaze':str(recent_crash)}})
                                else:
                                    #$ OPERAÇÃO CANCELADA, EXLUIR MENSAGENS E REINICIAR
                                    try:
                                        grupo_update = MongoDB.BlazeApostas.Crash.find_one({'id do grupo':grupo['id do grupo']})
                                        for mensagem in grupo_update['CODDING: ids mensagens de entrada'].split(';'):
                                            try:
                                                if mensagem != '':
                                                    bot.delete_message(chat_id=int(grupo['id do grupo']), message_id=int(mensagem))
                                                    
                                            except Exception as erro:
                                                print(erro)
                                    except Exception as erro:
                                        pass
                                    
                                    #$ REINICIAR 
                                    resetar(grupo)
                        if len(grupo['CODDING: historico da entrada'].split(';')) == 5:
                            if str(recent_crash) != grupo['CODDING: historico da blaze']:
                                if float(recent_crash[-1]) >= 2.00:
                                    #$ WIN SEM MARTINGALE
                                    mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text=converting_messages(text=grupo['MENSAGENS: mensagem de win sem martingale'], grupo=grupo, recent_history=recent_crash))
                                    bot.send_sticker(chat_id=int(grupo['id do grupo']), sticker=open('sticks/win-sem-gale.webp','rb'))
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                                    
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':grupo['CODDING: historico da entrada']+';'+str(recent_crash[-1])}})
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da blaze':str(recent_crash)}})

                                    #$ RESETAR
                                    resetar(grupo)
                                else:
                                    #$ LOSS, REALIZAR 1° MARTINGALE
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':grupo['CODDING: historico da entrada']+';'+str(recent_crash[-1])}})
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da blaze':str(recent_crash)}})
                                    
                                    mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text="""RESULTADO(Sem Martingale): <b>🔺{}x</b>\nRealize 1° Martingale buscando atingir <b>🔺2.00x</b> no <a href='https://blaze.com/pt/games/crash'>Crash</a>""".format(recent_crash[-1]))
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                        if len(grupo['CODDING: historico da entrada'].split(';')) == 6:
                            if str(recent_crash) != grupo['CODDING: historico da blaze']:
                                if float(recent_crash[-1]) >= 2.00:
                                    #$ WIN COM 1 MARTINGALE
                                    mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text=converting_messages(text=grupo['MENSAGENS: mensagem de win no martingale'], grupo=grupo, recent_history=recent_crash))
                                    bot.send_sticker(chat_id=int(grupo['id do grupo']), sticker=open('sticks/win-no-gale.webp','rb'))
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                                    
                                    if grupo['CODDING: excluir mensagens de martingale'] == 'True':
                                        try:
                                            bot.delete_message(chat_id=int(grupo['id do grupo']), message_id=grupo['CODDING: ids mensagens de entrada'].split(';')[-1])
                                            
                                        except Exception as erro:
                                            print(erro)

                                    #$ RESETAR
                                    resetar(grupo)
                                else:
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':grupo['CODDING: historico da entrada']+';'+str(recent_crash[-1])}})
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da blaze':str(recent_crash)}})
                                    
                                    mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text="""RESULTADO(1° Martingale): <b>🔺{}x</b>\nRealize 2° Martingale buscando atingir <b>🔺2.00x</b> no <a href='https://blaze.com/pt/games/crash'>Crash</a>""".format(recent_crash[-1]))
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                        if len(grupo['CODDING: historico da entrada'].split(';')) == 7:
                            if str(recent_crash) != grupo['CODDING: historico da blaze']:
                                if float(recent_crash[-1]) >= 2.00:
                                    #$ WIN COM 2 MARTINGALE
                                    mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text=converting_messages(text=grupo['MENSAGENS: mensagem de win no martingale'], grupo=grupo, recent_history=recent_crash))
                                    bot.send_sticker(chat_id=int(grupo['id do grupo']), sticker=open('sticks/win-no-gale.webp','rb'))
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                                    
                                    if grupo['CODDING: excluir mensagens de martingale'] == 'True':
                                        try:
                                            bot.delete_message(chat_id=int(grupo['id do grupo']), message_id=grupo['CODDING: ids mensagens de entrada'].split(';')[-1])
                                            bot.delete_message(chat_id=int(grupo['id do grupo']), message_id=grupo['CODDING: ids mensagens de entrada'].split(';')[-2])
                                        except Exception as erro:
                                            print(erro)
                                    
                                    #$ RESETAR
                                    resetar(grupo)
                                else:
                                    #$ LOSS, REALIZAR MARTINGALE 2
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da entrada':grupo['CODDING: historico da entrada']+';'+str(recent_crash[-1])}})
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: historico da blaze':str(recent_crash)}})
                                    
                                    mensagem = bot.send_message(chat_id=int(grupo['id do grupo']), text=converting_messages(text=grupo['MENSAGENS: mensagem de loss no martingale'], grupo=grupo, recent_history=recent_crash))
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                                    mensagem = bot.send_sticker(chat_id=int(grupo['id do grupo']), sticker=open('sticks/loss.webp', 'rb'))
                                    grupo = MongoDB.BlazeApostas.Crash.find_one({'id do grupo':grupo['id do grupo']})
                                    MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']}, {'$set':{'CODDING: ids mensagens de entrada':'{}'.format(mensagem.id) if grupo['CODDING: ids mensagens de entrada'] == '' else grupo['CODDING: ids mensagens de entrada']+';'+str(mensagem.id)}})
                                    
                                    if grupo['CODDING: excluir mensagens de loss'] == 'True':
                                        """
                                        EXCLUIR MENSAGENS: Procurando Patterns
                                        """
                                        grupo_update = MongoDB.BlazeApostas.Crash.find_one({"id do grupo":grupo['id do grupo']})
                                        if grupo_update['CODDING: mensagem procurando pattern'] != '':
                                            for mensagem in grupo_update['CODDING: mensagem procurando pattern'].split(';'):
                                                try:
                                                    if mensagem != '':
                                                        bot.delete_message(chat_id=int(grupo['id do grupo']), message_id=int(mensagem))
                                                except Exception as erro:
                                                    print(erro)
                                            MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']},{'$set':{'CODDING: mensagem procurando pattern':''}})

                                        """
                                        EXCLUIR MENSAGENS: Loss
                                        """
                                        grupo_update = MongoDB.BlazeApostas.Crash.find_one({"id do grupo":grupo['id do grupo']})
                                        for mensagem in grupo_update['CODDING: ids mensagens de entrada'].split(';'):
                                            try:
                                                if mensagem != '':
                                                    bot.delete_message(chat_id=int(grupo['id do grupo']), message_id=int(mensagem))
                                                    
                                            except Exception as erro:
                                                print(erro)

                                    #$ REINICIAR
                                    resetar(grupo)
                                    
                    
                    """
                    CODDING: Excluir Mensagem de Procurando Patters
                    """
                    if grupo['CONFIGURAÇÕES: excluir mensagens de procurando patters'] == 'True':
                        grupo_update = MongoDB.BlazeApostas.Crash.find_one({"id do grupo":grupo['id do grupo']})
                        for mensagem in grupo_update['CODDING: mensagem procurando pattern'].split(';'):
                            try:
                                if mensagem != '':
                                    bot.delete_message(chat_id=int(grupo['id do grupo']), message_id=int(mensagem))
                            except Exception as erro:
                                print(erro)
                        MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']},{'$set':{'CODDING: mensagem procurando pattern':''}})
                    else:
                        MongoDB.BlazeApostas.Crash.update_one({'id do grupo':grupo['id do grupo']},{'$set':{'CODDING: mensagem procurando pattern':''}})


            time.sleep(3.5)
            
        except Exception as erro:
            print(erro)
            
            
configuracoes = MongoDB.BlazeApostas.Configuracoes.find_one({'tipo':'crash'})       
Bot(configuracoes['CODDING: token(@botfhater)'])







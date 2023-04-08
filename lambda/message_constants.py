
# LAUCHER

LAUNCHER_OUTPUT_FIRST_VISIT = '''
<speak>
    Olá! Bem-vindo ao assistente para interagir com o CHAT G.P.T..<break time="0.4s"/> 
    Consigo enviar sua pergunta mantendo o contexto das perguntas anteriores.<break time="0.4s"/>
    Para fazer uma pergunta você deve falar a palavra "responda",
    e em seguida qual a sua dúvida. Por exemplo: <break time="0.2s"/>"responda qual a capital da França".<break time="0.2s"/>
    Sinta-se à vontade para fazer uma pergunta.
</speak>
'''

LAUNCHER_OUTPUT_NOT_FIRST_VISIT = '''
<speak>
    Olá!
    Como posso ajudar a interagir com o CHAT G.P.T?
</speak>
'''

LAUNCHER_REPROMPT = '''
<speak>
    Você precisa falar a palavra "responda"<break time="0.1s"/> e na mesma sentença o que você deseja saber.
</speak>'''


# ASKCHAGPT

ASKCHATGPT_OUTPUT_CHANGE_VOICE = '''
<speak>
    <voice name="{voice}">
        {{response}}
    </voice>
    {{not_a_full_msg}}
    <break time="0.2s"/>
    Não hesite em chamar a Alexa e fazer uma nova pergunta.
</speak>
'''

ASKCHATGPT_ADD_NOT_A_FULL_RESPONSE = '''
<break time="0.4s"/>
Desculpe, infelizmente não consegui receber a resposta inteira dentro do tempo limite.
'''

ASKCHATGPT_MAX_QUESTIONS_DAILY_REACHED = '''
<speak>
    Desculpe, você já fez o número máximo de {max_questions} perguntas hoje.
    <say-as interpret-as="interjection">{interjection}</say-as>.
</speak>
'''

ASKCHATGPT_MAX_QUESTIONS_PER_CONVERSATION_REACHED = '''
<speak>
    Desculpe, você já fez o número máximo de {max_questions} perguntas nessa conversa.
    Você pode falar o comando "escutar conversa"<break time="0.1s"/> para ouvi-lá novamente ou 
    o comando "finalizar conversa"<break time="0.1s"/> para apagá-la e assim conseguir iniciar uma nova conversa.
    O que você gostaria de fazer?
</speak>
'''


# ACTIONS
LISTEN_A_ROLE = '''
<voice name="{voice}">
    {talk}
</voice>
<break time="0.2s"/>
'''

LISTEN_OUTPUT = '''
<speak>
    Certo, aqui vai a sua última conversa: <break time="0.2s"/>
    {conversation}
    Para apagar essa conversa e conseguir iniciar uma nova use o comando <break time="0.15s"/>"finalizar conversa"<break time="0.15s"/>.
</speak>
'''

LISTEN_EMPTY_CONVERSATION_OUTPUT = '''
<speak>
    Não há conversa disponível para escutar.<break time="0.1s"/>
    Se desejar faça uma pergunta.
</speak>
'''

END_A_CONVERSATION_OUTPUT = '''
<speak>
    Certo, sua conversa foi apagada. Estou disponível para iniciar uma nova conversa.
</speak>
'''

# HELP

HELP_OUTPUT = '''
<speak>
    Certo, aqui vão algumas dicas:<break time="0.6s"/>
    Para fazer uma pergunta você precisa falar a palavra "responda"<break time="0.1s"/>, e em seguida o que você deseja saber. 
    Por exemplo, <break time="0.25s"/> "responda qual é a capital da França".
    <break time="0.4s"/>
    Para escutar a sua conversa atual fale  o comando <break time="0.15s"/>"escutar conversa"<break time="0.15s"/>.
    E para finalizá-la, fale <break time="0.15s"/>"finalizar conversa"<break time="0.15s"/>.
    <break time="0.4s"/>
    Para sair da Skill, você pode pedir a Alexa para Sair.
    <break time="0.4s"/>
    O que você gostaria de fazer?
</speak>'''


# CANCEL

CANCEL_OUTPUT = '''
<speak>
    <say-as interpret-as="interjection">{interjection}</say-as>.
</speak>'''


# FALLBACK

FALLBACK_OUTPUT = '''
<speak>
    Hmm, Você não informou qual sua pergunta. Você precisa falar a palavra "responda", e em seguida o que você deseja saber.
</speak>'''


# ERRORS

ERRORS_OUTPUT_RATELIMITERROR_2_OPTION = '''
<speak>
    <say-as interpret-as="interjection">{}</say-as>.
    <break time="0.2s"/>
    <amazon:emotion name="disappointed" intensity="high">
        Chegamos ao limite mensal de perguntas ao CHAT G.P.T..
    </amazon:emotion>
    <break time="0.2s"/>
    <amazon:emotion name="excited" intensity="high">
        Mas não se preocupe, mês que vem estaremos de volta!
    </amazon:emotion>
    <break time="0.2s"/>
    <say-as interpret-as="interjection">até mais ver</say-as>.
</speak>'''

ERRORS_OUTPUT_REQUESTAPIERROR = '''
<speak>
    Infelizmente ocorreu um erro ao enviar a sua pergunta para o Chat G.P.T.. <break time="0.1s"/> Tente novamente mais tarde.
</speak>'''

ERRORS_OUTPUT_DEFAULT = '''
<speak>
    Desculpe, não entendi o que você perguntou. Pode tentar novamente?
</speak>'''
 
## Skill da Alexa para se comunicar com o ChatGPT

>Essa skill consegue enviar sua pergunta ao ChatGPT, mantendo o contexto das perguntas anteriores ao responder uma nova pergunta.

+ A skill base para essa está disponível no: https://www.amazon.com.br/dp/B0BZ9BSSSM (você pode usar os reviews para inspiração). 
+ Skill é feita em Python.
+ A ideia não ser uma skill 100% pronta para publicação, mas sim servir de base para customização. Dica: tente deixar a interação com a skill mais natural para uma conversa.
+ Adicionar documentação e modularização do código da skill será feito no futuro e atualizado aqui (como não há no momento, o código pode ser bem difícil de entender para quem não conhecer Python ou o Alexa Skills Kit para desenvolvedores).

### Como implementar?<strong>
1. Acesse o https://developer.amazon.com/alexa/console/ask e faça sua eventuais atualizações de cadastro se necessário (é utilizada a mesma conta da Amazon).
  
2. Clique no botão "Create Skill".

    ![image](https://user-images.githubusercontent.com/64989931/230691603-0d83ba4a-2272-4003-8ece-5994fd86544c.png)
  
3. Crie um nome para a Skill e altere a linguagem padrão para "Português(BR)", depois clique em Next.

   ![image](https://user-images.githubusercontent.com/64989931/230691787-2dbf82ad-fabc-444a-911a-5e21f1b82f48.png)
  
4. Selecione uma categoria e deixe a opção de modelo "Custom", depois clique em Next.

    ![image](https://user-images.githubusercontent.com/64989931/230692301-3a2a8872-41c5-4793-b09b-51e777c74b80.png)
 
5. Clique em "Import Skill".

    ![image](https://user-images.githubusercontent.com/64989931/230691993-494e8e41-b717-47bd-9f9c-7138e566b059.png)

6. Adicione o link desse repositório(https://github.com/miguelzph/converse_com_chatgpt_alexa_skill), clique em "Import" e aguarde até finalizar.

    ![image](https://user-images.githubusercontent.com/64989931/230692052-6ae183fc-3bd7-459e-a78f-fc5353992a0e.png)
 
7. Na próxima tela, Vá em "Invocations" --> "Skill Invocation Name" e altere para o nome que vai chamar essa skill. Clique em "Save Model" e depois em "Build Model".

   ![image](https://user-images.githubusercontent.com/64989931/230693809-58b16cb7-b7ec-48f8-bbbd-8113f4a80052.png)

8. Após aguarda o build do modelo, vá na aba de "Code"e adicione a chave que você encontra no site da OpenAI https://platform.openai.com/account/api-keys. Depois é só clicar em Deploy e aguardar finalizar.

   ![image](https://user-images.githubusercontent.com/64989931/230694044-0eaefe82-55b6-4c0a-a114-643903d390a0.png)

9. Para testar você pode ir na aba de "Test" e selecionar "Development" (habilitando no seu aplicativo você também vai conseguir testar por ele e na sua Alexa).

### Comandos disponíveis
+ Primeiro você precisa abrir a skill com "abrir" + <Skill Invocation Name> escolhido no passo 7.

    ![image](https://user-images.githubusercontent.com/64989931/230694844-3efa8fe9-186b-49b3-9e2c-c552fdf411f5.png)

+ Perguntas podem ser feitas falando a palavra "responda" seguida da sua pergunta.

   ![image](https://user-images.githubusercontent.com/64989931/230694920-1b7ff80c-37f9-40e0-b710-131f4ec5ec02.png)

+ O comando "escutar conversa" serve para escutar toda a conversa atual e o comando "finalizar conversa" serve para finalizar a conversa atual, e assim conseguir iniciar uma nova.

   ![image](https://user-images.githubusercontent.com/64989931/230694952-c6ade451-e62e-442e-8778-5c042b07deb8.png)

</strong>
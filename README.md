# Código Secreto

Jogo de decifrar palavras em que cada número é uma letra (1 = A, 2 = B, 3 = C…), com ranking da turma em tempo quase real. Foi desenvolvido como apoio à oficina **Detetives da Lógica**, do projeto **Exploradores Digitais**, voltada a crianças de 8 a 10 anos.

## Acesse o site

**https://codigo-secreto-njbu.onrender.com**

No plano gratuito da hospedagem, se o site ficou parado, a primeira abertura pode levar cerca de 1 minuto. É normal.

## Contexto acadêmico

| | |
|---|---|
| Universidade | Universidade da Região de Joinville (Univille) |
| Curso | Engenharia de Software e Sistema de Informação |
| Disciplina | Vivências de Extensão II |
| Professor(a) | Luiz melo Romão |
| Ano | 2026 |
| Projeto | Oficina "Exploradores Digitais" |
| Oficina nº | 3 |
| Tema da oficina | Detetives da Lógica |
| Público-alvo | Crianças de 8 a 10 anos |

### Equipe

- Alya
- Ayme
- Carolina
- Daniela Venturi
- Mariana

## A oficina

A estrutura geral da oficina foi definida pela organização do projeto e mantida pela equipe. Dentro dela, cada etapa podia ser mantida, adaptada ou substituída.

### Ideia central

- **O que queremos que as crianças aprendam:** como investigar problemas com lógica e trabalho em equipe, observando tudo por vários ângulos até achar a melhor solução.
- **O que elas vão fazer:** absorver um conteúdo um pouco mais teórico sobre lógica e aplicá-lo em desafios práticos, por meio de competições e atividades lúdicas que mantêm a turma engajada.
- **Como vamos perceber que aprenderam:** observando a velocidade e a habilidade nas atividades e, ao final, ouvindo as próprias crianças na conversa de feedback.


### Resumo de cada etapa

1. **Acolhida (Dinâmica da Teia).** As crianças ficam em roda, passam um rolo de linha de uma para outra e cada uma diz nome, idade e algo de que gosta, segurando um pedaço da linha. Forma-se uma grande teia. O desafio é desfazê-la e enrolar a linha de volta, seguindo uma lógica para retornar pelo caminho percorrido, sem soltar nem arrebentar a linha.
2. **Descoberta.** Slides que perguntam "O que vocês acham que é lógica?", retomam a teia e mostram as quatro etapas para resolver um problema: observar, descobrir padrões, criar hipóteses e testar.
3. **Atividade lúdica (Código Secreto).** Com um cartaz do alfabeto numerado, cada dupla recebe uma frase escrita só com números e a decifra, substituindo cada número pela letra correspondente. A correção é coletiva.
4. **Atividade no computador.** As crianças exploram jogos de raciocínio lógico, sequências e resolução de problemas no site Racha Cuca, incentivadas a observar, testar possibilidades e pensar antes de cada movimento.
5. **Desafio prático (Sanduíche).** Em pequenos grupos, as crianças dão instruções em sequência para um monitor montar um sanduíche com peças de EVA. Nenhuma etapa pode ser pulada e o monitor segue exatamente o que foi dito.
6. **Quiz final.** A turma é dividida em 4 grupos que competem resolvendo desafios de lógica: ligar pontos com fio para formar uma imagem, montar algo na sequência correta e desvendar uma frase em código para realizar uma ação.
7. **Fechamento.** Roda de conversa sobre a tarde, entrega de lembrancinha (doces) e carimbo de assiduidade para todos.

## Onde o Código Secreto se encaixa

- **Etapa 3, atividade lúdica:** no planejamento, as crianças decifram frases em números usando um cartaz. Este site trabalha a mesma ideia (associar número e letra) em formato de jogo, com pontos e ranking.
- **Etapa 6, quiz final:** um dos desafios é desvendar uma frase em código. O site pode servir de treino para isso.

O site é um **complemento**. Ele não substitui as atividades planejadas da oficina (cartaz, Racha Cuca, sanduíche e quiz em grupos).

### Habilidades trabalhadas

Leitura, atenção, raciocínio lógico, associação entre números e letras, curiosidade, autonomia e interação entre as crianças.

## Por que este projeto foi feito com o Claude

A ideia inicial era algo **rápido**: uma página simples para levar à aula e mostrar o código secreto às crianças, só um teste. Pedimos ajuda ao **Claude** (assistente de IA da Anthropic) para montar essa página.

Depois que a primeira versão funcionou, o projeto foi crescendo aos poucos:

1. uma página única com o jogo, a tabela do código e um tradutor de número para letra;
2. nome do aluno, pontuação, cronômetro e um ranking para fazer competição;
3. como várias crianças jogariam em vários computadores, o ranking precisou ser salvo em um banco de dados. Por isso o projeto virou um sistema com back-end e front-end, publicado na web.

Em resumo: **a maior parte do código foi gerada pelo Claude** a partir de pedidos da equipe, e depois ajustada conforme as nossas necessidades (por exemplo, a aba Tradutor só aparece depois que a criança termina a partida). Este projeto **não é um sistema de produção**: foi pensado para um uso pontual, em uma aula. Se for reaproveitado, o código deve ser revisado.

## Como o jogo funciona

1. A criança escreve o nome e clica em **Começar**.
2. Aparecem 10 palavras, uma de cada vez, escritas em números. A criança digita a palavra. Acentos e letras maiúsculas ou minúsculas não importam.
3. Palavras do jogo: BOLA, GATO, CASA, BANANA, ESCOLA, LOGICA, ROBO, CODIGO, PENSAR e SEGREDO.
4. Cada palavra vale até 10 pontos. Cada dica custa 2 pontos e cada erro custa 1 ponto, e o mínimo por palavra é 1 ponto. A pontuação máxima é 100.
5. A dica revela as letras da esquerda para a direita, uma por vez, e nunca revela a última letra.
6. Ao terminar, a pontuação e o tempo vão para o **ranking da turma**, ordenado por pontos. Em caso de empate, vence quem foi mais rápido.
7. Se a criança jogar de novo com o mesmo nome, só o melhor resultado fica no ranking.
8. O ranking mostra os 30 melhores e se atualiza sozinho a cada 5 segundos.
9. A aba **Tabela do código** mostra A = 1 até Z = 26 para consulta.
10. A aba **Tradutor** (texto para número e número para texto) só aparece depois que a primeira partida termina.
11. O botão **Zerar ranking** apaga todos os resultados e exige a senha do professor.

## Tecnologias e arquitetura

| Parte | Ferramentas |
|---|---|
| Back-end | Python, Flask, SQLite (servido com Gunicorn na publicação) |
| Front-end | Vue.js 3, Axios, Vite |
| Hospedagem | GitHub e Render (plano gratuito) |

Tudo está no mesmo repositório. O Flask entrega a API e também o site já compilado:

## Créditos

- Equipe da oficina: Alya, Ayme, Carolina, Daniela Venturi e Mariana (Univille).
- Código gerado com a ajuda do [Claude](https://claude.ai), da Anthropic, e ajustado pela equipe da oficina.

# Camada Deco — regras canônicas

Este arquivo é a fonte da camada Deco. Ele reúne seis peças e dois guardrails
de auditoria aprovados em 18/08/2026 para a organização que mantém este fork.

A camada é aditiva: ela não cria uma segunda metodologia, não redefine specs,
fases ou gates do Specsfy e não substitui nenhuma skill do framework. Onde o
Specsfy já resolve, a camada não repete.

Status desta edição: `v0.1.0-draft` — contrato documental. A instalação
automática e a verificação executável chegam na v0.2.

## Peças

### Peça 1 — Contrato de handoff

Ao encerrar uma sessão de trabalho, registrar um handoff em Markdown com
exatamente cinco campos fixos, nesta ordem e com estes nomes:

1. Projeto e data — `DD/MM/AAAA`
2. Estado verificável — branch, HEAD, o que está no ar e o que não subiu
3. Decisões da sessão + porquê
4. Pendências e próximo passo
5. Evidências e links canônicos

Regras do contrato:

- Formato **delta, não diário**: registrar apenas o que a sessão mudou.
- **Regra dos 30 segundos**: se o handoff não puder ser relido em meio minuto,
  virou diário; cortar antes de gravar.
- Contexto estável que já vive em documento canônico é **linkado, nunca
  duplicado**.
- O campo "Decisões da sessão + porquê" exige o porquê; registrar apenas o quê
  não cumpre o contrato.
- **Um único handoff ativo por projeto.** O anterior recebe status `SUPERADO`
  e a indicação "substituído por", apontando para o sucessor.

**Por quê:** a amnésia entre sessões é o modo de falha que nenhum SDD puro
cobre sozinho. Sem artefato em disco curado por humano, o contexto é
reconstruído à mão ou vem de transcript bruto e de resumo com perda.

**Como aplicar:** mecânica de arquivos na peça correspondente do módulo
(`deco/templates/HANDOFF.md` e `deco/templates/session-handoff.md`).

### Peça 2 — Ponte Notion ↔ repositório

O Notion é o **upstream humano** do contexto de negócio. O repositório carrega
uma **cópia derivada e autossuficiente** desse contexto.

- Nada dentro do repositório pode depender do MCP do Notion estar conectado em
  tempo de execução.
- Atualizar a cópia derivada é trabalho explícito, nunca sincronização
  automática.
- Contexto estável é **referenciado, não duplicado** — vale entre repositório e
  Notion e também entre documentos do próprio repositório.

**Por quê:** mantém o Notion acima do ambiente de execução sem transformar uma
conveniência em dependência de runtime. O projeto continua legível se o MCP
cair ou se o harness mudar.

### Peça 3 — Protocolo de decisão para não-especialista

Toda escolha técnica levada a quem conduz o projeto chega com:

1. as **opções** viáveis;
2. o **trade-off de cada opção** — o que se ganha e o que se perde;
3. uma **recomendação explícita**, identificada como tal.

Encerrar a mensagem apenas com "qual você prefere?" não cumpre o protocolo:
sem trade-off e sem recomendação, a decisão é empurrada para quem tem menos
informação técnica para tomá-la.

**Por quê:** quem orquestra decide melhor vendo o leque completo e o parecer de
quem analisou, em vez de receber uma direção única já fechada ou uma pergunta
aberta sem subsídio.

### Peça 4 — Régua de validação do orquestrador

Toda entrega ou pedido de aprovação de gate inclui, em linguagem simples:

- **o que testar**;
- **onde clicar ou qual comando executar**;
- **o resultado esperado**;
- como chegar a esse veredito **sem ler o diff**.

**Por quê:** quem conduz o projeto não lê diff de código. Sem essa régua, a
aprovação de um gate vira confiança no agente em vez de verificação.

### Peça 5 — Engenharia reversa de legado

**Status: `BACKLOG`.** Peça canônica reconhecida, **não instalada e não
implementada na v0.1**.

Escopo previsto: transformar código antigo sem documentação em especificação
utilizável pelo método. Preferir ferramenta pronta a construir do zero.

**Por quê o adiamento:** é a peça mais cara e a única que não tem uso no dia 1;
só entra quando um projeto desta camada precisar atacar legado real.

### Peça 6 — Guardrail de negócio

Distinguir **Build-to-Earn** (trabalho que gera ou deve gerar retorno) de
**Build-to-Learn** (trabalho de aprendizado). Tecnologia nova entra primeiro em
contexto Build-to-Learn, não no projeto que precisa entregar.

- O agente **recusa** o pedido quando ele viola uma regra de negócio registrada
  e **aponta a regra violada** antes de propor ajuste — nunca recusa em
  silêncio nem inventa outro motivo.
- Onde a disciplina se aplicar, valem teste antes do código e a recusa de
  entregar sem especificação prévia.

**Por quê:** impede que o projeto vire estudo sem retorno e dá ao agente um
critério objetivo para dizer não.

## Guardrails de auditoria

Os dois itens abaixo saíram da auditoria de modos de falha de agentes contra o
Specsfy (18/08/2026). Eles **não são peças** e não recebem numeração na série
acima: são reforços pontuais onde o método cobre apenas parcialmente.

### Guardrail A — Quem implementa não aprova sozinho

Quem implementou uma tarefa não fecha sozinho o próprio gate. O fechamento
exige revisão distinta da execução: outro agente, outra sessão ou validação
humana explícita. Quando executor e aprovador coincidirem, sinalizar antes de
prosseguir.

### Guardrail B — Pendência documental bloqueia entrega

Uma entrega não fecha com pendência documental em aberto nos artefatos que a
especificação exige. Marcar a pendência não basta: ou ela é resolvida, ou a
exceção é aceita explicitamente por quem orquestra.

## Proveniência

Decisão de método e catálogo das seis peças: Notion, 18/08/2026. Guardrails A e
B: auditoria dos modos de falha registrada na mesma data. O Notion permanece
como fonte normativa; este arquivo é a cópia derivada e autossuficiente
prevista na peça 2.

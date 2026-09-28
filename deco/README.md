# Módulo `deco/`

Extensão organizacional mantida no fork Educamundo do Specsfy. Reúne regras de
comportamento, o contrato de handoff entre sessões e os artefatos necessários
para instalar esse conjunto em projetos consumidores.

## Finalidade

O Specsfy resolve especificação, fases e gates. Existem lacunas que ele não
cobre por ser genérico: continuidade entre sessões, a forma como uma decisão
técnica chega a quem não é especialista, e regras de negócio próprias da
organização. Esta camada cobre essas lacunas sem tocar no método.

## Relação upstream / fork

| Origem | Papel |
| --- | --- |
| `promovaweb/specsfy` (upstream) | metodologia, skills, especialistas e CLI |
| `EducamundoBR/specsfy` (este fork) | espelho do upstream **mais** o módulo `deco/` |
| `deco/` | conteúdo exclusivo do fork; nunca proposto ao upstream |

O módulo é aditivo por construção: não altera `cli/`, `skills/` ou
`specialists/`. Sincronizar com o upstream continua sendo um fast-forward, e há
exatamente **dois pontos de contato** com arquivo compartilhado, ambos no
`AGENTS.md` da raiz:

1. a linha de `deco/` na tabela de módulos;
2. o parágrafo de roteamento e limites do módulo, na seção "Fonte da verdade".

Os dois precisam ser reconciliados a cada merge de upstream que toque esse
arquivo.

## O que a camada cobre

- Continuidade entre sessões (contrato de handoff de cinco campos).
- Contexto de negócio que vive fora do repositório, trazido como cópia derivada.
- Forma de apresentar decisões técnicas a quem orquestra sem ser especialista.
- Como validar uma entrega sem ler diff.
- Regras de negócio da organização e o dever de recusar quando violadas.

## O que a camada não cobre

- Não define specs, fases, gates, templates de spec nem critérios de aceite —
  isso é do Specsfy.
- Não substitui nenhuma skill do framework.
- Não é uma segunda metodologia, não é fonte normativa paralela e não
  transforma a raiz do monorepo em projeto consumidor.
- Engenharia reversa de legado é peça canônica, mas está em `BACKLOG` e não
  entra na v0.1.

## Árvore do módulo

```text
deco/
├── README.md                          este documento
├── manifest.json                      fonte da distribuição (papéis, destinos, hashes)
├── rules/
│   ├── canonical.md                   seis peças + dois guardrails (normativo)
│   └── candidates.md                  heurísticas não aprovadas (não normativo)
├── skills/
│   ├── fechar-sessao-deco/SKILL.md    procedimento do contrato de handoff
│   ├── git-guardian/SKILL.md          preflight Git executável (SPEC-0002/T004)
│   └── session-guardian/SKILL.md      abertura e fechamento de sessão (SPEC-0002/T005)
├── templates/
│   ├── HANDOFF.md                     ponteiro para o snapshot ativo
│   ├── session-handoff.md             base do snapshot datado
│   ├── review-request.md              contratos da rodada de revisão (SPEC-0002/T006)
│   ├── review-verdict.md              modelo do revisor
│   └── correction-report.md           modelo do implementador na reconferência
├── fixtures/handoff/                  cenários documentais para o verifier da v0.2
├── fixtures/review-round/             artefatos de rodada válidos e inválidos (T006)
└── specs/                             specs do desenvolvimento da própria camada
    └── <NNNN>-<slug>/
        ├── spec.md                    fonte normativa da fatia (Specsfy/2.0)
        └── research/                  evidência derivada das fontes externas
```

Subpastas adicionais de uma fatia — contratos materializados, harness de
conformidade, registro de piloto — não são estrutura fixa deste módulo: cada
fatia as define no seu Plan Gate. Não presuma caminhos que a spec ainda não
fixou.

### Sobre `deco/specs/`

Esta pasta guarda as specs que governam o **desenvolvimento da camada**. Ela não
torna o monorepo um projeto consumidor e não cria fonte normativa paralela:

- **Decisão local de roteamento:** nesta versão, as specs da camada vivem em
  `deco/specs/<NNNN>-<slug>/`, sem segmento físico `<estado>/`. São specs de
  definição da própria camada distribuível; o estado vive no front matter ou
  cabeçalho e nos gates. A decisão permanece sujeita ao Definition Gate e não é
  regra global do Specsfy: projetos consumidores continuam seguindo o próprio
  roteamento aplicável.
- A proibição de `AGENTS.md:37-38` é sobre criar `specs/` **na raiz** do
  monorepo. `deco/specs/` vive dentro do módulo, cujo ownership o `AGENTS.md`
  já atribui a este fork.
- A fonte da camada continua sendo `deco/rules/canonical.md`. Uma spec aqui
  governa o **comportamento da fatia em desenvolvimento** — o escopo que
  `docs/develop/context/README.md:72-81` já atribui a `spec.md` — e nada mais.
- A precedência da spec é **interina**. Enquanto a fatia atravessa Definition,
  Plan e Delivery, a spec governa aquela fatia. Depois da materialização e do
  aceite, **os arquivos operacionais produzidos passam a ser a norma técnica
  vigente** e a spec passa a registrar decisão, rastreabilidade e histórico, sem
  competir com eles. Decisão de negócio aprovada no Notion mantém precedência
  própria em qualquer momento.
- Promover contratos de uma fatia a `deco/rules/canonical.md` é decisão separada,
  com gate próprio, registrada na spec correspondente.
- Nada em `deco/specs/` é instalado em consumidores: o `manifest.json` não a
  declara, e seu `filesScope` cobre apenas artefatos de distribuição.

Specs vigentes:

| Spec | Assunto | Estado |
| --- | --- | --- |
| `0001-ponte-notion-repositorio/` | ponte Notion ↔ repositório: cockpit, Consulta SDD, Modo B, proveniência e reconciliação | `Defined`; Definition e Plan Gates `Passed`; Delivery Gate `Pending` |
| `0002-governanca-sdd/` | governança transversal do SDD: risco, gates, preflight, sessão e repasse | `Defined`; Definition e Plan Gates `Passed`; Delivery Gate `Pending` |

## Destinos pretendidos no consumidor

| Fonte | Destino | Instalação |
| --- | --- | --- |
| `deco/rules/canonical.md` | `.deco/RULES.md` | obrigatória |
| `deco/rules/candidates.md` | `.deco/CANDIDATES.md` | nunca por padrão; opcional sob pedido |
| `deco/templates/HANDOFF.md` | `docs/HANDOFF.md` | obrigatória |
| `deco/templates/session-handoff.md` | base de `docs/sessoes/<AAAA-MM-DD>-handoff.md` | obrigatória |
| `deco/skills/fechar-sessao-deco/SKILL.md` | ver matriz por harness abaixo | obrigatória |
| `deco/manifest.json` | não instalado | nunca |
| estado instalado | `.deco/lock.json` | gerado na instalação |

### Matriz de destinos por harness

Baseada no comportamento verificado do Specsfy 0.22.2 (`cli/src/installer.ts`),
não em suposição:

| O que | Onde o Specsfy 0.22.2 escreve | Destino da camada |
| --- | --- | --- |
| Skills do framework | `.agents/skills/<nome>/` | `.agents/skills/fechar-sessao-deco/` |
| Roteamento de agentes | bloco gerenciado em `AGENTS.md` e `CLAUDE.md` da raiz, entre `<!-- specsfy:framework:start -->` e `<!-- specsfy:framework:end -->` | bloco gerenciado próprio da camada, delimitado por marcadores distintos |
| Spec normativa | `.specsfy/Spec.md` | não usado pela camada |
| Templates gerenciados | `.specsfy/templates/` (com precedência de `.specsfy/templates/custom/`) | não usado pela camada |
| Lock | `.specsfy/skills-lock.json` | `.deco/lock.json`, separado |

O installer do 0.22.2 grava skills apenas em `.agents/skills/`; não cria
`.claude/skills/`, `.codex/` ou `.cursor/` no consumidor. A camada segue o mesmo
caminho e não inventa diretórios por harness.

### Roteamento futuro

O carregamento da camada pelos agentes deve acontecer por **bloco gerenciado e
idempotente** em `AGENTS.md` e `CLAUDE.md` do consumidor, com marcadores
próprios, preservando integralmente o texto humano e o bloco do Specsfy que já
existem nesses arquivos. Reescrever o arquivo inteiro está descartado.

## Fonte, instalação e lock

Três conceitos distintos, deliberadamente separados:

- **Fonte** — o conteúdo versionado aqui em `deco/`, descrito por
  `manifest.json`. É o que este fork mantém.
- **Instalação** — a cópia gravada no projeto consumidor nos destinos da tabela
  acima.
- **Lock** — `.deco/lock.json` no consumidor: o que foi instalado, em que
  versão da camada e com quais hashes. É o que permite detectar personalização
  local e atualizar sem sobrescrever trabalho de quem usa.

`manifest.json` descreve a fonte e **não é** o lock do consumidor: não carrega
data de instalação nem estado de nenhum projeto.

## Compatibilidade

Declarada em `manifest.json`, campo `compatibleSpecsfy`. A v0.1 é escrita contra
o Specsfy `0.22.2`. Faixas futuras exigem reconferir os caminhos da matriz por
harness, porque eles vêm do comportamento do instalador do framework, que muda
entre versões.

## Política de atualização — requisito futuro da v0.2

As duas seções de política abaixo especificam o comportamento esperado do
instalador e do verifier da v0.2. **Não são normas operacionais para agentes na
v0.1**: nada aqui é roteado a agentes, participa de gate ou vincula o
comportamento de quem trabalha no projeto hoje. A norma da camada está em
`deco/rules/canonical.md`, e estas políticas não são movidas para lá.

- A camada tem ciclo de versão próprio (`layerVersion`), independente do
  `VERSION` da raiz do monorepo, que governa os artefatos publicáveis do
  Specsfy.
- A atualização é idempotente: reinstalar a mesma versão sobre um consumidor já
  atualizado não altera nenhum arquivo.
- Cada atualização confere o lock do consumidor antes de escrever.

## Política de conflito — requisito futuro da v0.2

Também especificação do instalador/verifier da v0.2, não norma operacional da
v0.1.

- Arquivo instalado que divergir do hash registrado no lock é tratado como
  **personalização local** e não é sobrescrito sem confirmação explícita.
- Bloco gerenciado em `AGENTS.md`/`CLAUDE.md` é substituído apenas dentro dos
  seus marcadores; texto fora deles nunca é tocado.
- `candidates.md` não participa de conflito porque não é instalado por padrão.
- Divergência entre `docs/HANDOFF.md` e o snapshot apontado é erro de
  verificação, não conflito de instalação: o verifier reporta, não corrige
  sozinho.
- O status de um snapshot é determinado **exclusivamente** pelo campo
  estrutural `Status:` logo abaixo do título. É proibido inferir `ATUAL` ou
  `SUPERADO` procurando essas substrings livremente no corpo: as mesmas
  palavras aparecem legitimamente em decisões, histórico e explicações, e essa
  ocorrência não altera o status do snapshot.

## Fases

- **v0.1 — documental (esta).** Regras, contrato de handoff, templates, skill,
  manifesto e fixtures. Sem código executável: nada instala nem verifica
  automaticamente.
- **v0.2 — executável.** `installer/install.mjs` e `installer/verify.mjs`,
  testes sobre as fixtures, escrita atômica do par ponteiro/snapshot e geração
  do `.deco/lock.json`.

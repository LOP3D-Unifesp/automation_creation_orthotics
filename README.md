# Orthosis Creation Automation

Addon para Blender focado em evoluir o fluxo de criacao de orteses em etapas pequenas e seguras.

Nesta versao, o foco esta em melhorar a organizacao da interface e a usabilidade da preparacao do modelo, mantendo as funcionalidades existentes.

## Fluxo por etapas

### Etapa atual

No N-panel, o addon agora esta organizado em 3 paineis diretos (cada um recolhivel):

- `Inicializacao`
- `Preparar modelo`
- `Roadmap`

Isso deixa a tela mais limpa e facilita focar em uma etapa por vez.

### Proxima etapa (implementacao)

A proxima entrega implementara as primeiras acoes reais de inicializacao:

- `template.blend` obrigatorio para preparar o ambiente
- importacao de STL

## O que funciona hoje

- Atualizar contagem de geometria (`vertices` e `faces`)
- Decimacao com 3 estrategias (`Collapse`, `Un-Subdivide`, `Planar`)
- Alinhamento por eixo (`X`, `Y`, `Z`)

## Como usar a decimacao agora

Fluxo recomendado:

1. Ajuste o parametro no painel.
2. Clique em `Aplicar <modo>`.
3. Aguarde a aplicacao.
4. Confira popup de sucesso e contagem atualizada automaticamente.

### Como escolher a estrategia

- `Collapse`: reduz poligonos mantendo a forma geral.
- `Un-Subdivide`: tenta desfazer subdivisoes regulares.
- `Planar`: simplifica regioes quase planas.

## Roadmap de funcionalidades futuras

Ordem planejada no painel:

1. Encontrar landmarks anatomicos
2. Rigging
3. Reposicionamento anatomico

## Onde encontrar no Blender

Depois de instalar e ativar o addon:

- `3D Viewport`
- barra lateral `N`
- aba `Automacao de Orteses`
- painel `Automacao na Criacao de Orteses`

## Requisitos

- Blender com API Python compativel
- `bl_info` declara compatibilidade minima com Blender `3.0.0`
- desenvolvimento e uso atual no contexto do Blender `3.6`

## Instalacao

### Opcao 1: instalar como `.zip`

1. Compacte a pasta do addon em um arquivo `.zip`.
2. No Blender, abra `Edit > Preferences > Add-ons`.
3. Clique em `Install...`.
4. Selecione o `.zip`.
5. Ative o addon `Orthosis Creation Automation`.
6. Clique em `Save Preferences` para manter habilitado nas proximas sessoes.

### Opcao 2: copiar para a pasta de add-ons

Copie a pasta `automation_creation_orthotics` para:

```text
C:\Users\<usuario>\AppData\Roaming\Blender Foundation\Blender\3.6\scripts\addons\
```

Depois:

1. Abra o Blender.
2. Va em `Edit > Preferences > Add-ons`.
3. Procure por `Orthosis Creation Automation`.
4. Marque a caixa para habilitar.

## Teste manual rapido

1. Abrir o Blender.
2. Importar uma malha e selecionar o objeto.
3. Abrir a aba `Automacao de Orteses`.
4. Validar os 3 paineis diretos (`Inicializacao`, `Preparar modelo`, `Roadmap`).
5. Clicar em `Atualizar Contagem`.
6. Ajustar parametro e aplicar uma decimacao.
7. Confirmar popup de sucesso e nova contagem de vertices/faces.
8. Escolher eixo e clicar em `Alinhar`.

## Estrutura do projeto

```text
automation_creation_orthotics/
|- __init__.py
|- operators/
|- panels/
|- properties/
|- utils/
`- menus/
```


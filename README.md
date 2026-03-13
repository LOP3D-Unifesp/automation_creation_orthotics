# Orthosis Creation Automation

Addon para Blender voltado a automatizar etapas iniciais do preparo de modelos 3D para criacao de orteses. O foco atual do projeto e apoiar a manipulacao de malhas importadas, com ferramentas para reduzir poligonos, inspecionar contagem de geometria e alinhar o modelo a um eixo de referencia.

## O que o addon faz hoje

Na versao atual, o painel do addon expoe 3 grupos de acoes:

- Decimacao da malha com 3 estrategias:
  - `Collapse`: reduz a malha mantendo uma proporcao das faces.
  - `Un-Subdivide`: tenta reverter etapas de subdivisao.
  - `Planar`: dissolve faces quase coplanares com base em um angulo.
- Contagem de geometria:
  - mostra o numero de vertices e faces do objeto ativo.
- Alinhamento por eixo:
  - reposiciona o objeto para alinhar seu centroide ao eixo `X`, `Y` ou `Z`.

## Onde encontrar no Blender

Depois de instalar e ativar o addon, ele aparece no `3D Viewport`:

- Barra lateral `N`
- Aba `Automacao de Orteses`
- Painel `Automacao na Criacao de Orteses`

## Requisitos

- Blender com API Python compativel com o addon
- O `bl_info` declara compatibilidade minima com Blender `3.0.0`
- O projeto esta organizado e sendo usado no contexto do Blender `3.6`

## Instalacao

### Opcao 1: instalar como `.zip`

1. Compacte a pasta do addon em um arquivo `.zip`.
2. No Blender, abra `Edit > Preferences > Add-ons`.
3. Clique em `Install...`.
4. Selecione o `.zip`.
5. Ative o addon `Orthosis Creation Automation`.
6. Clique em `Save Preferences` se quiser mante-lo habilitado nas proximas sessoes.

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

## Fluxo de uso recomendado

### 1. Importar e selecionar a malha

O addon espera que exista um objeto ativo do tipo `MESH`. Se nenhum objeto estiver selecionado, ou se o objeto ativo nao for uma malha, os operadores cancelam a acao e exibem um popup de erro.

### 2. Atualizar a contagem

Clique em `Atualizar Contagem` para preencher os campos do painel com:

- numero de vertices
- numero de faces

Isso e util como referencia antes e depois da decimacao.

### 3. Reduzir a malha

Escolha uma das estrategias:

- `Collapse`
  - abre um popup com o parametro `Ratio`
  - usa o modificador `DECIMATE` no modo `COLLAPSE`
- `Un-Subdivide`
  - abre um popup com o numero de `Iterations`
  - usa o modificador `DECIMATE` no modo `UNSUBDIV`
- `Planar`
  - abre um popup com o `Angle Limit`
  - usa o modificador `DECIMATE` no modo `DISSOLVE`

O modificador e aplicado automaticamente ao final da operacao.

### 4. Alinhar o modelo a um eixo

Selecione o eixo desejado no painel:

- `X`
- `Y`
- `Z`

Depois clique em `Alinhar`.

O operador:

1. garante que o objeto ativo esteja selecionado
2. alterna entre `OBJECT MODE` e `EDIT MODE`
3. calcula o centroide da malha
4. desloca o objeto para alinhar o centroide ao eixo escolhido
5. ajusta a origem para `ORIGIN_CENTER_OF_MASS`
6. mostra um popup informando sucesso ou erro

## Comportamento interno do codigo

### Registro do addon

O ponto de entrada e [__init__.py](/C:/Users/ganga/AppData/Roaming/Blender%20Foundation/Blender/3.6/scripts/addons/automation_creation_orthotics/__init__.py).

Ele registra:

- propriedades de cena
- operadores de interface
- painel do addon

Tambem cria estas propriedades em `bpy.types.Scene`:

- `vertices`
- `faces`
- `align_limb_props`

### Painel

O layout principal esta em [panels/orthosis_automation.py](/C:/Users/ganga/AppData/Roaming/Blender%20Foundation/Blender/3.6/scripts/addons/automation_creation_orthotics/panels/orthosis_automation.py).

Esse arquivo define:

- botoes de decimacao
- atualizacao de contagem
- selecao do eixo
- botao de alinhamento

### Operadores

Os operadores atualmente expostos estao em:

- [operators/decimation.py](/C:/Users/ganga/AppData/Roaming/Blender%20Foundation/Blender/3.6/scripts/addons/automation_creation_orthotics/operators/decimation.py)
- [operators/align.py](/C:/Users/ganga/AppData/Roaming/Blender%20Foundation/Blender/3.6/scripts/addons/automation_creation_orthotics/operators/align.py)
- [operators/alert.py](/C:/Users/ganga/AppData/Roaming/Blender%20Foundation/Blender/3.6/scripts/addons/automation_creation_orthotics/operators/alert.py)

Resumo:

- `ACO_OT_decimate_collapse`
- `ACO_OT_decimate_un_subdivide`
- `ACO_OT_decimate_planar`
- `ACO_OT_number_of_vertices_and_faces`
- `ACO_OT_align_limb_axis`
- `ACO_OT_alert_error_popup`
- `ACO_OT_alert_info_popup`

### Utilitarios

Os comportamentos auxiliares ficam em `utils/`:

- `selection.py`
  - ativacao de objeto
  - troca de modo
  - parent com armature
- `object.py`
  - decimacao por tipo
  - calculo de centroide
  - tamanho por eixo
  - criacao de bones a partir de posicoes
- `transform.py`
  - alinhamento do objeto ao eixo
  - reposicionamento no eixo escolhido
- `decorator.py`
  - validacao para exigir um objeto `MESH` ativo
- `ui.py`
  - rotinas auxiliares relacionadas a objeto ativo e handlers experimentais

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

## Funcionalidades em desenvolvimento ou nao expostas no painel

O repositorio ja contem codigo para outras ideias, mas elas nao fazem parte do fluxo principal disponivel hoje na interface:

- criacao de bones e armature em [operators/rigging.py](/C:/Users/ganga/AppData/Roaming/Blender%20Foundation/Blender/3.6/scripts/addons/automation_creation_orthotics/operators/rigging.py)
- preenchimento de lacunas de malha em [operators/fill_in_gaps.py](/C:/Users/ganga/AppData/Roaming/Blender%20Foundation/Blender/3.6/scripts/addons/automation_creation_orthotics/operators/fill_in_gaps.py)
- handlers automaticos em [utils/ui.py](/C:/Users/ganga/AppData/Roaming/Blender%20Foundation/Blender/3.6/scripts/addons/automation_creation_orthotics/utils/ui.py)

Esses trechos devem ser tratados como experimentais ate serem registrados no addon e testados no painel.

## Limitacoes atuais

- O addon foi escrito assumindo que o usuario esta trabalhando com uma malha ativa.
- Parte do fluxo usa `bpy.ops`, entao o contexto do Blender importa bastante.
- A interface atual cobre apenas decimacao, contagem e alinhamento.
- Existem modulos no repositorio que ainda nao estao integrados ao `register()`.
- O codigo ainda tem espaco para padronizacao de nomes, tratamento de erros e documentacao inline.

## Sugestao de teste manual

Um teste rapido para validar o addon e:

1. abrir o Blender
2. importar uma malha de membro superior ou inferior
3. selecionar o objeto
4. abrir a aba `Automacao de Orteses`
5. clicar em `Atualizar Contagem`
6. executar uma das decimacoes
7. atualizar a contagem novamente
8. escolher um eixo e clicar em `Alinhar`

## Objetivo do projeto

O objetivo deste addon e servir como base para um fluxo mais automatizado de preparacao de modelos para orteses dentro do Blender, reduzindo tarefas repetitivas e aproximando o processo tecnico das necessidades do laboratorio.

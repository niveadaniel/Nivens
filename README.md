# Nivens
Projeto de TCC, desenvolvido para Fatec.

## Árvore de diretórios

```markdown
├───bot
│   └───__pycache__
├───nivensapp
│   ├───migrations
│   ├───templates
|───nivensproject 
└───static
    ├───bootstrap
    │   ├───css
    │   └───js
    ├───css
    ├───DataTables
    │   ├───DataTables-1.10.24
    ├───icons
    ├───img
    ├───javascript
    └───jquery
```

************
## Como utilizar este repositório

1. Clone este repositório:
```
git clone https://github.com/niveadaniel/Nivens.git
```

2. Crie um ambiente dedicado. É possível criar esse ambiente usando Anaconda:

```python
conda create --name myenv
```

Para ativar o ambiente digite:

```python
conda activate myenv
```

Para desativar digite:

```python
conda deactivate
```


Ou com Virtualenv:

- Instale o virtualenv no diretório desejado:
```python
pip install virtualenv
```
- Em seguida digite:

```python
python3 -m venv env
```

Para ativar o ambiente digite: 

```python
source myenv/bin/activate
```

Para desativar digite:
```python
(myenv) $ deactivate
``` 

3. Após criar e ativar um ambiente virtual no seu terminal, navegue até a pasta Nivens e digite:

```python
pip install -r requirements.txt
```

4. Aguarde a instalação das dependências e em seguida, crie uma banco de dados com nome **nivens** no seu servidor MySQL local e insira seus parâmetros de conexão locais no arquivo setting.py;

5. Dentro do projeto Nivens digite ```python manage.py createsuperuser``` para criar o usuário administrador local;

6. Para fazer as migrações do banco de dados digite ```python manage.py makemigrations``` ou ```python manage.py migrate```;

7. Para verficar as mudanças realizadas no projeto, digite ```python manage.py check``` e em seguida, ```python manage.py runserver```.

# Arquitetura de Microsserviços para Gestão Acadêmica

Este projeto implementa um sistema de gestão acadêmica utilizando uma arquitetura de microsserviços. O sistema é dividido em três serviços independentes: Gerenciamento, Reservas e Atividades.

## Arquitetura

A arquitetura é baseada em três microsserviços principais, cada um com sua própria responsabilidade e banco de dados, orquestrados com Docker Compose.

- **Gerenciamento (`gerenciamento`):** Responsável pelo cadastro e gerenciamento de Alunos, Professores e Turmas. Ele serve como a fonte da verdade para essas entidades e fornece seus IDs para os outros serviços.
- **Reservas (`reservas`):** Gerencia a lógica de reservas de salas, vinculando uma reserva a uma `Turma` existente no serviço de Gerenciamento.
- **Atividades (`atividades`):** Gerencia as atividades e notas, vinculando-as a um `Professor` e a uma `Turma` do serviço de Gerenciamento.

### Integração entre Serviços

A comunicação entre os microsserviços é síncrona e realizada através de chamadas HTTP REST.

- O serviço de **Reservas** consulta o serviço de **Gerenciamento** para validar a existência de uma `Turma` antes de criar ou atualizar uma reserva.
- O serviço de **Atividades** consulta o serviço de **Gerenciamento** para validar a existência de um `Professor` e de uma `Turma` antes de criar ou atualizar uma atividade.

Essa abordagem garante a consistência dos dados entre os serviços.

## Descrição da API

Cada microsserviço expõe uma API RESTful para gerenciar seus respectivos recursos. A documentação completa de cada API está disponível em Swagger UI.

- **Gerenciamento:** `http://localhost:5000/apidocs/`
- **Reservas:** `http://localhost:5001/apidocs/`
- **Atividades:** `http://localhost:5002/apidocs/`

### Endpoints Principais

#### Gerenciamento
- `GET, POST /alunos`
- `GET, PUT, DELETE /alunos/{id}`
- `GET, POST /professores`
- `GET, PUT, DELETE /professores/{id}`
- `GET, POST /turmas`
- `GET, PUT, DELETE /turmas/{id}`

#### Reservas
- `GET, POST /reservas`
- `GET, PUT, DELETE /reservas/{id}`

#### Atividades
- `GET, POST /atividades`
- `GET, PUT, DELETE /atividades/{id}`

## Instruções de Execução (com Docker)

Para executar o projeto, você precisa ter o Docker e o Docker Compose instalados.

1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_DIRETORIO>
   ```

2. Suba os contêineres com o Docker Compose:
   ```bash
   docker-compose up --build
   ```

Os serviços estarão disponíveis nos seguintes endereços:
- **Gerenciamento:** `http://localhost:5000`
- **Reservas:** `http://localhost:5001`
- **Atividades:** `http://localhost:5002`

Para parar a execução, pressione `Ctrl + C` no terminal onde o `docker-compose` está rodando e depois execute:
```bash
docker-compose down
```

## Integrantes do Grupo

- Ronaldo - RA 2403661
- Maycon - RA 2402929
- Luis Gabriel - RA 2402947

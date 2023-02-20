# Prefect threads

Projeto feito para estudo de uso de threads dentro de jobs do prefect, afim
de afilizar tarefas com muito delay de I/O.

## Reproduzindo

- Inicie a API que irá simular uma API externa, que devolve valores aleatórios
com meio segundo de delay em cada chamada

```
cd external_api
uvicorn main:app
```

- Inicie o prefect server com o comando

```
prefect server start
```

- Inicie um agent local com o comando

```
prefect agent local start --show-flow-logs
```

- Crie um projeto teste

```
prefect create project test
```

- Registre os flows no server

```
prefect register --project test -p flows/ --watch
```

## Notas e observações

- O simples fato de precisar criar 100 jobs mapeados com uma lógica simples
sendo processada em cada job, custou 20 segundos.
- O job que faz a requisição na API, mapeado, custou 1 minuto e 13 segundos.

## Resultados

- O flow que usa jobs para se comunicar com a API, levou **1 minuto e 15 segundos**
para finalizar.
- O flow que utilizou threads, levou **2 segundos** para finalizar.

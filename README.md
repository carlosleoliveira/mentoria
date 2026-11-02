# mentoria

Hello World em Python com pipeline de CI/CD no GitHub Actions
([.github/workflows/deploy.yml](.github/workflows/deploy.yml)).

A aplicação mostra o ambiente e a versão em que está rodando:

```text
Hello, World!
Running in: production
Version: main-abc1234
```

## Fluxo da pipeline

```text
PR:       lint -> test + scan -> (fim)
develop:  lint -> test + scan -> build+push (develop-<sha>) -> deploy (development)
main:     lint -> test + scan -> build+push (main-<sha>) -> [aprovação] -> deploy (production)
```

| Etapa | PR | develop | main |
| --- | --- | --- | --- |
| Lint (ruff) | ✅ | ✅ | ✅ |
| Testes + cobertura mínima de 70% | ✅ | ✅ | ✅ |
| Scan de segurança (Trivy, HIGH/CRITICAL) | ✅ | ✅ | ✅ |
| Build + push no ghcr.io | ❌ | ✅ `develop-<sha>` | ✅ `main-<sha>` |
| Aprovação manual | ❌ | ❌ | ✅ |
| Deploy | ❌ | ✅ automático em `development` | ✅ em `production`, após aprovação |

Cada etapa depende da anterior: se o lint falhar, nada mais roda; se os testes
ou o scan falharem, não há build nem deploy.

## Decisões

**Testes na develop.** A develop roda os mesmos testes da main, e uma falha
bloqueia o deploy. Os testes levam poucos segundos, e pegar o erro na develop é
mais barato do que descobrir só quando o código chega na main. O que a develop
não tem é a aprovação manual: o deploy em `development` é automático para dar
feedback rápido.

**Aprovação na main.** O job de deploy usa o environment `production`, que tem
*Required reviewers* configurado no GitHub. A pipeline para e só faz o deploy
depois que alguém aprova.

**Estratégia de tags.** A imagem recebe a tag `<branch>-<sha curto>`, por
exemplo `develop-0e10c1c`. Pela tag dá para saber de qual branch e de qual
commit a imagem veio, e cada commit gera uma tag diferente, ao contrário de
`latest`, que é sobrescrita. A mesma tag é injetada no build via
`--build-arg APP_VERSION` e exibida pela aplicação, e o deploy confere se a
versão exibida bate com a tag da imagem.

**Cobertura mínima de 70%.** É o suficiente para garantir que a lógica
principal está testada sem forçar testes artificiais. Hoje a cobertura está em
torno de 90%; só a chamada `main()` dentro do `if __name__ == "__main__"` não é
executada pelos testes.

**Deploy usa a imagem publicada.** O deploy não faz `docker build`: ele faz
`docker pull` da imagem do ghcr.io e roda o container, então o que vai para o
ambiente é exatamente a imagem publicada com aquela tag.

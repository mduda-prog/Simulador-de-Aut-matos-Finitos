# 🧠 Simulador de Autômatos Finitos (AFD, AFN, AFN-λ)

Este projeto é uma ferramenta de linha de comando desenvolvida para simular autômatos finitos a partir de arquivos de definição e arquivos de teste. Ele permite validar palavras conforme o comportamento esperado do autômato fornecido.

---

## 📌 Funcionalidade

A ferramenta identifica automaticamente o tipo de autômato (AFD, AFN ou AFN-λ) com base nas transições definidas no arquivo `.aut` e executa os testes especificados no arquivo `.in`.

Cada entrada testada é processada e o resultado é salvo no arquivo de saída com o seguinte formato:

```
palavra;resultadoesperado;resultado_obtido;tempo
```

---

## 📂 Estrutura dos Arquivos

### 📄 Arquivo `.aut` (Exemplo)

```txt
estados: q0,q1,q2
alfabeto: 0,1
inicial: q0
finais: q2
transicoes:
q0,ε,q1
q1,0,q1
q1,1,q2
```

### 📄 Arquivo `.in` (Exemplo)

```txt
01;aceita
0;rejeita
1;aceita
```

---

## ▶️ Como Executar

No terminal, execute:

```bash
python ferramenta.py maquina.aut testes.in resultado.out
```

**Parâmetros:**

- `maquina.aut`: arquivo com a definição do autômato
- `testes.in`: arquivo com as palavras de entrada e resultados esperados
- `resultado.out`: nome do arquivo de saída que será gerado

---

## 📤 Saída Esperada (`resultado.out`)

```txt
01;aceita;aceita;0.000032
0;rejeita;rejeita;0.000027
1;aceita;aceita;0.000030
```

---

## ⚙️ Requisitos

- Python 3.7 ou superior
- Execução via terminal (sem interface gráfica)

---

## 👨‍💻 Autor

Maria Eduarda da Silva Siqueira

Ciência da Computação-Universidade Estadual do Norte do Paraná

2025

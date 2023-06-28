# Customer Fidelity Program - Clustering
![Captura de tela 2023-06-28 151640 (1)](https://github.com/EDJR94/customer_fidelity/assets/128603807/22d6cf06-90a9-4bf4-baa2-4aae7440395f)



**All in One** é uma empresa fictícia de comércio eletrônico com sede no Reino Unido. Ela oferece uma ampla gama de produtos voltados para diversas categorias, incluindo decoração de casa, suprimentos para festas, acessórios de cozinha, soluções de armazenamento e muito mais.

## Problema de Negócio

Após vender com sucesso uma ampla variedade de produtos e acumular uma base substancial de clientes, a All in One reconhece o imenso valor oculto em seus dados de clientes. A empresa tem como objetivo aproveitar o poder da ciência de dados para obter **insights mais profundos** sobre sua base de clientes e aplicar esses insights de forma estratégica. Um de seus principais objetivos é **segmentar seus clientes** de forma eficaz. Essa segmentação permitirá à All in One compreender sua base de clientes em um nível mais detalhado, identificar grupos de clientes específicos com necessidades e preferências distintas, e adaptar seus esforços de marketing e ofertas de produtos de acordo.

Além disso, ao implementar um **programa de fidelidade**, a All in One busca cultivar relacionamentos mais fortes com os clientes e aumentar a retenção deles. Por meio da análise cuidadosa dos comportamentos dos clientes, padrões de compra e preferências, eles podem projetar um programa de fidelidade que ofereça incentivos personalizados, recompensas e benefícios exclusivos para diferentes segmentos de clientes. Essa abordagem personalizada não apenas promove a fidelidade do cliente, mas também cria um senso de apreço e pertencimento entre os clientes, fortalecendo ainda mais sua conexão com a marca.

## Dados

| Column Name | Description |
| --- | --- |
| InvoiceNo | Número da fatura, um identificador único para cada transação |
| StockCode | Código do produto, um identificador único para cada produto |
| Description | Descrição do produto |
| Quantity | Quantidade de produtos comprados em cada transação |
| InvoiceDate | Data e hora de cada transação |
| UnitPrice | Preço unitário de cada produto |
| CustomerID | ID do cliente, um identificador único para cada cliente |
| Country | País do cliente |

## Estratégia de Solução

A estratégia utilizada foi o método CRISP, um método cientifício baseado em ciclos:

![crisp](https://github.com/EDJR94/customer_fidelity/assets/128603807/ed8ae3f7-11e3-4561-a662-69cdbceea6e9)

Os ciclos do projeto foram dividas nas seguintes partes:

- Entendimento do Problema
- Descrição dos Dados
- Feature Engineering
- Estudo dos espaços de Embedding
- Definição dos Números de Clusters
- Estudos dos Algoritmos de Machine Learning
- Treinamento dos Modelos
- Análise Exploratória dos Dados
- Publicação em Nuvem
- Business Perfomance

## Feature Engineering

A seleção de features foi inspirada no modelo RFM e nas métricas de negócio geralmente utilizadas para uma empresa de negócio:

![RFM model](https://github.com/EDJR94/customer_fidelity/assets/128603807/d391a820-de8c-405d-bf05-fc17dbd28f76)
Através dos dados fornecidos foram criadas as features do modelo RFM: Recency, Frenquency e Monetary. Ao todo foram criadas 14 feature que estão disponíveis no notebook na pasta notebooks.

## Estudo do Espaço

Como o nosso dataset possui 15 colunas, procurei reduzir essa dimensionalidade para 2 dimensões utilizando algumas técnicas, como PCA, t-SNE, UMAP e redução de dimensionalidade por árvore utilizando a Random Forest. De acordo com o que mostrei no jupyter notebook, a redução que mais se mostrou separar mais os dados foi a baseada na árvore Random Forest:

![Untitled](https://github.com/EDJR94/customer_fidelity/assets/128603807/8fd1701d-76d4-4dd1-bf9c-2c67314d4d39)

## Definição do Número de Clusters

Para definir o melhor número de Clusters, utilizei 3 principais algoritmos de Clusterização:

- KMeans
- GaussianMixtureModel(GMM)
- Hierarchical Clustering(HCluster)

Para isso utilizei a métrica da Silhouette Score e a visualização em 2 dimensções da divisão feita pelo espaço da árvore para todos os modelos.

O melhor resultado foi obtido pelo HClustering:

![Untitled (1)](https://github.com/EDJR94/customer_fidelity/assets/128603807/316e2cb6-b84f-41e2-ad45-237069811bcf)

![Untitled (2)](https://github.com/EDJR94/customer_fidelity/assets/128603807/62f580f5-c985-4ea5-9b90-0fba1e18da46)

Tinham valores de silhueta mais altos mas optei por utilizar 5 pois também tem um bom valor de silhueta e tem uma boa divisão dos dados como podemos ver acima.

## Resultado

Após o treinamento do HClustering com 5 clusters e calcular as métricas, chegamos no seguinte resultado:

| Clusters | Monetary | Frequency | Recency | Percent | Qtd Products | Nº Products Returned | Relationship Duration | Nº Customers | AVG Order Value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Insiders | 6599.350958 | 0.086662 | 44.127336 | 15.033368 | 300.517523 | 50.135514 | 246.336449 | 856 | 1149.044275 |
| Potentials | 2119.202031 | 0.024631 | 101.500428 | 20.495258 | 152.898886 | 35.820908 | 122.052271 | 1167 | 927.101689 |
| At Risk | 1053.963650 | 0.029953 | 94.205109 | 24.060414 | 38.831387 | 11.224088 | 123.827007 | 1370 | 503.898063 |
| Sleeping | 280.102519 | 0.016227 | 149.095310 | 23.217422 | 22.301059 | 2.193646 | 32.131619 | 1322 | 233.020635 |
| Occasional | 93.049877 | 0.006202 | 187.118488 | 17.193537 | 9.247191 | 0.880490 | 0.391216 | 979 | 91.611593 |

Podemos observar que os ‘Insiders’ sao clientes que comprar um valor alto, uma grande quantidade de produtos, com alta frequência e baixa recência.

Os Clientes ‘Potentials’ são possíveis candidatos a se tornarem Insiders, porque eles compram bastante produtos as estão com a recência muito alta, ou seja, faz tempo desde sua última compra. 

Os clientes ‘At Risk’ são clientes que compram com uma frequência aceitável mas compram pouca quantidade de produtos. Se aumentarmos a quantidade de produtos comprados eles poderão ser candidados aos Insiders.

Os ‘Sleeping’ São clientes que compraram poucos produtos poucas vezes e não voltaram mais, sua duração da relação com a empresa durou em média apenas 32 dias. São clientes que devem ser incentivados a buscar a All in One mais vezes.

Por fim, os ‘Occasionals’ são clientes novos que compraram faz pouco tempo, devem ser incentivados a permanecerem na empresa.

Além disso foi feito um Dashboard no Metabase conectado com a base de dados da AWS(RDS) em nuvem para atualizar as dados conforme forem entrando mais clientes:

![Untitled (3)](https://github.com/EDJR94/customer_fidelity/assets/128603807/42afda78-bfde-4c17-a26a-b039f307adb7)

## Publicação em Nuvem

Após finalizar o projeto na minha máquina local criei um banco de dados na Amazon AWS para que os dados possam ser alimentados lá conforme forem entrando mais clientes novos. 

Também deixei um HD S3 da AWS para armazenar tanto os dados originais quantos os novos dados e o meu modelo treinado e salvo através do Pipeline. 

Dessa forma, consigo buscar meu modelo e meus dados atráves da AWS e o Metabase é atualizado conforme eu for alimentando a minha base de dados Postgres após passar esses dados pelo modelo treinado.

A estrutura do modelo em produção ficou conforme a figura abaixo:

![Untitled (4)](https://github.com/EDJR94/customer_fidelity/assets/128603807/f46820d4-e309-4356-a193-090df03f8d71)

Segue abaixo a estrutura do meu Pipeline: 

![Untitled (5)](https://github.com/EDJR94/customer_fidelity/assets/128603807/71c32544-3c64-4d11-b5da-a7bd79653b34)

Mais informações sobre o Pipeline podem ser encontradas na pasta pipeline_class.

## Performance do Negócio e Conclusão

O faturamento da empresa All in One antes da clusterização é de: R$10.027.467,31

Supondo que após a aplicação do programa de fidelidade a empresa consiga, por meio de campanhas de marketing e descontos especiais, aumentar em 20% o faturamento gerado pelos Insiders.

Também considerando que a empresa consiga uma taxa de conversão para o programa Insiders de 20% para os clientes ‘Potentials’, 10% para os clientes At Risk e 5% para os clientes ‘Sleeping’, haverá um aumento de 51% na quantidade de clientes pertencentes ao Insiders.

Se concluirmos que os clientes convertidos seguirão o padrão de consumo dos Insiders, o faturamento total passará a ser de R$11.282.203,37. Isso representa um aumento de R$1.254.728,62 ou 12,51% a mais para a empresa All in One.

Mais detalhes sobre o cálculo podem ser encontrados no notebook ‘customer_fidelity_final_embedding’ na seção Business Performance.

Portanto, podemos concluir que a implementação de um programa de fidelidade a partir de algoritmos de clusterização podem trazer resultados consideráveis para o valor da empresa. Além disso ao implementar técnicas de engajamento com os clientes a empresa ganha conhecimento de técnicas de marketing e alocação de recursos de forma mais eficiente

## Referências

Autor: Edilson Santos, Cientista de Dados

Porfólio: https://edjr94.github.io/portfolio_projetos/

Linkedin: https://www.linkedin.com/in/edilsonsantosjr/

# Customer Loyalty Program - Clustering
![Captura de tela 2023-06-28 151640 (1)](https://github.com/EDJR94/customer_fidelity/assets/128603807/22d6cf06-90a9-4bf4-baa2-4aae7440395f)



 **All in One** is a fictional e-commerce company based in the United Kingdom. It offers a wide range of products across various categories, including home decor, party supplies, kitchen accessories, storage solutions, and more.

## Business Problem

After successfully selling a diverse array of products and amassing a substantial customer base, All in One recognizes the hidden value in its customer data. The company aims to harness the power of data science to gain **deeper insights** into its customer base and strategically apply these insights. One of its main objectives is to effectively **segment its customers**. This segmentation will enable All in One to understand its customer base at a more granular level, identify specific customer groups with distinct needs and preferences, and tailor its marketing efforts and product offerings accordingly.

Furthermore, by implementing a **loyalty program**, All in One seeks to foster stronger customer relationships and enhance customer retention. By carefully analyzing customer behaviors, purchasing patterns, and preferences, they can design a loyalty program that offers personalized incentives, rewards, and exclusive benefits to different customer segments. This personalized approach not only promotes customer loyalty but also fosters a sense of appreciation and belonging among customers, further strengthening their connection with the brand.

## Data

| Column Name | Description |
| --- | --- |
| InvoiceNo | Invoice number, a unique identifier for each transaction |
| StockCode | Product code, a unique identifier for each product |
| Description | Product description |
| Quantity | Quantity of products purchased in each transaction |
| InvoiceDate | Date and time of each transaction |
| UnitPrice | Unit price of each product |
| CustomerID | Customer ID, a unique identifier for each customer |
| Country | Customer's country |

## Solution Strategy

The strategy employed was the CRISP method, a scientific method based on cycles:

![crisp](https://github.com/EDJR94/customer_fidelity/assets/128603807/ed8ae3f7-11e3-4561-a662-69cdbceea6e9)

The project cycles were divided into the following phases:

- Problem Understanding
- Data Description
- Feature Engineering
- Embedding Space Study
- Definition of Cluster Numbers
- Machine Learning Algorithm Study
- Model Training
- Exploratory Data Analysis
- Cloud Deployment
- Business Performance

## Feature Engineering

Feature selection was inspired by the RFM model and commonly used business metrics for a business:

![RFM model](https://github.com/EDJR94/customer_fidelity/assets/128603807/d391a820-de8c-405d-bf05-fc17dbd28f76)
Based on the provided data, features of the RFM model were created: Recency, Frequency, and Monetary. In total, 14 features were created, which are available in the notebook in the notebooks folder.

## Embedding Space Study

Since our dataset has 15 columns, I aimed to reduce this dimensionality to 2 dimensions using techniques such as PCA, t-SNE, UMAP, and dimensionality reduction by tree using Random Forest. According to what I showed in the Jupyter notebook, the reduction that showed the most separation of data was based on the Random Forest tree:

![Untitled](https://github.com/EDJR94/customer_fidelity/assets/128603807/8fd1701d-76d4-4dd1-bf9c-2c67314d4d39)

## Definition of Cluster Numbers

To define the optimal number of clusters, I used 3 main clustering algorithms:

- KMeans
- GaussianMixtureModel (GMM)
- Hierarchical Clustering (HCluster)

I used the Silhouette Score metric and a 2-dimensional visualization of the division made by the tree space for all models.

The best result was obtained with HClustering:

![Untitled (1)](https://github.com/EDJR94/customer_fidelity/assets/128603807/316e2cb6-b84f-41e2-ad45-237069811bcf)

![Untitled (2)](https://github.com/EDJR94/customer_fidelity/assets/128603807/62f580f5-c985-4ea5-9b90-0fba1e18da46)

They had higher silhouette values, but I chose to use 5 clusters as it also has a good silhouette value and effectively divides the data, as shown above.

## Result

After training the HClustering with 5 clusters and calculating the metrics, we arrived at the following result:

| Clusters | Monetary | Frequency | Recency | Percent | Qty Products | No. Products Returned | Relationship Duration | No. Customers | AVG Order Value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Insiders | 6599.350958 | 0.086662 | 44.127336 | 15.033368 | 300.517523 | 50.135514 | 246.336449 | 856 | 1149.044275 |
| Potentials | 2119.202031 | 0.024631 | 101.500428 | 20.495258 | 152.898886 | 35.820908 | 122.052271 | 1167 | 927.101689 |
| At Risk | 1053.963650 | 0.029953 | 94.205109 | 24.060414 | 38.831387 | 11.224088 | 123.827007 | 1370 | 503.898063 |
| Sleeping | 280.102519 | 0.016227 | 149.095310 | 23.217422 | 22.301059 | 2.193646 | 32.131619 | 1322 | 233.020635 |
| Occasional | 93.049877 | 0.006202 | 187.118488 | 17.193537 | 9.247191 | 0.880490 | 0.391216 | 979 | 91.611593 |

We can observe that 'Insiders' are customers who purchase high-value products, a large quantity of products, with high frequency and low recency.

'Potentials' customers are potential candidates to become 'Insiders', as they purchase a considerable number of products but have a high recency, indicating it's been a while since their last purchase.

'At Risk' customers are those who make acceptable-frequency purchases but buy a low quantity of products. By increasing the quantity of products they purchase, they could potentially become 'Insiders'.

'Sleeping' customers have made few purchases, rarely return, and their relationship with the company lasted on average only 32 days. They should be encouraged to make more frequent purchases.

Finally, 'Occasionals' are new customers who recently made purchases and should be encouraged to stay engaged with the company.

Additionally, a dashboard was created in Metabase connected to the AWS cloud-based RDS database to update the data as new customers are added:

![Untitled (3)](https://github.com/EDJR94/customer_fidelity/assets/128603807/42afda78-bfde-4c17-a26a-b039f307adb7)

## Cloud Deployment

After completing the project on my local machine, I set up a database on Amazon AWS to feed the data as new customers are added. I also utilized an AWS S3 bucket to store both the original and new data, as well as my trained model saved through the Pipeline.

This way, I can access my model and data through AWS, and Metabase is updated as I feed my Postgres database after passing the data through the trained model.

The production model structure is as depicted in the figure below:

![Untitled (4)](https://github.com/EDJR94/customer_fidelity/assets/128603807/f46820d4-e309-4356-a193-090df03f8d71)

Here is the structure of my Pipeline:

![Untitled (5)](https://github.com/EDJR94/customer_fidelity/assets/128603807/71c32544-3c64-4d11-b5da-a7bd79653b34)

More information about the Pipeline can be found in the pipeline_class folder.

## Business Performance and Conclusion

The revenue of the All in One company before clustering is: $10,027,467.31

Assuming that after implementing the loyalty program, the company can increase the revenue generated by 'Insiders' by 20% through marketing campaigns and special discounts.

Also, assuming the company achieves a conversion rate for the Insiders program of 20% for 'Potentials', 10% for 'At Risk', and 5% for 'Sleeping' customers, there will be a 51% increase in the number of 'Insiders'.

If we assume that the converted customers follow the consumption pattern of 'Insiders', the total revenue will become $11,282,203.37. This represents an increase of $1,254,728.62 or 12.51% more for the All in One company.

More details about the calculation can be found in the 'customer_fidelity_final_embedding' notebook in the Business Performance section.

Therefore, we can conclude that implementing a loyalty program based on clustering algorithms can bring considerable results to the company's value. Furthermore, by implementing customer engagement techniques, the company gains insights into marketing strategies and more efficient resource allocation.

## References

Author: Edilson Santos, Data Scientist

Portfolio: [https://edjr94.github.io/portfolio_projetos/](https://edjr94.github.io/portfolio_projetos/)

LinkedIn: [https://www.linkedin.com/in/edilsonsantosjr/](https://www.linkedin.com/in/edilsonsantosjr/)


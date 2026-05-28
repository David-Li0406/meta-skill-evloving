# Openai-Api - Embeddings

**Pages:** 3

---

## 

**URL:** https://platform.openai.com/docs/api-reference/vector-stores-files

**Contents:**
- Vector store files
- Create vector store file
    - Path parameters
    - Request body
    - Returns
- List vector store files
    - Path parameters
    - Query parameters
    - Returns
- Retrieve vector store file

Vector store files represent files inside a vector store.

Related guide: File Search

Create a vector store file by attaching a File to a vector store.

The ID of the vector store for which to create a File.

A File ID that the vector store should use. Useful for tools like file_search that can access files.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters, booleans, or numbers.

The chunking strategy used to chunk the file(s). If not set, will use the auto strategy.

A vector store file object.

Returns a list of vector store files.

The ID of the vector store that the files belong to.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A cursor for use in pagination. before is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with obj_foo, your subsequent call can include before=obj_foo in order to fetch the previous page of the list.

Filter by file status. One of in_progress, completed, failed, cancelled.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

Sort order by the created_at timestamp of the objects. asc for ascending order and desc for descending order.

A list of vector store file objects.

Retrieves a vector store file.

The ID of the file being retrieved.

The ID of the vector store that the file belongs to.

The vector store file object.

Retrieve the parsed contents of a vector store file.

The ID of the file within the vector store.

The ID of the vector store.

The parsed contents of the specified vector store file.

Update attributes on a vector store file.

The ID of the file to update attributes.

The ID of the vector store the file belongs to.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters, booleans, or numbers.

The updated vector store file object.

Delete a vector store file. This will remove the file from the vector store but the file itself will not be deleted. To delete the file, use the delete file endpoint.

The ID of the file to delete.

The ID of the vector store that the file belongs to.

A list of files attached to a vector store.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters, booleans, or numbers.

The strategy used to chunk the file.

The Unix timestamp (in seconds) for when the vector store file was created.

The identifier, which can be referenced in API endpoints.

The last error associated with this vector store file. Will be null if there are no errors.

The object type, which is always vector_store.file.

The status of the vector store file, which can be either in_progress, completed, cancelled, or failed. The status completed indicates that the vector store file is ready for use.

The total vector store usage in bytes. Note that this may be different from the original file size.

The ID of the vector store that the File is attached to.

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
4
5
6
7
curl https://api.openai.com/v1/vector_stores/vs_abc123/files \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -H "OpenAI-Beta: assistants=v2" \
    -d '{
      "file_id": "file-abc123"
    }'
```

Example 2 (bash):
```bash
1
2
3
4
5
6
7
curl https://api.openai.com/v1/vector_stores/vs_abc123/files \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -H "OpenAI-Beta: assistants=v2" \
    -d '{
      "file_id": "file-abc123"
    }'
```

Example 3 (unknown):
```unknown
1
2
3
4
5
6
7
```

Example 4 (python):
```python
1
2
3
4
5
6
7
8
from openai import OpenAI
client = OpenAI()

vector_store_file = client.vector_stores.files.create(
  vector_store_id="vs_abc123",
  file_id="file-abc123"
)
print(vector_store_file)
```

---

## Vector embeddings

**URL:** https://platform.openai.com/docs/guides/embeddings

**Contents:**
- Vector embeddings
- What are embeddings?
- How to get embeddings
- Embedding models
- Use cases
  - Obtaining the embeddings
    - Regression using the embedding features
- FAQ
  - How can I tell how many tokens a string has before I embed it?
  - How can I retrieve K nearest embedding vectors quickly?

OpenAI’s text embeddings measure the relatedness of text strings. Embeddings are commonly used for:

An embedding is a vector (list) of floating point numbers. The distance between two vectors measures their relatedness. Small distances suggest high relatedness and large distances suggest low relatedness.

Visit our pricing page to learn about embeddings pricing. Requests are billed based on the number of tokens in the input.

To get an embedding, send your text string to the embeddings API endpoint along with the embedding model name (e.g., text-embedding-3-small):

The response contains the embedding vector (list of floating point numbers) along with some additional metadata. You can extract the embedding vector, save it in a vector database, and use for many different use cases.

By default, the length of the embedding vector is 1536 for text-embedding-3-small or 3072 for text-embedding-3-large. To reduce the embedding's dimensions without losing its concept-representing properties, pass in the dimensions parameter. Find more detail on embedding dimensions in the embedding use case section.

OpenAI offers two powerful third-generation embedding model (denoted by -3 in the model ID). Read the embedding v3 announcement blog post for more details.

Usage is priced per input token. Below is an example of pricing pages of text per US dollar (assuming ~800 tokens per page):

Here we show some representative use cases, using the Amazon fine-food reviews dataset.

The dataset contains a total of 568,454 food reviews left by Amazon users up to October 2012. We use a subset of the 1000 most recent reviews for illustration purposes. The reviews are in English and tend to be positive or negative. Each review has a ProductId, UserId, Score, review title (Summary) and review body (Text). For example:

Below, we combine the review summary and review text into a single combined text. The model encodes this combined text and output a single vector embedding.

To load the data from a saved file, you can run the following:

Using larger embeddings, for example storing them in a vector store for retrieval, generally costs more and consumes more compute, memory and storage than using smaller embeddings.

Both of our new embedding models were trained with a technique that allows developers to trade-off performance and cost of using embeddings. Specifically, developers can shorten embeddings (i.e. remove some numbers from the end of the sequence) without the embedding losing its concept-representing properties by passing in the dimensions API parameter. For example, on the MTEB benchmark, a text-embedding-3-large embedding can be shortened to a size of 256 while still outperforming an unshortened text-embedding-ada-002 embedding with a size of 1536. You can read more about how changing the dimensions impacts performance in our embeddings v3 launch blog post.

In general, using the dimensions parameter when creating the embedding is the suggested approach. In certain cases, you may need to change the embedding dimension after you generate it. When you change the dimension manually, you need to be sure to normalize the dimensions of the embedding as is shown below.

Dynamically changing the dimensions enables very flexible usage. For example, when using a vector data store that only supports embeddings up to 1024 dimensions long, developers can now still use our best embedding model text-embedding-3-large and specify a value of 1024 for the dimensions API parameter, which will shorten the embedding down from 3072 dimensions, trading off some accuracy in exchange for the smaller vector size.

Question_answering_using_embeddings.ipynb

There are many common cases where the model is not trained on data which contains key facts and information you want to make accessible when generating responses to a user query. One way of solving this, as shown below, is to put additional information into the context window of the model. This is effective in many use cases but leads to higher token costs. In this notebook, we explore the tradeoff between this approach and embeddings bases search.

Semantic_text_search_using_embeddings.ipynb

To retrieve the most relevant documents we use the cosine similarity between the embedding vectors of the query and each document, and return the highest scored documents.

Code search works similarly to embedding-based text search. We provide a method to extract Python functions from all the Python files in a given repository. Each function is then indexed by the text-embedding-3-small model.

To perform a code search, we embed the query in natural language using the same model. Then we calculate cosine similarity between the resulting query embedding and each of the function embeddings. The highest cosine similarity results are most relevant.

Recommendation_using_embeddings.ipynb

Because shorter distances between embedding vectors represent greater similarity, embeddings can be useful for recommendation.

Below, we illustrate a basic recommender. It takes in a list of strings and one 'source' string, computes their embeddings, and then returns a ranking of the strings, ranked from most similar to least similar. As a concrete example, the linked notebook below applies a version of this function to the AG news dataset (sampled down to 2,000 news article descriptions) to return the top 5 most similar articles to any given source article.

Visualizing_embeddings_in_2D.ipynb

The size of the embeddings varies with the complexity of the underlying model. In order to visualize this high dimensional data we use the t-SNE algorithm to transform the data into two dimensions.

We color the individual reviews based on the star rating which the reviewer has given:

The visualization seems to have produced roughly 3 clusters, one of which has mostly negative reviews.

Regression_using_embeddings.ipynb

An embedding can be used as a general free-text feature encoder within a machine learning model. Incorporating embeddings will improve the performance of any machine learning model, if some of the relevant inputs are free text. An embedding can also be used as a categorical feature encoder within a ML model. This adds most value if the names of categorical variables are meaningful and numerous, such as job titles. Similarity embeddings generally perform better than search embeddings for this task.

We observed that generally the embedding representation is very rich and information dense. For example, reducing the dimensionality of the inputs using SVD or PCA, even by 10%, generally results in worse downstream performance on specific tasks.

This code splits the data into a training set and a testing set, which will be used by the following two use cases, namely regression and classification.

Embeddings present an elegant way of predicting a numerical value. In this example we predict the reviewer’s star rating, based on the text of their review. Because the semantic information contained within embeddings is high, the prediction is decent even with very few reviews.

We assume the score is a continuous variable between 1 and 5, and allow the algorithm to predict any floating point value. The ML algorithm minimizes the distance of the predicted value to the true score, and achieves a mean absolute error of 0.39, which means that on average the prediction is off by less than half a star.

Classification_using_embeddings.ipynb

This time, instead of having the algorithm predict a value anywhere between 1 and 5, we will attempt to classify the exact number of stars for a review into 5 buckets, ranging from 1 to 5 stars.

After the training, the model learns to predict 1 and 5-star reviews much better than the more nuanced reviews (2-4 stars), likely due to more extreme sentiment expression.

Zero-shot_classification_with_embeddings.ipynb

We can use embeddings for zero shot classification without any labeled training data. For each class, we embed the class name or a short description of the class. To classify some new text in a zero-shot manner, we compare its embedding to all class embeddings and predict the class with the highest similarity.

User_and_product_embeddings.ipynb

We can obtain a user embedding by averaging over all of their reviews. Similarly, we can obtain a product embedding by averaging over all the reviews about that product. In order to showcase the usefulness of this approach we use a subset of 50k reviews to cover more reviews per user and per product.

We evaluate the usefulness of these embeddings on a separate test set, where we plot similarity of the user and product embedding as a function of the rating. Interestingly, based on this approach, even before the user receives the product we can predict better than random whether they would like the product.

Clustering is one way of making sense of a large volume of textual data. Embeddings are useful for this task, as they provide semantically meaningful vector representations of each text. Thus, in an unsupervised way, clustering will uncover hidden groupings in our dataset.

In this example, we discover four distinct clusters: one focusing on dog food, one on negative reviews, and two on positive reviews.

In Python, you can split a string into tokens with OpenAI's tokenizer tiktoken.

For third-generation embedding models like text-embedding-3-small, use the cl100k_base encoding.

More details and example code are in the OpenAI Cookbook guide how to count tokens with tiktoken.

For searching over many vectors quickly, we recommend using a vector database. You can find examples of working with vector databases and the OpenAI API in our Cookbook on GitHub.

We recommend cosine similarity. The choice of distance function typically doesn't matter much.

OpenAI embeddings are normalized to length 1, which means that:

Yes, customers own their input and output from our models, including in the case of embeddings. You are responsible for ensuring that the content you input to our API does not violate any applicable law or our Terms of Use.

No, the text-embedding-3-large and text-embedding-3-small models lack knowledge of events that occurred after September 2021. This is generally not as much of a limitation as it would be for text generation models but in certain edge cases it can reduce performance.

**Examples:**

Example 1 (python):
```python
1
2
3
4
5
6
7
8
9
10
import OpenAI from "openai";
const openai = new OpenAI();

const embedding = await openai.embeddings.create({
  model: "text-embedding-3-small",
  input: "Your text string goes here",
  encoding_format: "float",
});

console.log(embedding);
```

Example 2 (javascript):
```javascript
1
2
3
4
5
6
7
8
9
10
import OpenAI from "openai";
const openai = new OpenAI();

const embedding = await openai.embeddings.create({
  model: "text-embedding-3-small",
  input: "Your text string goes here",
  encoding_format: "float",
});

console.log(embedding);
```

Example 3 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
10
```

Example 4 (python):
```python
1
2
3
4
5
6
7
8
9
from openai import OpenAI
client = OpenAI()

response = client.embeddings.create(
    input="Your text string goes here",
    model="text-embedding-3-small"
)

print(response.data[0].embedding)
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/vector-stores

**Contents:**
- Vector stores
- Create vector store
    - Request body
    - Returns
- List vector stores
    - Query parameters
    - Returns
- Retrieve vector store
    - Path parameters
    - Returns

Vector stores power semantic search for the Retrieval API and the file_search tool in the Responses and Assistants APIs.

Related guide: File Search

Create a vector store.

The chunking strategy used to chunk the file(s). If not set, will use the auto strategy. Only applicable if file_ids is non-empty.

A description for the vector store. Can be used to describe the vector store's purpose.

The expiration policy for a vector store.

A list of File IDs that the vector store should use. Useful for tools like file_search that can access files.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The name of the vector store.

A vector store object.

Returns a list of vector stores.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A cursor for use in pagination. before is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with obj_foo, your subsequent call can include before=obj_foo in order to fetch the previous page of the list.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

Sort order by the created_at timestamp of the objects. asc for ascending order and desc for descending order.

A list of vector store objects.

Retrieves a vector store.

The ID of the vector store to retrieve.

The vector store object matching the specified ID.

Modifies a vector store.

The ID of the vector store to modify.

The expiration policy for a vector store.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The name of the vector store.

The modified vector store object.

Delete a vector store.

The ID of the vector store to delete.

Search a vector store for relevant chunks based on a query and file attributes filter.

The ID of the vector store to search.

A query string for a search

A filter to apply based on file attributes.

The maximum number of results to return. This number should be between 1 and 50 inclusive.

Ranking options for search.

Whether to rewrite the natural language query for vector search.

A page of search results from the vector store.

A vector store is a collection of processed files can be used by the file_search tool.

The Unix timestamp (in seconds) for when the vector store was created.

The expiration policy for a vector store.

The Unix timestamp (in seconds) for when the vector store will expire.

The identifier, which can be referenced in API endpoints.

The Unix timestamp (in seconds) for when the vector store was last active.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The name of the vector store.

The object type, which is always vector_store.

The status of the vector store, which can be either expired, in_progress, or completed. A status of completed indicates that the vector store is ready for use.

The total number of bytes used by the files in the vector store.

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
4
5
6
7
curl https://api.openai.com/v1/vector_stores \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -H "OpenAI-Beta: assistants=v2" \
  -d '{
    "name": "Support FAQ"
  }'
```

Example 2 (bash):
```bash
1
2
3
4
5
6
7
curl https://api.openai.com/v1/vector_stores \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -H "OpenAI-Beta: assistants=v2" \
  -d '{
    "name": "Support FAQ"
  }'
```

Example 3 (unknown):
```unknown
1
2
3
4
5
6
7
```

Example 4 (python):
```python
1
2
3
4
5
6
7
from openai import OpenAI
client = OpenAI()

vector_store = client.vector_stores.create(
  name="Support FAQ"
)
print(vector_store)
```

---

# WANDS - Wayfair ANnotation Dataset

Note: this is a "fork" of the original dataset with the data transformed from
csv to duckdb for convenience.

## About The Project

WANDS is a Wayfair product search relevance dataset that is published as a
companion to the paper from ECIR 2022:

> WANDS: Dataset for Product Search Relevance Assessment\
> Yan Chen, Shujian Liu, Zheng Liu, Weiyi Sun, Linas Baltrunas and Benjamin
> Schroeder

The dataset allows objective benchmarking and evaluation of search engines on an
E-Commerce dataset. Key features of this dataset includes:

1. 42,994 candidate products
2. 480 queries
3. 233,448 (query,product) relevance judgements

Please refer to the paper for more details.

## Dataset Details

The data is stored in `wands.db`. The database consists of three tables:

The `product` table:

```sql
create table product(
    id int64 primary key -- ID of product,
    name varchar not null -- product's name,
    description varchar -- description of product,
    category varchar -- category which product falls under,
    category_hierarchy varchar[] -- parent categories of the product,
    features json not null -- attributes describing the product,
    rating_count double -- number of user ratings for the product,
    average_rating double -- average rating the product received,
    review_count double -- number of user reviews for the product,
);
```

The `query` table:

```sql
create table query(
    id int64 primary key, -- unique ID for each query
    query varchar not null, -- query string
    class varchar -- category to which this query falls under
);
```

The `label` table:

```sql
create type label_t as enum('Irrelevant', 'Partial', 'Exact');

create table label(
    id int64 primary key, -- unique ID for each annotation
    query_id int64 not null references query(id), -- query ID for annotation
    product_id int64 not null references product(id), -- product ID for annotation
    label label_t not null -- relevance label
);
```

## License

Distributed under the `MIT` License. See `LICENSE` for more information.

## Citation

Please cite this paper if you are building on top of or using this dataset:

```text
@InProceedings{wands,  
  title = {WANDS: Dataset for Product Search Relevance Assessment},  
  author = {Chen, Yan and Liu, Shujian and Liu, Zheng and Sun, Weiyi and Baltrunas, Linas and Schroeder, Benjamin},  
  booktitle = {Proceedings of the 44th European Conference on Information Retrieval},  
  year = {2022},  
  numpages = {12}  
}
```

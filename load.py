import json

import duckdb
import duckdb.typing as t


def read_product_csv(conn):
    def product_features_to_json(delimited_str):
        pairs = delimited_str.split("|")
        data = {}
        for pair in pairs:
            try:
                key, val = pair.split(":", 1)
                key = key.strip()
                val = val.strip()
            except ValueError:
                data[pair.strip()] = None
                continue
            try:
                val = float(val)
            except ValueError:
                pass
            data[key] = val
        return json.dumps(data, indent=None, separators=(",", ":"))

    conn.create_function(
        "features_to_json", product_features_to_json, [t.VARCHAR], t.VARCHAR
    )
    conn.sql(
        """
        create temporary view product_raw as
        select
            product_id as id,
            product_name as name,
            product_class as category,
            "category hierarchy" as category_hierarchy ,
            product_description as description,
            product_features as features,
            rating_count,
            average_rating,
            review_count
        from read_csv('dataset/product.csv')
             """
    )

    conn.sql(
        """
        create table product(
            id int64 primary key,
            name varchar not null,
            description varchar,
            category varchar,
            category_hierarchy varchar[],
            features json not null,
            rating_count double,
            average_rating double,
            review_count double,
        );
             """
    )

    conn.sql(
        """
        insert into product by name
        (select *
            replace(
                features_to_json(features) as features,
                list_transform(
                    string_split(category_hierarchy, '/'),
                    s -> trim(s)
                )
                as category_hierarchy
            ),
        from product_raw)
             """
    )


def read_query_csv(conn):
    conn.sql(
        """
        create table query(
            id int64 primary key,
            query varchar not null,
            class varchar
        );
             """
    )

    conn.sql(
        """
        insert into query by name
        select query_id as id, query, query_class as class
        from read_csv('dataset/query.csv')
        """
    )


def read_label_csv(conn):
    conn.sql(
        """
        create type label_t as enum('Irrelevant', 'Partial', 'Exact');
        create table label(
            id int64 primary key,
            query_id int64 not null references query(id),
            product_id int64 not null references product(id),
            label label_t not null
        );
             """
    )

    conn.sql(
        "insert into label by name (select * from read_csv('dataset/label.csv'))"
    )


def main():
    db_path = "wands.db"
    with duckdb.connect(db_path) as conn:
        read_product_csv(conn)
        read_query_csv(conn)
        read_label_csv(conn)


if __name__ == "__main__":
    main()

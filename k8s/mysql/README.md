# How to add a new secret?

```base
kubectl create secret generic mysql-secret -n database --from-literal=<KEY>=<VALUE> --dry-run=client -o yaml > k8s/mysql/overlays/database/secret.yaml
```

```bash
kubeseal -o yaml < k8s/mysql/overlays/database/secret.yaml > k8s/mysql/overlays/database/sealed-secret.yaml
```

# Schema management with SchemaHero

After you deploy MySQL container and schemahero.

```bash
❯ kubectl schemahero get migrations -n database
ID       DATABASE  TABLE  PLANNED  EXECUTED  APPROVED  REJECTED
7cbbee2  test      notes  55s
```

Check the migration

```bash
❯ kubectl schemahero describe migration -n database 7cbbee2

Migration Name: 7cbbee2

Generated DDL Statement (generated at 2021-05-12T00:00:56+09:00):
  create table `notes` (`id` int (11) not null, `title` varchar (50), `description` varchar (100), `created_at` date, primary key (`id`))

To apply this migration:
  kubectl schemahero -n database approve migration 7cbbee2

To recalculate this migration against the current schema:
  kubectl schemahero -n database recalculate migration 7cbbee2

To deny and cancel this migration:
  kubectl schemahero -n database reject migration 7cbbee2
```

Approve the migration

```bash
❯ kubectl schemahero -n database approve migration 7cbbee2
Migration 7cbbee2 approved
```

Result

```bash
❯ kubectl schemahero get migrations -n database
ID       DATABASE  TABLE  PLANNED  EXECUTED  APPROVED  REJECTED
7cbbee2  test      notes  2m57s    18s       18s

❯ kubectl exec -it mysql-0 -n database -- mysql -uroot -p$(kubectl get secret -n database  mysql-secret -o yaml | grep MYSQL_ROOT_PASSWORD | sed 's/.*.: \(.*\)/\1/' | base64 --decode) test
mysql: [Warning] Using a password on the command line interface can be insecure.
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 55
Server version: 5.7.34 MySQL Community Server (GPL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| notes          |
+----------------+
1 row in set (0.00 sec)

mysql> describe notes;
+-------------+--------------+------+-----+---------+-------+
| Field       | Type         | Null | Key | Default | Extra |
+-------------+--------------+------+-----+---------+-------+
| id          | int(11)      | NO   | PRI | NULL    |       |
| title       | varchar(50)  | YES  |     | NULL    |       |
| description | varchar(100) | YES  |     | NULL    |       |
| created_at  | date         | YES  |     | NULL    |       |
+-------------+--------------+------+-----+---------+-------+
4 rows in set (0.00 sec)

mysql> exit
Bye
```

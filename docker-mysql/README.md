# MySQL

## Build the image and run container
```
$ cd docker-mysql
$ docker build -t mysql . 
$ docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=1234 mysql 
```

## Create db table from running container
```
$ docker exec -i -t mysql bash // 컨테이너 bash 실행

# mysql -uroot -p
# 1234
# create database test_db;
# use test_db;
# CREATE TABLE `test_db`.`test_table` (
            `key` VARCHAR(32) NOT NULL COMMENT '',
                `value` VARCHAR(64) NOT NULL COMMENT '',
                    PRIMARY KEY (`key`)  COMMENT '');
# INSERT INTO `test_table` (`key`, `value`) VALUES ('asdf', '123sadf');
```



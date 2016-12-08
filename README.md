# Naver Open Source Project
Hanyang University Team 5

## Architecture

This is the architecture of Web Application Server (WAS).

![arch](/doc/images/architecture.png)

성능 비교를 위한 Web Application Server 의 구조이다. 
WAS는 MySQL, Arcus nBase-ARC 에 대하여 웹 브라우저를 통해 쿼리를 보내며, 
NGrinder 를 통해 테스트 쿼리 셋을 날려서 성능을 비교한다.
세 가지의 DB 에는 Hubblemon 에 연결되어 각 DB의 상태를 모니터링 하도록 한다.

## Usage
```
$ cd arcus-python-client
$ python3 db_test.py
```
WAS 프로그램 실행 후 Web Browser 를 통해 다음의 쿼리를 수행할 수 있다.
```
(web) http://localhost:8000/mysql_insert?key=1&value=a
(web) http://localhost:8000/mysql_select?key=1
(web) http://localhost:8000/arcus_set?key=1&value=a
(web) http://localhost:8000/arcus_get?key=1
(web) http://localhost:8000/nbase_arc_set?key=1&value=a
(web) http://localhost:8000/nbase_arc_get?key=1
```

###Contributor
Yongeun Jung, Hyeongwon Jang, Junwoo Park, Gunju Ko



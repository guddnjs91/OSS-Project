# Arcus

## Build the image and run container
```
$ cd docker-arcus
$ docker build --rm -t arcus-admin ./arcus
$ docker build --rm -t arcus-memcached ./arcus-memcached

$ docker run -d --name="arcus-admin" -h "arcus" arcus-admin
$ docker run -d --name="arcus-memcached-1" -h "memcached-1" arcus-memcached
$ docker run -d --name="arcus-memcached-2" -h "memcached-2" arcus-memcached
$ docker run -d --name="arcus-memcached-3" -h "memcached-3" arcus-memcached
```

## Arcus cloud build

### Enter the running arcus-admin container

memcached-X 컨테이너의 ip 주소(여기서는 172.17.0.20-22이라고 가정) 를 알아야 한다.

```
$ docker exec -i -t arcus-admin bash //컨테이너 bash 실행
```

### Modify /opt/arcus/scripts/arcus.sh 
```
zklist=“172.17.0.20:2181,172.17.0.21:2181,172.17.0.22:2181”
```

### Modify /opt/arcus/scripts/conf/guddnjs91.json
```
{
    "serviceCode": "guddnjs91-cloud"
        , "servers": [
        { "hostname": "memcached-1", "ip": "172.17.0.20",
            "config": {
                "port"   : "11211"
            }
        }
    , { "hostname": "memcached-1", "ip": "172.17.0.20",
        "config": {
            "port"   : "11212"
        }
    }
    , { "hostname": "memcached-2", "ip": "172.17.0.21",
        "config": {
            "port"   : "11211"
        }
    }
    , { "hostname": "memcached-2", "ip": "172.17.0.21",
        "config": {
            "port"   : "11212"
        }
    }
    , { "hostname": "memcached-3", "ip": "172.17.0.22",
        "config": {
            "port"   : "11211"
        }
    }
    , { "hostname": "memcached-3", "ip": "172.17.0.22",
        "config": {
            "port"   : "11212"
        }
    }
    ]
        , "config": {
            "threads"    : "6"
                , "memlimit"   : "100"
                , "connections": "1000"
        }
}
```

### Build guddnjs91-cloud
```
# cd /opt/arcus/scripts
# ./arcus.sh deploy conf/guddnjs91.json
# ./arcus.sh zookeeper init
# ./arcus.sh zookeeper start
# ./arcus.sh memcached register conf/guddnjs91.json
# ./arcus.sh memcached start guddnjs91-cloud
# ./arcus.sh memcached list guddnjs91-cloud  // 상태 확인
```



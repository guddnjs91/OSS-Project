FROM     ubuntu:14.04

MAINTAINER Hyeongwon Jang <guddnjs91@gmail.com>

# Requirements
RUN apt-get update && apt-get install -y supervisor openssh-server aptitude net-tools iputils-ping nano curl \
 vim git netcat build-essential make gcc g++ autoconf automake libtool libextutils-pkgconfig-perl libcppunit-dev python2.7-dev python-setuptools subversion

# Install Directiry
ENV SRC_DIR /opt

# Install JDK
ENV JDK_URL http://download.oracle.com/otn-pub/java/jdk
ENV JDK_VER 8u65-b17
ENV JDK_VER2 jdk-8u65
ENV JAVA_HOME /usr/local/jdk
ENV PATH $PATH:$JAVA_HOME/bin
RUN cd $SRC_DIR && curl -LO "$JDK_URL/$JDK_VER/$JDK_VER2-linux-x64.tar.gz" -H 'Cookie: oraclelicense=accept-securebackup-cookie' \
 && tar xzf $JDK_VER2-linux-x64.tar.gz && mv jdk1* $JAVA_HOME && rm -f $JDK_VER2-linux-x64.tar.gz \
 && echo '' >> /etc/profile \
 && echo '# JDK' >> /etc/profile \
 && echo "export JAVA_HOME=$JAVA_HOME" >> /etc/profile \
 && echo 'export PATH="$PATH:$JAVA_HOME/bin"' >> /etc/profile \
 && echo '' >> /etc/profile

# Install ANT (1.9.7)
ENV ANT_VER 1.9.7
ENV ANT_HOME $SRC_DIR/apache-ant-$ANT_VER
ENV PATH $PATH:$ANT_HOME/bin
RUN cd $SRC_DIR && curl -LO "http://www.us.apache.org/dist/ant/binaries/apache-ant-$ANT_VER-bin.tar.bz2" \
 && tar xjf apache-ant-$ANT_VER-bin.tar.bz2 && rm -f apache-ant-$ANT_VER-bin.tar.bz2 \
 && echo '# Ant' >> /etc/profile \
 && echo "export ANT_HOME=$ANT_HOME" >> /etc/profile \
 && echo 'export PATH=$PATH:$ANT_HOME/bin' >> /etc/profile \
 && echo '' >> /etc/profile

# Arcus Build
RUN cd $SRC_DIR && git clone https://github.com/naver/arcus.git \
 && cd arcus/scripts && sed -i "s/memcached -E/memcached -u memcached -E/g" fabfile.py && ./build.sh
ADD conf/guddnjs91.json $SRC_DIR/arcus/scripts/conf/guddnjs91.json

# Generating SSH Public Key (authorized to memcached node)
RUN ssh-keygen -t dsa -P '' -f "/root/.ssh/id_dsa"
RUN cat /root/.ssh/id_dsa.pub >> /root/.ssh/authorized_keys
RUN chmod 644 /root/.ssh/authorized_keys

# Supervisor (for sshd)
RUN mkdir -p /var/log/supervisor
ADD conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# SSH Setting
RUN mkdir /var/run/sshd
RUN sed -i 's/without-password/yes/g' /etc/ssh/sshd_config
RUN sed -i 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config

# Root Password
RUN echo 'root:arcus' |chpasswd

# Port
EXPOSE 22

# Start command of starting container
CMD ["/usr/bin/supervisord"]

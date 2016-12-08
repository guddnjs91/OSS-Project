FROM     ubuntu:14.04

MAINTAINER Hyeongwon Jang <guddnjs91@gmail.com>

# Requirements
RUN apt-get update && apt-get install -y curl openssh-server supervisor vim

# Install Directory
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

# Generate Arcus Memcached Users
RUN useradd -M -s /sbin/nologin memcached \
 && mkdir -p /var/run/memcached && chown memcached:memcached /var/run/memcached

# Supervisor (for sshd) 
RUN mkdir -p /var/log/supervisor
ADD conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# SSH Setting
RUN mkdir /root/.ssh && mkdir /var/run/sshd
RUN sed -i 's/without-password/yes/g' /etc/ssh/sshd_config
RUN sed -i 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config

# Root Password
RUN echo 'root:memcached' |chpasswd

# Port 
EXPOSE 22 2181 11211 11212

# Start command of starting container
CMD ["/usr/bin/supervisord"]

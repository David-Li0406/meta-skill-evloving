FROM eclipse-temurin:17-jdk
ARG GIT_USERNAME=
ARG GIT_PASSWORD=

RUN apt-get update \
    && apt-get install -y git screen \
    && rm -rf /var/lib/apt/lists/*


RUN echo "machine github.com" > /root/.netrc
RUN echo "login $GIT_USERNAME" >> /root/.netrc
RUN echo "password $GIT_PASSWORD" >> /root/.netrc

WORKDIR /

RUN git clone --depth 1 -b "main" https://github.com/hotwax/moqui-framework.git

WORKDIR /moqui-framework
RUN git clone --depth 1 -b "main" https://github.com/hotwax/moqui-runtime.git runtime

WORKDIR /moqui-framework/runtime/component
RUN git clone --depth 1 -b "build-gradle-file" https://github.com/dixitdeepak/moqui-atomikos.git
RUN git clone --depth 1 -b "main" https://github.com/hotwax/darpan.git

RUN rm -rf /root/.netrc

WORKDIR /moqui-framework

#Copy production configuration file.
RUN cp -rf runtime/component/darpan/docker/MoquiProductionConf.xml runtime/conf/
RUN git apply runtime/component/darpan/docker/buildGradle.patch

#Create war file.
RUN ./gradlew addRuntime

#Extract war file.
WORKDIR /moqui-deploy
RUN cp /moqui-framework/runtime/component/darpan/docker/entrypoint.sh /moqui-deploy/

RUN chmod +x entrypoint.sh
RUN jar -xvf /moqui-framework/moqui-plus-runtime.war

ENV DB_LOAD="./gradlew loadProduction -Ptypes=seed,seed-initial,install,ext-seed,ext -Praw"
ENV JAVA_OPTS="-Xms512m -Xmx4096m"
ENV CONF_FILE="/moqui-framework/runtime/conf/MoquiProductionConf.xml"
ENV SLEEP="sleep 2"
ENV JWT_KEY=
ENV MOQUI_HOST=
ENV Moqui_DB_HOST=
ENV Moqui_DB_USER=
ENV Moqui_DB_PASSWORD=
ENV Moqui_DB_NAME=
ENV ELASTICSEARCH_HOST=
ENV TIME_ZONE=

EXPOSE 8080

ENTRYPOINT ./entrypoint.sh && bash

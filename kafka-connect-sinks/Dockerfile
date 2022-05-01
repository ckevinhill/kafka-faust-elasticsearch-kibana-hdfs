FROM cnfldemos/cp-server-connect-datagen:0.5.3-7.1.0

ENV CONNECT_PLUGIN_PATH = "/usr/share/java,/usr/share/confluent-hub-components"

RUN confluent-hub install --no-prompt confluentinc/kafka-connect-hdfs3:1.1.10 \
    && confluent-hub install --no-prompt confluentinc/kafka-connect-elasticsearch:11.1.10

CMD /etc/confluent/docker/run
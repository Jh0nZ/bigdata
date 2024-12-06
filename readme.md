```bash
start-dfs.sh
```

```bash
start-yarn.sh
```

```bash
hadoop fs -mkdir -p /datos
```

```bash
hdfs dfs -put -f /a/archivo /datos/
```

```bash
hdfs dfs -ls /
```

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-input /datos/noticias.csv \
-output /user/jhon/resultado \
-mapper "python3 mapper.py" \
-reducer "python3 reducer.py" \
-file mapper.py \
-file reducer.py
```

```bash
hadoop fs -cat /user/jhon/resultado/part-00000
```
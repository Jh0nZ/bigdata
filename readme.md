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

```bash
hadoop fs -rm -r /user/jhon/resultado
```

# conteo de palabras
```bash
hadoop fs -rm -r /user/jhon/resultado_palabras
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-input /datos/pg74840.txt \
-output /user/jhon/resultado_palabras \
-mapper "python3 mapper.py" \
-reducer "python3 reducer.py" \
-file palabras/mapper.py \
-file palabras/reducer.py
```

```bash
hdfs dfs -put -f palabras/mapper.py palabras/reducer.py /user/jhon/scripts/
```

```bash
hadoop fs -cat /user/jhon/resultado_palabras/part-00000
```

# tarifas
```bash
hadoop fs -rm -r /user/jhon/resultado_tarifas
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-input /datos/tarifas.csv \
-output /user/jhon/resultado_tarifas \
-mapper "python3 mapper.py" \
-reducer "python3 reducer.py" \
-file tarifas/mapper.py \
-file tarifas/reducer.py
```

```bash
hdfs dfs -put -f tarifas/mapper.py tarifas/reducer.py /user/jhon/scripts/
```

```bash
hadoop fs -cat /user/jhon/resultado_tarifas/part-00000
```
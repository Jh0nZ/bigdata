-- comandos para cargar en pig
transacciones = LOAD 'hdfs:///datos/transacciones.csv' 
USING PigStorage(',') 
AS (id_transaccion:int, 
    producto:chararray, 
    categoria:chararray, 
    cantidad:int, 
    precio_unitario:chararray, 
    Subtotal:chararray, 
    fecha:chararray);

DUMP transacciones;

transacciones_converted = FOREACH transacciones GENERATE 
    id_transaccion, 
    producto, 
    categoria, 
    cantidad, 
    (double)REPLACE(REPLACE(precio_unitario, '.', ''), ',', '.') AS precio_unitario, 
    (double)REPLACE(REPLACE(Subtotal, '.', ''), ',', '.') AS Subtotal, 
    fecha;

DUMP transacciones_converted;

STORE data_converted INTO 'transacciones_procesadas' USING org.apache.hive.hcatalog.pig.HCatStorer();



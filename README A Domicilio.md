BAR LA CONSULTA

# La Consulta en Data

- Un análisis operativo y de negocio sobre el servicio de reparto a domicilio del bar La Consulta, pensado para detectar qué factores afectan a la facturación, al ritmo de pedidos y a la satisfacción de los clientes.
- ¿Qué plataforma genera más ingresos? ¿Influye la lluvia en el volumen diario de pedidos? ¿Cómo afecta el tiempo de espera a la valoración del cliente? ¿Crece la demanda con el paso de las semanas?
- Le puede interesar directamente a la gerencia y al equipo operativo de La Consulta para optimizar turnos en días de lluvia, controlar tiempos de entrega y tomar decisiones sobre canales de venta y ticket medio.


## · LOS DATOS

- De dónde salen: De la base de datos MySQL alojada en TiDB Cloud (en la nube), con un dialecto SQL muy similar al de SQLite, conectada mediante usuario y contraseña (sin exponer credenciales reales en el repositorio).
- Cuántos son: 1376 filas y 13 columnas ("pedidos_limpios.csv")
- Qué es cada fila: Cada fila representa un pedido realizado a La Consulta, con información sobre la fecha, la plataforma de pedido, el barrio de entrega, el importe total (€), los minutos de espera, la valoración del cliente y la lluvia registrada en milímetros.
- **Qué he limpiado y por qué:**


    1º Convierto la columna "total" cambiando las comas por puntos y pasándola a formato numérico con "pd.to_numeric()" y "str.replace()" para poder sumar los importes y calcular la facturación por "plataforma".
    2º Unifico "fecha_hora" pasando todo a formato "%Y-%m-%d %H:%M". Utilizo también ".fillna()" para poder unificar todo con el mismo formato.
    3º Paso el "estado" a minúsculas con ".str.lower()" ya que las filas que hay en la columna "estado" venían mezcladas.
    4º Quito los huecos de los lados y paso los barrios a minúsculas con "str.strip().str.lower()". Después con ".replace()" y ".str.capitalize()" pongo todos los nombres de los barrios iguales y ortográficamente bien.
    5º Compruebo si hay filas duplicadas, hago la prueba quitando los "id" y veo que hay 31 filas repetidas, por lo que las suprimo y paso de 1407 a 1376.
    6º Relleno los huecos en los que "propina" está vacío con "0".
    7º Observo que en "minutos" hay valores raros de entrega en 0 y 999 minutos por lo que con ".loc()" paso esos valores a "None".
    8º En las valoraciones de las plataformas, en las de "Telefono" las dejo como están a 0.
    9º Añado 2 columnas , una de "fecha" y otra de "hora" para poder seguir analizando más datos.
    10º Añado la columna de "dia_semana" con ".dt.day_of_week.map() para tener más datos a analizar.
    11º Añado la columna semana con ".dt.isocalendar().week" para poder ver el número de la semana de pedidos.
    12º Añado la columna "neto" para seguir comparando valores.
    13º Para saber qué dias llovió en los pedidos con ".merge()" junto 2 tablas por su columna en común.



## · CONCLUSIONES DEL EDA

1-Impacto del tiempo de espera en la satisfacción del cliente

    -Al cruzar los minutos de espera con la nota del cliente, se observa una relación negativa: conforme aumenta el tiempo de entrega, tiende a caer la puntuación recibida.

    -La conclusión: El tiempo de reparto es uno de los factores más críticos para la reputación del servicio. Reducir los picos de demora en franjas críticas protege directamente la valoración media en las plataformas de delivery.

2-El efecto de la lluvia en la demanda diaria

    -Al agrupar los pedidos por fecha y comparar la media diaria de pedidos en días sin lluvia frente a días con precipitaciones, el promedio diario de pedidos varía significativamente cuando llueve respecto a los días secos.

    -La conclusión: Medir la media diaria (y no solo el total acumulado) evita el sesgo de que llueva pocos días al año y confirma que la meteorología es un indicador clave para prever picos de demanda y reforzar cocina y reparto con antelación.

3- Concentración de ingresos por canal y evolución semanal

    -La facturación no se reparte de forma uniforme entre plataformas ni entre tramos de importe, concentrándose el grueso de pedidos en una franja concreta de ticket medio mientras la actividad evoluciona semana a semana.

    -La conclusión: Conocer qué canal aporta mayor volumen de facturación y cómo evolucionan las semanas permite enfocar promociones de ticket mínimo y ajustar la capacidad operativa según la tendencia real del negocio.

---

## La app

![alt text](app-1.png) 

La aplicación en Streamlit permite explorar los pedidos de Bar La Consulta aplicando filtros dinámicos en la barra lateral (Plataforma y Precio pedido) para consultar al instante las métricas principales (total de pedidos, facturación total, ticket medio y tiempo medio de espera). A través de tres pestañas (Pedidos filtrados, Canales y tiempos y ¿Qué pasaría si...?, donde se incluye un simulador rápido de ticket mínimo), el usuario puede revisar los pedidos filtrados, analizar canales y tiempos de entrega y simular cuántos pedidos y cuánta facturación se alcanzan a partir de un importe elegido.


https://adomicilio.streamlit.app/




## Cómo ejecutarlo

1. Crear un entorno e instalar las librerías: `pip install -r requirements.txt`
2. El EDA está en `eda.ipynb`.
3. La app se abre con `streamlit run app.py`.

## Autor
Jon Vaquerizo 

GitHub: jonvaque69-cmyk

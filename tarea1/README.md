# Tarea 1

## Requerimiento

Crear un par de (nano) servicios mediante FastAPI, que envíen sus logs mediante Promtail a un log aggregation system Loki y visualizar dichos logs mediante Grafana.
Todo debe estar desplegado mediante docker-compose.

## Estructura de proyecto

El repositorio esta organizado de la siguiente forma:

- `logs`: carpeta que almacena logs de contenedores, es un reflejo del archivo `*.log` de cada contenedor (NO CARGADA EN EL REPO, se crea al construir contenedores).
- `promtail`: tiene la configuración para leer los logs.
- `service_01`
- `service_02`
- `docker-compose`: para crear los contenedores y volumenes con un solo comando.

## Instrucciones

1. Clonar repositorio
```bash
git clone [link]
```

2. luego ejecutar comando de docker para construir contenedores
```bash
docker-compose build
docker-compose up -d
```

```bash
# este comando es todo junto
docker-compose up --build -d
```

3. Conectar Grafana con loki
    - Abrir Grafana en `localhost:3000` o directamente de docker desktop
    - Hacer login (credenciales default en docker-compose) 
    - Menu lateral > Data sources > buscar Loki > agregar `http://loki:3100`
    - Menu lateral > Explore > hacer request (no aparecen los servicios la primera vez, se debe hacer un curl para que los `*.log` tengan algo escrito)


> [!IMPORTANT] 
> Si no aparecen las asignaciones en Grafana para el `service_01` y `service_02`, puede ser porque los archivos `.log` no tienen nada escrito porque estan recien creados,
> se debe puede hacer `curl http://localhost:5001` y `curl http://localhost:5002` para comprobar el sistema y con eso ya se tienen los logs necesarios para que Grafana
> detecte los archivos.

4. Cargar datos en mongodb
```bash
# servicio 01
./service_01/seed.sh

# servicio 02
./service_02/seed.sh
./service_02/test.sh
```

5. Eliminar los contenedores
```bash
docker-compose down -v
```
---

## Notas de desarrollo personales

### Docker

#### docker-compose

- `link` como estaba en ejemplo del profe, ya no se usa. Se detectan automatico si estan en la misma red.
- `depends_on` se ocupa para dar un orden de ejecucion solamente, no es que se detenga a esperar  que uno termine para empezar. Para eso se ocupa `healthcheck`.
- Ocupar 1 solo docker-compose cuando ambos servicios tengan relacion entre si, en este caso para la tarea es posible porque deben comunicarse entre si y es mas comodo, levantar ambos a la vez.


#### Dockerfile

Cada micro servicio es mejor que tenga su propio Dockerfile, ya que son desarrollos distintos. Es mejor un Dockerfile para cada carpeta de desarrollo, en este caso son dos microservicios entonces 2 Dockerfiles.

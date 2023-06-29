Skip to content
DEV Community
Search...

Log in
Create account

4
Jump to Comments
21
Save

Marco Villarreal
Marco Villarreal
Posted on Jun 26, 2021


13

2

1
Creating a Spark Standalone Cluster with Docker and docker-compose(2021 update)
#
docker
#
spark
#
bigdata
Back in 2018 I wrote this article on how to create a spark cluster with docker and docker-compose, ever since then my humble repo got 270+ stars, a lot of forks and activity from the community, however I abandoned the project by some time(Was kinda busy with a new job on 2019 and some more stuff to take care of), I've merged some pull quest once in a while, but never put many attention on upgrading versions.

But today we are going to revisit this old fella with some updates and hopefully run some examples with scala and python(yeah 2018 version didn't support python, thanks to the community to bring pyspark to this baby).

Requirements
Docker (I am using version 20.10.7)
docker-compose (I am using version 1.21.2)
This repo ;)
Project Structure
The following project structure will be used
|
|--|apps # Apps directory for volume mounts(any app you want to deploy just paste it here)
|--|data # Data directory for volume mounts(any file you want to process just paste it here)
|--|Dockerfile #Dockerfile used to build spark image
|--|start-spark.sh # startup script used to run different spark workloads
|--|docker-compose.yml # the compose file

Creating The Image
In the 2018 version, we've used a base image and a separated image for each spark workload(one image for the master one for the worker and one for spark-submit). In this new approach we will use docker multi stage builds to create a unique image that can be launched as any workload we want.

Here's the dockerfile used to define our apache-spark image:

# builder step used to download and configure spark environment
FROM openjdk:11.0.11-jre-slim-buster as builder

# Add Dependencies for PySpark
RUN apt-get update && apt-get install -y curl vim wget software-properties-common ssh net-tools ca-certificates python3 python3-pip python3-numpy python3-matplotlib python3-scipy python3-pandas python3-simpy

RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1

# Fix the value of PYTHONHASHSEED
# Note: this is needed when you use Python 3.3 or greater
ENV SPARK_VERSION=3.0.2 \
HADOOP_VERSION=3.2 \
SPARK_HOME=/opt/spark \
PYTHONHASHSEED=1

# Download and uncompress spark from the apache archive
RUN wget --no-verbose -O apache-spark.tgz "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
&& mkdir -p /opt/spark \
&& tar -xf apache-spark.tgz -C /opt/spark --strip-components=1 \
&& rm apache-spark.tgz


# Apache spark environment
FROM builder as apache-spark

WORKDIR /opt/spark

ENV SPARK_MASTER_PORT=7077 \
SPARK_MASTER_WEBUI_PORT=8080 \
SPARK_LOG_DIR=/opt/spark/logs \
SPARK_MASTER_LOG=/opt/spark/logs/spark-master.out \
SPARK_WORKER_LOG=/opt/spark/logs/spark-worker.out \
SPARK_WORKER_WEBUI_PORT=8080 \
SPARK_WORKER_PORT=7000 \
SPARK_MASTER="spark://spark-master:7077" \
SPARK_WORKLOAD="master"

EXPOSE 8080 7077 6066

RUN mkdir -p $SPARK_LOG_DIR && \
touch $SPARK_MASTER_LOG && \
touch $SPARK_WORKER_LOG && \
ln -sf /dev/stdout $SPARK_MASTER_LOG && \
ln -sf /dev/stdout $SPARK_WORKER_LOG

COPY start-spark.sh /

CMD ["/bin/bash", "/start-spark.sh"]
Notice that in the dockerfile we reference a script called start-spark.sh, it's primary goal is to run spark-class script with the given role (master, or worker).
#start-spark.sh
#!/bin/bash
. "/opt/spark/bin/load-spark-env.sh"
# When the spark work_load is master run class org.apache.spark.deploy.master.Master
if [ "$SPARK_WORKLOAD" == "master" ];
then

export SPARK_MASTER_HOST=`hostname`

cd /opt/spark/bin && ./spark-class org.apache.spark.deploy.master.Master --ip $SPARK_MASTER_HOST --port $SPARK_MASTER_PORT --webui-port $SPARK_MASTER_WEBUI_PORT >> $SPARK_MASTER_LOG

elif [ "$SPARK_WORKLOAD" == "worker" ];
then
# When the spark work_load is worker run class org.apache.spark.deploy.master.Worker
cd /opt/spark/bin && ./spark-class org.apache.spark.deploy.worker.Worker --webui-port $SPARK_WORKER_WEBUI_PORT $SPARK_MASTER >> $SPARK_WORKER_LOG

elif [ "$SPARK_WORKLOAD" == "submit" ];
then
    echo "SPARK SUBMIT"
else
    echo "Undefined Workload Type $SPARK_WORKLOAD, must specify: master, worker, submit"
fi
To build the image just run:
docker build -t cluster-apache-spark:3.0.2 .
After some time the image will be successfully created, it will take some time depending on how fast the dependencies and the spark tarball are dowloaded (fortunatelly these steps get cached as a layer thanks to the multistage setup).

The compose File
Now that we have our apache-spark image is time to create a cluster in docker-compose
version: "3.3"
services:
  spark-master:
    image: cluster-apache-spark:3.0.2
    ports:
      - "9090:8080"
      - "7077:7077"
    volumes:
       - ./apps:/opt/spark-apps
       - ./data:/opt/spark-data
    environment:
      - SPARK_LOCAL_IP=spark-master
      - SPARK_WORKLOAD=master
  spark-worker-a:
    image: cluster-apache-spark:3.0.2
    ports:
      - "9091:8080"
      - "7000:7000"
    depends_on:
      - spark-master
    environment:
      - SPARK_MASTER=spark://spark-master:7077
      - SPARK_WORKER_CORES=1
      - SPARK_WORKER_MEMORY=1G
      - SPARK_DRIVER_MEMORY=1G
      - SPARK_EXECUTOR_MEMORY=1G
      - SPARK_WORKLOAD=worker
      - SPARK_LOCAL_IP=spark-worker-a
    volumes:
       - ./apps:/opt/spark-apps
       - ./data:/opt/spark-data
  spark-worker-b:
    image: cluster-apache-spark:3.0.2
    ports:
      - "9092:8080"
      - "7001:7000"
    depends_on:
      - spark-master
    environment:
      - SPARK_MASTER=spark://spark-master:7077
      - SPARK_WORKER_CORES=1
      - SPARK_WORKER_MEMORY=1G
      - SPARK_DRIVER_MEMORY=1G
      - SPARK_EXECUTOR_MEMORY=1G
      - SPARK_WORKLOAD=worker
      - SPARK_LOCAL_IP=spark-worker-b
    volumes:
        - ./apps:/opt/spark-apps
        - ./data:/opt/spark-data
  demo-database:
    image: postgres:11.7-alpine
    ports: 
      - "5432:5432"
    environment: 
      - POSTGRES_PASSWORD=casa1234
For both spark master and worker we configured the following environment variables:

Environment	Description
SPARK_MASTER	Spark master url
SPARK_WORKER_CORES	Number of cpu cores allocated for the worker
SPARK_WORKER_MEMORY	Amount of ram allocated for the worker
SPARK_DRIVER_MEMORY	Amount of ram allocated for the driver programs
SPARK_EXECUTOR_MEMORY	Amount of ram allocated for the executor programs
SPARK_WORKLOAD	The spark workload to run(can be any of master, worker, submit)
Compared to 2018 version the following changes were made:

Removed the custom network and ip addresses

Expose 2 workers instead of 3, and expose each worker port in the range of(9090...9091 and so on)

Pyspark support thanks to community contributions

Include a postgresql instance to run the demos(both demos store data in jdbc)

The final step to create your test cluster will be to run the compose file:
docker-compose up -d
To validate your cluster just access the spark UI on each worker & master URL

Spark Master: http://localhost:9090

Alt Text

Spark Worker 1: http://localhost:9091

Alt Text

Spark Worker 2: http://localhost:9092

Alt Text

Database Server

To check database server just use the psql command(or any database client of your choice):
psql -U postgres -h 0.0.0.0 -p 5432
#It will ask for your password defined in the compose file
The Demo Apps
The following apps can be found in apps directory, this apps are used as proof of concept of our cluster behavior.

NY Bus Stops Data [Pyspark]
This programs just loads archived data from MTA Bus Time and apply basic filters using spark sql, the result are persisted into a postgresql table.

The loaded table will contain the following structure:

latitude	longitude	time_received	vehicle_id	distance_along_trip	inferred_direction_id	inferred_phase	inferred_route_id	inferred_trip_id	next_scheduled_stop_distance	next_scheduled_stop_id	report_hour	report_date
40.668602	-73.986697	2014-08-01 04:00:01	469	4135.34710710144	1	IN_PROGRESS	MTA NYCT_B63	MTA NYCT_JG_C4-Weekday-141500_B63_123	2.63183804205619	MTA_305423	2014-08-01 04:00:00	2014-08-01
To submit the app connect to one of the workers or the master and execute:
/opt/spark/bin/spark-submit --master spark://spark-master:7077 \
--jars /opt/spark-apps/postgresql-42.2.22.jar \
--driver-memory 1G \
--executor-memory 1G \
/opt/spark-apps/main.py
Alt Text

MTA Bus Analytics[Scala]
This program takes the archived data from MTA Bus Time and make some aggregations on it, the calculated results are persisted on postgresql tables.

Each persisted table correspond to a particullar aggregation:

Table	Aggregation
day_summary	A summary of vehicles reporting, stops visited, average speed and distance traveled(all vehicles)
speed_excesses	Speed excesses calculated in a 5 minute window
average_speed	Average speed by vehicle
distance_traveled	Total Distance traveled by vehicle
To submit the app connect to one of the workers or the master and execute:
/opt/spark/bin/spark-submit --deploy-mode cluster \
--master spark://spark-master:7077 \
--total-executor-cores 1 \
--class mta.processing.MTAStatisticsApp \
--driver-memory 1G \
--executor-memory 1G \
--jars /opt/spark-apps/postgresql-42.2.22.jar \
--conf spark.driver.extraJavaOptions='-Dconfig-path=/opt/spark-apps/mta.conf' \
--conf spark.executor.extraJavaOptions='-Dconfig-path=/opt/spark-apps/mta.conf' \
/opt/spark-apps/mta-processing.jar
You will notice on the spark-ui a driver program and executor program running(In scala we can use deploy-mode cluster)

Alt Text

Conclusions
We've created a simpler version of a spark cluster in docker-compose, the main goal of this cluster is to provide you with a local environment to test the distributed nature of your spark apps without making any deploy to a production cluster.

The generated image isn't designed to have a small footprint(Image size is about 1gb).

This cluster is only necessary when you want to run a spark app in a distributed environment in your machine(Production use is discouraged, use databricks or kuberetes setup instead).

What's left to do?
Right now to run applications in deploy-mode cluster is necessary to specify arbitrary driver port through spark.driver.port configuration (I must fix some networking and port issues).

The spark submit entry in the start-spark.sh is unimplemented, the submit used in the demos can be triggered from any worker.

Top comments (4)

Subscribe
pic
Add to the discussion
 
 
chpiero profile image
chpiero
•
Oct 8 '22

beautiful solution!!
in case I have instead of CPU GPU how can I modify the compose? also if I have the worker on another machine physically different from the master I just have to change the address inside the composer or do you need something else?

thank you


1
 like
Like
Reply
 
 
mhkdunn profile image
MHKDunn
•
Sep 16 '22 • Edited on Sep 16

I seem to have most of this working but the last step to persist the data isn't working due to missing database mta_data?

An error occurred while calling o48.jdbc.
: org.postgresql.util.PSQLException: FATAL: database "mta_data" does not exist
at org.postgresql.core.v3.QueryExecutorImpl.receiveErrorResponse(QueryExecutorImpl.java:2552)
at org.postgresql.core.v3.QueryExecutorImpl.readStartupMessages(QueryExecutorImpl.java:2664)
at org.postgresql.core.v3.QueryExecutorImpl.(QueryExecutorImpl.java:147)
at org.postgresql.core.v3.ConnectionFactoryImpl.openConnectionImpl(ConnectionFactoryImpl.java:273)
at org.postgresql.core.ConnectionFactory.openConnection(ConnectionFactory.java:51)
at org.postgresql.jdbc.PgConnection.(PgConnection.java:223)
at org.postgresql.Driver.makeConnection(Driver.java:465)
at org.postgresql.Driver.connect(Driver.java:264)
at org.apache.spark.sql.execution.datasources.jdbc.DriverWrapper.connect(DriverWrapper.scala:45)
at org.apache.spark.sql.execution.datasources.jdbc.JdbcUtils$.$anonfun$createConnectionFactory$1(JdbcUtils.scala:67)
at org.apache.spark.sql.execution.datasources.jdbc.JdbcRelationProvider.createRelation(JdbcRelationProvider.scala:48)
at org.apache.spark.sql.execution.datasources.SaveIntoDataSourceCommand.run(SaveIntoDataSourceCommand.scala:46)
at org.apache.spark.sql.execution.command.ExecutedCommandExec.sideEffectResult$lzycompute(commands.scala:70)
at org.apache.spark.sql.execution.command.ExecutedCommandExec.sideEffectResult(commands.scala:68)
at org.apache.spark.sql.execution.command.ExecutedCommandExec.doExecute(commands.scala:90)
at org.apache.spark.sql.execution.SparkPlan.$anonfun$execute$1(SparkPlan.scala:180)
at org.apache.spark.sql.execution.SparkPlan.$anonfun$executeQuery$1(SparkPlan.scala:218)
at org.apache.spark.rdd.RDDOperationScope$.withScope(RDDOperationScope.scala:151)
at org.apache.spark.sql.execution.SparkPlan.executeQuery(SparkPlan.scala:215)
at org.apache.spark.sql.execution.SparkPlan.execute(SparkPlan.scala:176)
at org.apache.spark.sql.execution.QueryExecution.toRdd$lzycompute(QueryExecution.scala:127)
at org.apache.spark.sql.execution.QueryExecution.toRdd(QueryExecution.scala:126)
at org.apache.spark.sql.DataFrameWriter.$anonfun$runCommand$1(DataFrameWriter.scala:962)
at org.apache.spark.sql.execution.SQLExecution$.$anonfun$withNewExecutionId$5(SQLExecution.scala:100)
at org.apache.spark.sql.execution.SQLExecution$.withSQLConfPropagated(SQLExecution.scala:160)
at org.apache.spark.sql.execution.SQLExecution$.$anonfun$withNewExecutionId$1(SQLExecution.scala:87)
at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:764)
at org.apache.spark.sql.execution.SQLExecution$.withNewExecutionId(SQLExecution.scala:64)
at org.apache.spark.sql.DataFrameWriter.runCommand(DataFrameWriter.scala:962)
at org.apache.spark.sql.DataFrameWriter.saveToV1Source(DataFrameWriter.scala:414)
at org.apache.spark.sql.DataFrameWriter.save(DataFrameWriter.scala:398)
at org.apache.spark.sql.DataFrameWriter.jdbc(DataFrameWriter.scala:790)
at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(Unknown Source)
at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(Unknown Source)
at java.base/java.lang.reflect.Method.invoke(Unknown Source)
at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:357)
at py4j.Gateway.invoke(Gateway.java:282)
at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
at py4j.commands.CallCommand.execute(CallCommand.java:79)
at py4j.GatewayConnection.run(GatewayConnection.java:238)
at java.base/java.lang.Thread.run(Unknown Source)

@mvillarrealb


Like
Reply
 
 
sunmoon4ever profile image
sunmoon4ever
•
Mar 19 '22

Spark job (Scala/s3) worked fine for few runs in stand-alone cluster with spark-submit but after few run it started giving the below error. There were no changes to code, it is making connection to spark-master but immediately application is getting killed with the reason “All masters are unresponsive! Giving up”.

Error

22/03/20 05:33:39 INFO StandaloneAppClient$ClientEndpoint: Connecting to master spark://spark-master:7077...
22/03/20 05:33:39 INFO TransportClientFactory: Successfully created connection to spark-master/xx.x.x.xxx:7077 after 42 ms (0 ms spent in bootstraps)
22/03/20 05:33:59 INFO StandaloneAppClient$ClientEndpoint: Connecting to master spark://spark-master:7077...
22/03/20 05:34:19 INFO StandaloneAppClient$ClientEndpoint: Connecting to master spark://spark-master:7077...
22/03/20 05:34:39 ERROR StandaloneSchedulerBackend: Application has been killed. Reason: All masters are unresponsive! Giving up.
22/03/20 05:34:39 WARN StandaloneSchedulerBackend: Application ID is not initialized yet.
22/03/20 05:34:39 INFO Utils: Successfully started service 'org.apache.spark.network.netty.NettyBlockTransferService' on port 33139.
22/03/20 05:34:39 INFO NettyBlockTransferService: Server created on a1326e4ae4bb:33139
22/03/20 05:34:39 INFO BlockManager: Using org.apache.spark.storage.RandomBlockReplicationPolicy for block replication policy
22/03/20 05:34:39 INFO SparkUI: Stopped Spark web UI at xxxxxxxxxxxxx:4040
22/03/20 05:34:39 INFO BlockManagerMaster: Registering BlockManager BlockManagerId(driver, a1326e4ae4bb, 33139, None)
22/03/20 05:34:39 INFO StandaloneSchedulerBackend: Shutting down all executors
22/03/20 05:34:39 INFO BlockManagerMasterEndpoint: Registering block manager a1326e4ae4bb:33139 with 1168.8 MiB RAM, BlockManagerId(driver, a1326e4ae4bb, 33139, None)
22/03/20 05:34:39 INFO CoarseGrainedSchedulerBackend$DriverEndpoint: Asking each executor to shut down
22/03/20 05:34:39 INFO BlockManagerMaster: Registered BlockManager BlockManagerId(driver, a1326e4ae4bb, 33139, None)
22/03/20 05:34:39 INFO BlockManager: Initialized BlockManager: BlockManagerId(driver, a1326e4ae4bb, 33139, None)
22/03/20 05:34:39 WARN StandaloneAppClient$ClientEndpoint: Drop UnregisterApplication(null) because has not yet connected to master
22/03/20 05:34:39 INFO MapOutputTrackerMasterEndpoint: MapOutputTrackerMasterEndpoint stopped!
22/03/20 05:34:39 INFO MemoryStore: MemoryStore cleared
22/03/20 05:34:39 INFO BlockManager: BlockManager stopped
22/03/20 05:34:39 INFO BlockManagerMaster: BlockManagerMaster stopped
22/03/20 05:34:39 INFO OutputCommitCoordinator$OutputCommitCoordinatorEndpoint: OutputCommitCoordinator stopped!
22/03/20 05:34:40 ERROR SparkContext: Error initializing SparkContext.
java.lang.IllegalArgumentException: requirement failed: Can only call getServletHandlers on a running MetricsSystem
at scala.Predef$.require(Predef.scala:281)


1
 like
Like
Reply
 
 
purnima1612 profile image
purnima1612
•
Jul 13 '22

I am unable to connect spark worker with master getting below mentioned error :
22/07/14 01:07:56 INFO Worker: Started daemon with process name: 557@spark-worker
22/07/14 01:07:56 INFO SignalUtils: Registering signal handler for TERM
22/07/14 01:07:56 INFO SignalUtils: Registering signal handler for HUP
22/07/14 01:07:56 INFO SignalUtils: Registering signal handler for INT
22/07/14 01:07:56 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
22/07/14 01:07:56 INFO SecurityManager: Changing view acls to: glue_user
22/07/14 01:07:56 INFO SecurityManager: Changing modify acls to: glue_user
22/07/14 01:07:56 INFO SecurityManager: Changing view acls groups to:
22/07/14 01:07:56 INFO SecurityManager: Changing modify acls groups to:
22/07/14 01:07:56 INFO SecurityManager: SecurityManager: authentication enabled; ui acls disabled; users with view permissions: Set(glue_user); groups with view permissions: Set(); users with modify permissions: Set(glue_user); groups with modify permissions: Set()
22/07/14 01:07:56 INFO Utils: Successfully started service 'sparkWorker' on port 40843.
22/07/14 01:07:56 INFO Worker: Worker decommissioning not enabled, SIGPWR will result in exiting.
22/07/14 01:07:56 INFO Worker: Starting Spark worker 172.24.0.3:40843 with 8 cores, 23.8 GiB RAM
22/07/14 01:07:56 INFO Worker: Running Spark version 3.1.1-amzn-0
22/07/14 01:07:56 INFO Worker: Spark home: /home/glue_user/spark
22/07/14 01:07:56 INFO ResourceUtils: ==============================================================
22/07/14 01:07:56 INFO ResourceUtils: No custom resources configured for spark.worker.
22/07/14 01:07:56 INFO ResourceUtils: ==============================================================
22/07/14 01:07:57 INFO log: Logging initialized @1340ms to org.sparkproject.jetty.util.log.Slf4jLog
22/07/14 01:07:57 INFO Server: jetty-9.4.37.v20210219; built: 2021-02-19T15:16:47.689Z; git: 27afab2bd37780d179836e313e0fe11bc4fa0ce9; jvm 1.8.0_322-b06
22/07/14 01:07:57 INFO Server: Started @1447ms
22/07/14 01:07:57 INFO AbstractConnector: Started ServerConnector@582f7291{HTTP/1.1, (http/1.1)}{0.0.0.0:8080}
22/07/14 01:07:57 INFO Utils: Successfully started service 'WorkerUI' on port 8080.
22/07/14 01:07:57 INFO ContextHandler: Started o.s.j.s.ServletContextHandler@73ee79ce{/logPage,null,AVAILABLE,@Spark}
22/07/14 01:07:57 INFO ContextHandler: Started o.s.j.s.ServletContextHandler@6d7ea67a{/logPage/json,null,AVAILABLE,@Spark}
22/07/14 01:07:57 INFO ContextHandler: Started o.s.j.s.ServletContextHandler@54bf8430{/,null,AVAILABLE,@Spark}
22/07/14 01:07:57 INFO ContextHandler: Started o.s.j.s.ServletContextHandler@20de6297{/json,null,AVAILABLE,@Spark}
22/07/14 01:07:57 INFO ContextHandler: Started o.s.j.s.ServletContextHandler@118e7b91{/static,null,AVAILABLE,@Spark}
22/07/14 01:07:57 INFO ContextHandler: Started o.s.j.s.ServletContextHandler@7e83cf73{/log,null,AVAILABLE,@Spark}
22/07/14 01:07:57 INFO WorkerWebUI: Bound WorkerWebUI to 0.0.0.0, and started at http://spark-worker:8080
22/07/14 01:07:57 INFO Worker: Connecting to master spark-master:7077...
22/07/14 01:07:57 INFO ContextHandler: Started o.s.j.s.ServletContextHandler@394bb5d9{/metrics/json,null,AVAILABLE,@Spark}
22/07/14 01:07:57 ERROR TransportClientFactory: Exception while bootstrapping client after 169 ms
java.lang.RuntimeException: java.lang.IllegalArgumentException: Authentication failed.
at org.apache.spark.network.crypto.AuthRpcHandler.doAuthChallenge(AuthRpcHandler.java:125)


Like
Reply
Code of Conduct • Report abuse
DEV Community

50 CLI Tools You Can't Live Without


>> Check out this classic DEV post <<

Read next
prasenjeetsymon profile image
Docker : From Zero to Hero 🛸 ( part 1)
Prasenjeet Kumar - May 3

javinpaul profile image
My Favorite Courses to Learn Docker and Containers in Depth
javinpaul - Apr 28

madmaxx profile image
Building Docker Images Smaller, Rootless and Non-Shell for Kubernetes
Robert Nemet - Apr 17

prasenjeetsymon profile image
Docker : From Zero to Hero 🛸 ( part 2)
Prasenjeet Kumar - May 4


Marco Villarreal
Follow
Pragmatic software developer with strong focus on Backend and Cloud Engineering.
EDUCATION
Computer Science Bachelor
WORK
Technical Product Owner at IRDigital
JOINED
Nov 18, 2019
More from Marco Villarreal
Deploy a Serverless Api on Cloud Run with Github Actions
#googlecloud #go #docker
E2E Sandbox with Test-containers
#testing #microservices #java #docker
profile
Cloudsmith
PROMOTED

Unpacked Conference Details

A FREE virtual conference for DevOps Professionals and Engineering Leaders
📺 Attend virtually from anywhere
🗺 Developers, DevOps Engineers, Security Professionals and IT Leaders from across the globe!
🤑 $0 to join

Register


# builder step used to download and configure spark environment
FROM openjdk:11.0.11-jre-slim-buster as builder

# Add Dependencies for PySpark
RUN apt-get update && apt-get install -y curl vim wget software-properties-common ssh net-tools ca-certificates python3 python3-pip python3-numpy python3-matplotlib python3-scipy python3-pandas python3-simpy

RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1

# Fix the value of PYTHONHASHSEED
# Note: this is needed when you use Python 3.3 or greater
ENV SPARK_VERSION=3.0.2 \
HADOOP_VERSION=3.2 \
SPARK_HOME=/opt/spark \
PYTHONHASHSEED=1

# Download and uncompress spark from the apache archive
RUN wget --no-verbose -O apache-spark.tgz "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
&& mkdir -p /opt/spark \
&& tar -xf apache-spark.tgz -C /opt/spark --strip-components=1 \
&& rm apache-spark.tgz


# Apache spark environment
FROM builder as apache-spark

WORKDIR /opt/spark

ENV SPARK_MASTER_PORT=7077 \
SPARK_MASTER_WEBUI_PORT=8080 \
SPARK_LOG_DIR=/opt/spark/logs \
SPARK_MASTER_LOG=/opt/spark/logs/spark-master.out \
SPARK_WORKER_LOG=/opt/spark/logs/spark-worker.out \
SPARK_WORKER_WEBUI_PORT=8080 \
SPARK_WORKER_PORT=7000 \
SPARK_MASTER="spark://spark-master:7077" \
SPARK_WORKLOAD="master"

EXPOSE 8080 7077 6066

RUN mkdir -p $SPARK_LOG_DIR && \
touch $SPARK_MASTER_LOG && \
touch $SPARK_WORKER_LOG && \
ln -sf /dev/stdout $SPARK_MASTER_LOG && \
ln -sf /dev/stdout $SPARK_WORKER_LOG

COPY start-spark.sh /

CMD ["/bin/bash", "/start-spark.sh"]
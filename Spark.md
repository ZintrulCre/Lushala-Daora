1. change password

   sudo passwd root

2. download spark

   curl http://apache.mirror.digitalpacific.com.au/spark/spark-2.4.2/spark-2.4.2-bin-hadoop2.7.tgz -o spark.tgz

3. build  image

   - cd Spark
   - docker build --tag spark-test:2.4.2 spark/

4. push image

  - docker tag spark-test:2.4.2 zintrulcre/spark-test:0.0.1
  - docker push zintrulcre/spark-test:0.0.1

5. docker-compose up
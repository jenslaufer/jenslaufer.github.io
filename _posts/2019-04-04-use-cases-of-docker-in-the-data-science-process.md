---
title: "Example Use Cases of Docker in the Data Science Process"
subtitle: '...or how to avoid the It-works-on-my-computer-but-nowhere-else-problem'
image: '/assets/img/PnvK7v6.png'
output: html_document
layout: post
show_comments: yes
tags: docker, process, data science
categories: data science
language: en
---






The excellent [comic by Jeff Lofvers](http://donthitsave.com/comic/2016/07/15/it-works-on-my-computer) 
illustrates what you often face in software development but also in data science. You are preparing a data analysis or predictive model, 
but when you want to share it, then it does not work on someone else machine. It fails, 
because libraries are missing, libraries are having the wrong version ("dependency hell"), or configurations are differing. Time-Consuming troubleshooting starts.

The solution is not far away: [Docker](https://www.docker.com/) solves the problem of reproducibility in a lightweight manner, but also offers you many other advantages. 

__What is Docker?__

Docker is a free software that performs operating-system-level virtualisation.
Docker is used to running software packages called containers. Containers are isolated from each other and bundle their application, tools, libraries and configuration files. All containers are run by a single operating system kernel and are thus more lightweight than virtual machines. [[Wikipedia on Docker](https://en.wikipedia.org/wiki/Docker_(software))]

Docker makes it easy to create, run and distribute applications. Applications are packaged up with everything that is needed to run the application. The concept guarantees that the container can be run on every docker runtime environment.

__Advantages of Docker__:

1. _Reproducibility_

    With Docker, you ensure that your software artefact (application, data analysis, predictive model etc.) runs on all docker runtime environments. Your shipments are more robust, as the container contains everything that's needed to run your artefact. You are not distributing only the code, but also the environment.

2. _Consistency_

    Docker equips you with one uniform and consistent runtime environment for all kinds of software artefacts. It reduces the time for system administration and lets you focus on your core work. You might know Anaconda environments; Docker is something similar for the __whole software ecosystem__.

3. _Traceability_ 

    a.) Version controlling of Docker container code

    A Docker container is built from a script which is a human-readable summary of the necessary software dependencies and environment. This script can be version controlled. The script is entirely traceable this way.


    b.) Uniform distribution environment for all artefacts

    Docker containers can be stored in a repository within your organisation. You keep the whole version history this way.

4. _Portability_

    Docker containers can easily be ported from one docker environment to another. [Docker Swarm](https://docs.docker.com/engine/swarm/) (or [Kubernetes](https://kubernetes.io/)) lets you scale applications automatically. Costs for system administration and operation are reduced this way.


However, what are the use-cases for Docker in the data science universe? I will concentrate on data science [OSEMN process](https://www.thelead.io/data-science/5-steps-to-a-data-science-project-lifecycle): 



![OSEMN: Data Science Process](https://www.thelead.io/wp-content/uploads/2019/01/data-science-process-OSEMN-framework.jpg)



## Use Cases of Docker in the Data Science Process

Reality is today that the process consists of a wide variety of tools and programming languages. Docker is the go-to platform to manage these heterogenous technology stacks, as each container provides the runtime environment it needs to run exactly the one application it is packed around. The interference of technology stacks is reduced this way. 

### 1. Obtain: Gather Data from relevant sources

Data is the oil for data science. You retrieve it, e.g. from surveys, clinical trials, web scraping, scientific experiments, corporate applications or simulations. Typically data engineers are dealing with the data, but also other stakeholders are involved, which leads to a wide diversity of database systems and programming languages. 

  - Web scraping: Python application with low-level dependencies to Selenium's Chrome driver and a Postgres database is packed as a multi-container application with [Docker Compose](https://docs.docker.com/compose/)
  - Labelling images: Lean web application with vue.js, a NodeJS backend and a MongoDB is used to label images
  - Surveys: Small static microsite build by the marketing team  in plain HTML with an integrated SurveyMonkey form 
  - Corporate application: Banking web application implemented in AngularJS and Java in the backend with an Oracle database produces valuable banking data from the customers
  - Computer simulation: Simulation programmed in C++ stores its results in JSON on Amazon S3 
  - Asynchronous data streams:  Car Sensors are sending their data to Kafka, which is distributing the data within the company
  
All these technology stacks can be run independently within Docker containers. 

### 2. Scrub: Clean and aggregate data to formats the machine understands

The Data which was obtained in Step 1 is the oil, but right now it's raw oil. You need to clean, process and combine it to the data you need for analysis and modelling.

  - Aggregation: An Application in Java gets the data from Kafka streams, does aggregations on the low-level data and stores it to an Oracle database
  - Data analysts clean and preprocess the data from a corporate web application as preparation for answering a business question with an RMarkdown Notebook, which they want to share with the management
  - A Machine Learning Engineer combines data from different data sources, cleans and preprocesses data for a predictive model in a Jupyter Notebook 
  - Data is combined, cleaned, aggregated and preprocessed and persisted for high-level interactive dashboards in Tableau


Some of these use cases might be already done in the data retrieval step and have more a data engineering technology stack. Other use cases overlap with the exploration and modelling phase and involve technologies more typical for data analytics.

A lot of data analytics work is done in Notebooks (Jupyter, RMarkdown) which need to be published. You can use a central Jupyter instance for the organisation. The problem with this approach is that you might be stuck with fixed configurations and library versions. Another method would be to publish one or more Notebooks with Docker containers. Then you are more flexible with particular setups.  


### 3. Explore: Find patterns and trends

In the exploration phase, all you have to do is to understand what patterns and values are in the hands of the data. You want to make the results available to everyone interested.


  - Data Analysts are creating Jupyter or RMarkdown Notebooks to answer a question they need to share with everyone interested in it.
  - Data Analysts cluster the companies customers into new segments which are persisted in a Customer Segment Database in MySQL
  - Data Analysts build interactive web applications for high-level data exploring for interested stakeholders in RShiny, Dash, Tableau or Kibana. This way managers can find patterns on their own (danger zone!).
  

### 4. Model: Construct models to predict and forecast

The cleaned and preprocessed data is used to train machine or deep learning algorithms. You create models which are a mathematical representation of observed data this way. They can be used for predictions, forecasts and quantification of the ineffable.

- The complete training process for a neural network for object detection in images is isolated to a Docker container that is run on Azure, AWS or Google Cloud
- A Keras model is imported into DeepLearning4J and published as a Java Microservice due to performance issues with Python

To train neural networks you need a lot of GPU power. You need [Nvidia Docker](https://github.com/NVIDIA/nvidia-docker) for isolating the training process to a Docker container, as using GPU cannot be done in a hardware-agnostic and platform-agnostic way.


### 5. Interpret: Put the results into good use

The data science insights are communicated and visualised. Models are distributed as microservices.

- Microsites to tell the data story
- A predictive machine learning model in Python is released as microservice
- A REST microservice  in Java with aggregated data is released to paying B2B customers
- A product recommender Service in Python is integrated into the company's web application
- Data-driven stories are  published on the company's Tableau Server and shared for internal and external use
- Data storytellers in the content management team share exciting insights from data analysts on a static Jekyll website 


## Conclusion

Docker is a powerful tool also for data scientists and can be applied to all stages in the OSEMN process. You can ship all kind of artefacts in a consistent, reproducible and traceable way. The artefacts can be very different in their technology stack, which is the reality in data science projects. Data engineers work with databases like Oracle, MySQL, MongoDB, Redis or ElasticSearch or programming languages like Java, Python or C++. In the analytics and modelling team, people might work with R, Python, Julia or Scala, while data storytellers tell their story with d3.js in JavaScript or use Tableau. As specialists are rare, it's better to let them work with familiar technologies instead of pushing them into something unknown. You get better results faster. 

Docker is the way to go to manage the heterogeneous technology landscape in data science.

## References

[Running Jekyll with Docker](https://kristofclaes.github.io/2016/06/19/running-jekyll-locally-with-docker/)

[Running Kibana on Docker](https://www.elastic.co/guide/en/kibana/current/docker.html)

[HOWTO: Tableau Server Linux in Docker Container](https://databoss.starschema.net/tableau-server-linux-docker-container/)

[Running dash app in docker container](https://community.plot.ly/t/running-dash-app-in-docker-container/16067)

[Learn How to Dockerize a ShinyApp in 7 Steps](https://www.bjoern-hartmann.de/post/learn-how-to-dockerize-a-shinyapp-in-7-steps/)

[How to compile R Markdown documents using Docker](https://jlintusaari.github.io/2018/07/how-to-compile-rmarkdown-documents-using-docker/)

[Tutorial: Running a Dockerized Jupyter Server for Data Science](https://www.dataquest.io/blog/docker-data-science/)
[Kafka-Docker: Steps To Run Apache Kafka Using Docker](https://medium.com/@rinu.gour123/kafka-docker-steps-to-run-apache-kafka-using-docker-1645e85acd50)

[Dockerizing an Angular App](https://mherman.org/blog/dockerizing-an-angular-app/)

[Dockerizing a Node.js web app](https://nodejs.org/de/docs/guides/nodejs-docker-webapp/)

[Dockerize Vue.js App](https://vuejs.org/v2/cookbook/dockerize-vuejs-app.html)

[Running MongoDB as a Docker container](https://www.thachmai.info/2015/04/30/running-mongodb-container/)

[Dockerize PostgreSQL](https://docs.docker.com/engine/examples/postgresql_service/)

[Docker Image with Chromedriver and Geckodriver](https://cloud.docker.com/repository/docker/jenslaufer/docker-chromedriver-geckodriver)

[Dockerize your Python Application](https://runnable.com/docker/python/dockerize-your-python-application)

---
title: "qraptor Technology Stack Part Two: Applications in September 2019"
subtitle: "The application we use for our reinforcement trading platform"
output: html_document
image: "https://res.cloudinary.com/jenslaufer/image/upload/c_scale,q_74,w_800/v1568015884/matt-artz-pH6wLT6TVFc-unsplash.jpg"
image_caption: "Photo by Matt Artz on Unsplash"
tags: docker, programming languages, technology stacks, applications
categories: qraptor
layout: post
language: en
---

In [Part One: Architecture and Programming Languages](/qraptor/qraptors-technology-stack-programming-languages.html) we showed you that we using several programming 
languages to get things done. Today we want to go more into details what applications/micro services for our reinforcement trading platform. It's devided into
several parts. First, we show you the shared technical services we use and second all the services to run our core business: algorithmic trdaing with reinforcement learning.

## Shared Technical Services ##

## MongoDB ##

![@TODO MongoDB Logo]()

MongoDb is our persistence container for a variety of artefacts, some of them are saved as MongoDB documents, which is basically simple JSON. We use also the GridFS-Filesystem for persisting
file-like structures. We love MongoDB, because of it's simplicity. You don't need schemas to persist data. However, we know that having no schema is in some situations risky.

The artefacts we persist in MongoDB:

- Training Session Meta Data 
@TODO example

We save the complete the Meta Data for each training session with all the parmeters in the MongoDB. The trainer fetches new training sessions and dynamically initializes the train

- Trained Models from Trainer in hdf5 file

What we haven't done so far is to persist the source data files into the MongoDB, although they should be there to be fully straighforward. To be honest we are bit to scared to save hundreds of GB in the GridFS.
filesystem.

- Training results as CSV


## Portainer ##

Every application/service we use is packed as a Docker container. We use docker-compose and docker-machine for the management of the application. We use [Portainer](https://www.portainer.io/) for web based Docker management. Portainer is a Docker container by itself and is dead-simple to install and makes life easy.

![Portainer Screenshot for qrapotor Applications](@TODO)


## Exploratory Data Analysis ##

For the exploratory data analysis we use RMarkdown a lot. As the data files are very big we apply some data reducing before. We seperate the core logic and visualisations from the Rmarkdown code to reuse it in other notebooks and in Shiny Apps. We use Shiny Dashboards for on the fly data analysis or for Dashboarding for our clients.

## Data Wrangling ##

### Data Reducing ###

For our one client we are having data for each instruments for very second for 9 years with about 30 datapoints. It adds about to about 15 GB of data each instrument. Importing this amount of data into a dataframe with pandas in Python or dplyr in R is challenge. So we perform a kind of reducing on the data for data analysis or our first training sessions. You can reduce the data to a certain unit and interval e.g. five minutes or 30 seconds. The Libraries from [tidyverse](https://www.tidyverse.org/) ecosystem in R lets us do this redcution. The code is pretty self-explaining with a bare minimum lines of code. We added REST-like interface to the reducer microservice with [plumber](https://www.rplumber.io/).

### Data Preprocessing ###

We created a data preprocessing microservice also with a REST-like API with plumber. We can select what features we want to include into the datasets and which of these fields need to be preprocessed. The services splits in a first step the training and test data. The data are time series data, so we detrended the data by differencing.

## Training Environment ##

### Training Framework ###

Our Training frameworks loads training sessions from the MongoDB and initializes dynamically the Python objects for the training. We do the Then a training is performed and the model is tested against the test set. The training and test process, the model and test metrics are persisted in the MongoDB. We keep our  training process reproducable this way. The heart of the training framework are [OpenAI Gym Environment](https://github.com/openai/gym/blob/master/docs/creating-environments.md) and the [Stable Baseline](https://stable-baselines.readthedocs.io/en/master/) implementations of reinforcement learning algorithms, although the framework should also be able to use other libraries like [Keras-RL](https://github.com/keras-rl/keras-rl).

### Training Session Tool ###

The JSON for training session is very complicated, as it holds all attributes for a training session. Adding new training sessions into the DB takes therefore a lot of time and is error prone. Parameter tuning requires strategies: You change e.g. one parameter and observe if the performance on the test set is getting better or not. We created a tool that lets us easily create multiple training sessions for different parameter set ups. The tool is written with [Vue.js](https://vuejs.org/) and [Quasar](https://quasar.dev/) with a [Spring Boot](https://spring.io/projects/spring-boot) Java Backend.


### Tensorboard ###

Tensorboard lets us track session experiment metrics, visualise the training process and model graphs. We use Tensorboard hand in hand with out Training Analysis Dasboard to analyse our training sessions.

[@Todo Screenshot]()


## Training Result Analysis ##

We created a dashboard for analysis of the training results. It's a shiny app with very lines of code. ggplot2 is our visualisation library, as it is the vis library we are the most familiar with. The ggplot visualisations by itself are not per se interactive, but we might use plot.ly in future to accomplish this.
Another option is to integrate our own datapoints into Tensorboard visualisations.

[@Todo Screenshot ]()

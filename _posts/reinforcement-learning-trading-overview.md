---
title: "Qraptor Tech Series: Architecture and Programming Languages"
subtitle: "The technology stack and programming languages we use for our reinforcement learning based trading platform"
output: html_document
image: "https://res.cloudinary.com/jenslaufer/image/upload/c_scale,q_74,w_800/v1568015884/matt-artz-pH6wLT6TVFc-unsplash.jpg"
image_caption: "Photo by Matt Artz on Unsplash"
tags: docker, programming languages, technology stacks
categories: qraptor
---

Lately we landed a big deal from a chinese company: The goal of the project is to implement a trading algorithm. I want to write a article series to share our experiences along the project. First I want to tell you why the project is a big adventure for us. It has different components which makes it so interesting, but also challenging.

## The client is from China

Working for a client from overseas is an adventure by itself, but we guess that a client from China is a challenge, because of the cultural differences. The client seems very pragmatic in comparison to european corporate clients. Fixing the contract was done within a few days. A few days after signing the contract we got the data for 65 instruments. It was not uploaded to the cloud what you would expect in these days, instead we received a 1TB harddrive (no joke!) filled with 560GB trading data by airmail. We guess the data is worth a lot. However, we cannot trade on the Chinese Market as non-chinese. Maybe a reason why the client outsourced the project to non-chinese.

## Reinforcement Learning for our trading agent

>Classical algorithmic trading is a method of executing orders using automated pre-programmed trading instructions. Algorithmic trading makes use of much more complex formulas, combined with mathematical models and human oversight, to make decisions to buy or sell financial securities on an exchange. Algorithmic traders often make use of high-frequency trading technology, which can enable a firm to make tens of thousands of trades per second.
https://www.investopedia.com/terms/a/algorithmictrading.asp

Classical algorithmic trading often includes relatively simple logics, which trade with the high frequency. 
  
## It's our first full lifecycle data science project, from analysis and preprocessing of the raw data to bringing the models into production

We worked before  in many corporate software engineering projects as freelancers, but also on our own full stack software projects. In data science our experience is limited so far to one part of the stack like data analysis, machine learning modelling or shipping models into production.

The trading project is our first full life cycle data science project, which includes data analysis, cleaning and preprocessing of the data, building a trading simulation environment with Open AI gym, training a reinforcement algorithm, shipping a model into production.

We have several ideas about the project. We want to use R for data analysis and preprocessing and Python for algorithm training, for handling life data we might use a reactive Java Spring Boot application. D For the trading simulation we want to use our own customized Open AI gym environment and the stable-baseline reinforcement algorithm implementations from stable-baseline as our main technology stack. Our goal is to implement a library that allows us to dynamically load and initialize configuartions from a database to limit codes changes to the bare minimum while evaluating different configurations. Results of the training process should be also persisted in the database to increase the reproducibility. To handle our polyglot technology stack (R, Python, Java) we want to use Docker.

## It's a project we can turn into a product

We are very excited about project, because we can make a product 
 


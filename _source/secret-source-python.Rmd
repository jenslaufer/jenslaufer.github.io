---
title: "The secret component to do machine learning in Python in a flexible way"
output: html_document
---

I trained last year my first neural network. As a software engineer with 20 years experience I put some effort in making the code nicely. I wanted to use Docker to be fexible with my training.
However, the nearer the deadline came I put less and less effort on code quality and archtecture. I ended up with a Jupyter notebook I ran on a GPU instance on AWS. I logged into the server instance and
commited the code changes to Git. However we know that Jupyter and Git are not the best friends. The project was a success, but I ended up in a mess.

This year with some background in Keras I am not struggling so much with coding part of neural networks, so I put some effort on putting the training process into a Docker containers and train the neural network on AWS with GPU. I shared my insights lately in a article. I was very proud on the article and my insights, but the feedback from other dat scientist was restrained. This made me think about more and noticed that as software engineer I am always have in my mind to reduce the lines of code, how to bring something into production. The most data scientist are not so interessted in this part of the story. They rather like the quick and dirty approach in  Jupyter Notebook or doing the training on Colab. And they are right in the way, why should someone pay a lot of money for GPU, when you can get of free on Colab. 
 
I am unhappy with the approaches. I thought more about that topic, which brought me the secret component that let you be flexible in training model. The secret "compoment" is not the secrept. 

The solution is very simple:


PYTHON MODULES


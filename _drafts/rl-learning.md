# Why I want to Reinforcement Learning

I got my first insights into Reinforcement Learning in my course for the [Machine Learning Nanodegree](). I teached a car learning to drive. The car got the sensor data for the directions to the final destination and the data for color of the traffic lights. The car could drive stop, go straight, turn left or right. The whole example was implemented from the scratch, to learn idea for reinforcement learning. But it was actually too much code to understand LL basic ideas about the environment and the agent. I love to have just the code, which is important to crasp the concepts. I got a general idea in the course. Don't misunderstand me, the example was actually great. I tried later to find more examples. All these examples were using the openai framework. The problem was, that the examples had nothing in common with the implementation in the course, so I gave up. However I was not investing too much time into it. I am a software engineer, who wants to use frameworks to solve different problems with the same patterns.

These days I gave RL another try, as I want to create a automatic self learning stock trading bot. Trading seems a good field for reinforcement learning, as you get a human being also creates a strategy when trading to try to maximize the earnings. This strategy is also a trial and error approach, like reinforcement learning. You have clear rewards.
The data is available everywhere. The field seems easier than let an agent learn to play chess, but more profitable.

So let's quickly brainstorm what questions and problems I have. The goal is to solve the problems. I am a hands on type of person. The goal is to have a working strategy at the end.

- What algorithms are suitable for the problem?
- Can I develop a minimal viable example?
- Is there a difference between the training environment and real life environments?
- Can the ready-to-use algorithms from baseline be customized (e.g exploitation vs exploration)

From what I understand I must setup a environment with the observation space and action space. Observations are partially describing the state space.

What is our trading agent about. First we need to analyse a stock, who seems suitable for trading. 
I analyse the time series for this.
What makes a stock interesting for training from my naive point of view:

- share price tendency goes up
- the share price is volatile
- enough volume, so that we can trade

What is the action space:

- It's a discrete action space with the actions "sell", "hold", "buy"
- To make the trading bot as simple, we just have an amount to invest

Questions:

- Does we invest everything in the beginning?
- Do we partially sell and buy?


Steps to perform:

- Get data for training
- Split training and test set
- Design the environment
- Train the agent
- Test the agent
- Do we need a live environment?

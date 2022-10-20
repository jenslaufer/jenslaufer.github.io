# Is it possible to rate aesthetics of images with a computer program?

Yes, it's possible, however not with classical programming. What do I mean with traditional programming? Classical programming is rule-based: It defines rules that are processed (think of if...else statements) with an image as an input. What could be the rules for beautiful photos? You might think of a high-resolution image with a beach and a blue sky. However, sometimes the photo might be a blurry one with an interesting person on it. Or a colourful one. Oh, I forgot about these pretty black and white photos. You see, it's challenging to define rules for beautiful photos.

A way to solve the problem is with machine learning or AI what you call it nowadays: You train a neural network with images because neural networks are a way to quantify the ineffable. One kind of neural network which is suitable for this kind of problem is Convolutional Neural Networks (CNN).

You need a balanced dataset with a great variety of photos (good and bad ones, different scenaries) to train the neural network. The dataset mustn't be biased. Think of a situation that people rated the images. However, all the people were actually male. It turns out that they rated all images with women in bikinis with the best rating. Now you have a bias.

I trained end of 2018 a CNN for image aesthetics with the AVA dataset and wrote an article about it: Image aesthetics quantification with a convolutional neural network (CNN)
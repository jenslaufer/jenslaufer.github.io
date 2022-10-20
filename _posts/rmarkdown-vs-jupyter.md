# The RMarkdown Notebooks vs Jupyter Notebook

This is the RMarkdown vs Jupyter Notebook showdown. While the first is the standard notebook in the R ecospcae comes the latter from Python world. However, you can use Python in RMarkdown and R in Jupyter.

## Version Control

Version controlling is essential in the world of software.

RMarkdown Notebooks are saved as they are in plain text without the results of code sells, to share your work you need to build a target file e.g like PDF, Word. HTML or just plain Markdown. Version control is a breathe as you easily to diffs from one version to another.

Juypter Notebooks are saved in Json. What's special about them is that the code is saved along with the resulting cell. Having the result cell also has the advantage that you can share the notebooks like they are, you don't have building step in it and you can use the jupyter webapp as similiar to an IDE. You can share Jupyter Notebooks on Github as Github is able to render notebooks. However you price for it. Jupyter Notebooks and version control are not friends. You can diff notebooks easily as there is a lot biolerplate JSON and having the results in the Notebooks is also breaking the version control, as you also have binary data for plots in the Json. 

## Exporting notebooks

## Sharing Notebooks

## Paramterizing Notebooks

You have to have an extra building step to render the Rmarkdown notebooks. On the one hand this is a big advantage, but on the other hand you are more flexibel. You can esily create paramterized reports and add additional rendering templates. So it's easy to create reporting pipelines with RMarkdown.

It#s difficult to change the result of a notebook in Jupyter and create paramterized reports.

## Tooling: Working with Notebooks

The RMarkdown you could easily work with simple text editor and with the use of build script you can create the arget file. But in practice this working style is a pain. To work similiar to Juypter you need to install RStudio on your machine. This is by far not as lightweight as Juypter where your browser is your working envrionment.
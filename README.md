# splink_demos

This repo contains interactive notebooks containing demonstration and tutorial for the Splink record linking library, the homepage for which is [here](https://github.com/moj-analytical-services/splink).

## Running these notebooks interactively

You can run these notebooks in an interactive Jupyter notebook by clicking the button below:

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/moj-analytical-services/splink_demos/master?urlpath=lab/tree/index.ipynb)

## Running these notebooks locally in VSCode

If you don't already have it, you'll need to install java on your system in order to run `pyspark`, which splink currently depends on.
Download java for your specific OS from [here](https://www.java.com/en/download/manual.jsp).

You can check the installation went correctly by using:

> `java -version`
> within a terminal instance. It should return details of your java installation.

If you have multiple java installations, you may need to change the version of java you're currently using.

To download the example notebooks, simply [clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#cloning-a-repository) this repository:

```
git clone git@github.com:moj-analytical-services/splink_demos.git
```

Create a [virtual environment](https://docs.python.org/3/library/venv.html) using:

```
python3 -m venv <name_of_venv>
```

Install the package list (which includes `pyspark`) with:

```
pip3 install -r requirements.txt
```

and, if you want to use jupyter, add a kernel corresopnding to your venv:

```
python -m ipykernel install --user --name=my-virtualenv-name
jupyter lab
```

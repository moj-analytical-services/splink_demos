# Splink demos

This repo contains interactive notebooks containing demonstration and tutorial for version 5 of the Splink record linking library, the homepage for which is [here](https://github.com/moj-analytical-services/splink).

## Running these notebooks interactively

You can run these notebooks in an interactive Jupyter notebook by clicking the button below:

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/moj-analytical-services/splink_demos/master?urlpath=lab)

## Running these notebooks locally in VSCode

To download the example notebooks, simply [clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#cloning-a-repository) this repository:

```bash
git clone git@github.com:moj-analytical-services/splink_demos.git
```

You can set up a virtual environment and install dependencies with:

```bash
./recreate_venv.sh
```

See [that script](./recreate_venv.sh) for details of setting up. You may instead wish to work with any suitable environment running Splink 4.

### Spark

If you don't already have it, you'll need to install java on your system in order to run `pyspark`, which you will need for any spark notebooks. You will need to manually install a suitable version `pyspark` for use with Splink.
Download java for your specific OS from [here](https://www.java.com/en/download/manual.jsp).

You can check the installation went correctly by using:

> `java -version`
> within a terminal instance. It should return details of your java installation.

If you have multiple java installations, you may need to change the version of java you're currently using.

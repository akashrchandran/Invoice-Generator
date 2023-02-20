# Invoice-Generator

Simple Invoice Generator made uing python flask mini web framework.

Live deployed version available at https://invoice-generator.akashrchandran.repl.co/

## Example Usage

![ezgif com-gif-maker (1)](https://user-images.githubusercontent.com/78685510/220176643-d2b2e3d0-9f8d-476d-8a23-782fce703cab.gif)

<div align="center">
  
__You can check the output file at [here](https://invoice-generator.akashrchandran.repl.co/share?id=NDM3MTUw).__
  
</div>

# Local Installation

> Clone to the local machine using git

```
git clone https://github.com/akashrchandran/Invoice-Generator/
```
> change directory and install depedencies using below commands

```
cd Invoice-Generator
pip install -r requirements.txt
```
> Database and Image hosting
### Mongo DB
you can sign up at [Mongo DB](https://www.mongodb.com/) and create a free cluster and set your URI as env variable `MONGO_URI`
### ImgBB
you can sign up at [ImgBB](https://imgbb.com/) and get your API key and then set it as env variable `ImgBB_API_KEY`
> Run local server using
### Linux based OS
```
python3 index.py
```
### Windows
```
py index.py
```

> Now open any browser on your computer and enter this link `http://127.0.0.1:8080` and press enter.

You should be able to see the app running.

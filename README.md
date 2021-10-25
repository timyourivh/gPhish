# gPhish
Universal phishing tool that accepts vue templates.

## !!! Disclaimer !!!

I am by no means a professional hacker/socialengineer. I made this tool for fun so if you see any room for impovements feel free to create a pr or fork.
I was inspired by [htr-tech](https://github.com/htr-tech)'s [zPhisher](https://github.com/htr-tech/zphisher).

---
### #Installation

requirements:
* php
* node package manager like npm or yarn
```sh
git clone (public repo url)
cd gPhish
pip3 install -r requirements.txt
py ./
```
The first time you launch this program it will prompt you to fill in your node package manager's commands for installing and building

npm: 
:   `npm run install` and `npm run build`

Yarn:
:   `yarn install` and `yarn build`

---
### #Usage
I dont know how to add a command to the systems cli so you'll have to start the program by following these steps:
1. Move to the root folder
1. Run `py ./` or `python ./` (It will run the `__main__.py` automatically)

Once started you can pick a template and run it.

*If anyone can come up with a better way of doin this feel free to create a pr*

---
### #Creating templates

I've tried to make creating templates as easy as possible!

First create a folder in `templates/` named after the category. For example let's create a category named "examples":
```
gPhish/templates/examples
```
Next, we'll create a template name. For example "simple":
```
gPhish/templates/examples/simple
```
Now we have to decide if we want to make a simple page or a vue project. I will describe how to make both! First the simple page:

#### Simple page:
In the folder `gPhish/templates/examples/simple` we'll create a index.html file with basic login details:
```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>My login page</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="">
    </head>
    <body>
        <h1>My login page</h1>
        <fieldset style="width: 200px;">
            <legend>Login to my login page</legend>
            <form action="/login" method="POST">
                <label for="user">Username:</label><br>
                <input type="text" id="user" name="user"><br>
                <label for="pass">Password:</label><br>
                <input type="password" id="pass" name="pass"><br><br>
                <input type="hidden" name="redir_url" value="https://www.youtube.com/watch?v=dQw4w9WgXcQ">
                <input type="submit" value="Login">
            </form>
        </fieldset>
    </body>
</html>
```
Important:
:   To get the input into the file and console we need to have 2 input elements:
* input named "user": `<input type="text" id="user" name="user">`
* input named "pass": `<input type="password" id="pass" name="pass">`
 
To redirect users after the request we'll add:
* hidden input named "redir_url": `<input type="hidden" name="redir_url" value="http://www.website.com/">`
* If this input is not found in the request it will show the following page to catch the error: 

You can also make a post request with jquery to `/login` with parameters `user` and `pass` and it will be saved and shown in the terminal.

__That's it!__ if you followed these steps the template should show up in the program and you should be able to use it.

now, on to the vue project:

#### Vue project:
__Requirements:__
* vue-cli

For this example we'll create a template named vueproject, to do that we'll move to `gPhish/templates/examples/` and open a terminal window.
In this folder we'll open a terminal and create a vue project as follows:
```shell
vue create vueproject
```
After running this command vue-cli will ask what preset you want to use feel free to pick any option. I've only tested with Vue 2 so far so that's what I will pick for this example.

After the command has finished move to the project folder and install axios:
```
cd vueproject
vue add axios
```
The reason you want to install axios is because you can send requests to the server in the background and it is very easy to use.

Next, create your login form using this structure:

html
```html
<input type="text" v-model="form.user">
<input type="password" v-model="form.pass">
```
script
```javascript
// In your data function you want to create a from object like this
data: () => ({
    form: {
        user: '',
        pass: '',
    }
})
```
Validation is all up to the creator of the template for now. I may add a default password standard in the future.

Submit it whenever you like by calling `this.$axios.post('login', this.form)`.

---

### #Configurable .env

A nice feature I've added is the ability to configure .env files before building. It uses the following syntax:

__Important:__ The file must be named `.env.example` the script will create a new `.env` every build.
```sh
## Non configurable:
TEST1='Non configurable .env values (development only)'

## Configurable
!TEST2=#('Default value')#

## Don't forget if you want to use env variables in the frontend of vue project, prefix them with 'VUE_APP_' like this:
VUE_APP_TEST3='Front-end variable'
```

### License

```
gPhish - Open-Source Phishing Framework

The MIT License (MIT)

Copyright (c) 2021 Tim van Herwijnen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software ("gPhish") and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

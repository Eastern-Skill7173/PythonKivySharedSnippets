# SharedSnippets

This repo contains a set of common python, kivy & kivymd utilities 
I have found myself using throughout the years and a base template for my projects.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for personal use, development or testing purposes.

### Pre-Packaged Executables

Setting up the program using pre-packaged executables doesn't require anything. Simply download the best provided package for your machine (_based on your os and CPU architecture_).

Current available packages are:

* Windows (_.exe_)
* RHEL & Fedora (_.rpm_)
* Ubuntu (_.deb_)
* Android (_.apk_)

If your operating system or architecture is __not__ included in the packages list, you can follow the rest of this guide to set up the project from source.

### From Source

If your operating system or architecture is not included in the packages list, or you plan on contributing or testing the project you can set it up from the source code. follow these steps as mentioned:

1. You __MUST__ have a python >= 3.8 interpreter installed on your machine
   * To check your python version, you can do:

     ```
     python3 --version
     ```
   
   * If you are ___Windows___, you can visit the official [python](https://www.python.org/) website to download a matching version
   * If you are on ___Linux OR Mac___, you already have python installed, but it is highly possible that is does not match the minimum required version. You can get a matching version using the package manager on your machine Examples:
   
     On _Ubuntu_:

     ```
     sudo apt install python3
     ```
   
     On _Fedora_:

     ```
     sudo dnf install python3
     ```
   
     On _Mac (Using homebrew)_:
     
     ```
     brew install python
     ```


2. You __MUST__ also have ___pip___ installed
    * To check if you have pip installed, you can do:
      ```
      pip --version
      ```
    * If you are ___Windows___, you probably have pip installed
    * If you are on ___Linux OR Mac___, using your package manager you can install pip. Examples:

      On _Ubuntu_:
    
        ```
        sudo apt install python3-pip
        ```
    
      On _Fedora_:

        ```
        sudo dnf install python3-pip
        ```
      On _Mac (Using homebrew)_:

        ```
        python3 -m pip install --upgrade pip
        ```


3. You __MUST__ also have ___git___ installed on your machine to be able to copy the repo, otherwise you are going to have to manually copy and paste the files' content
    * To check if you have git installed, you can do:
      ```
      git --version
      ```
    On _Ubuntu_:
      ```
      sudo apt install git
      ```
    On _Fedora_:
      ```
      sudo dnf install git
      ```
    On _Mac (Using homebrew)_:
     
     ```
     brew install git
     ```


4. (__OPTIONAL__) If you are on ___Linux OR Mac___, for better keyboard integration it is recommended to install the _xclip_ and _xsel_ packages. Examples:

    On _Ubuntu_:
      ```
      sudo apt install xclip xsel
      ```
    On _Fedora_:
      ```
      sudo dnf install xclip xsel
      ```
    On _Mac (Using homebrew)_:
     
      ```
      brew install xclip xsel
      ```

5. It is __highly recommended__ that you create a python virtual environment. A virtual environment helps organize projects and prevent python package conflicts.

    1. Ensure you have the latest setuptools and virtualenv packages installed:
        ```
        pip3 install setuptools virtualenv
        ```
    2. Create a virtual environment named _venv_ in the current working directory
        ```
        python3 -m virtualenv venv
        ```
    3. Activate the virtual environment. Beware that everytime a new terminal session is launched you are going to have to re-activate the virtual environment
       * If you are on _Windows CMD (default terminal)_:
         ```
         .\venv\Scripts\activate
         ```
       * If you are on a _BASH terminal on Windows_:
         ```
         source ./venv/Scripts/activate
         ```
       * If you are on _Linux OR Mac_:
         ```
         source ./venv/bin/activate
         ```
       You should now see the name of the virtual environment as a prefix on each line of the terminal. This indicates that the virtual environment has been turned on successfully.
    4. Clone the repository:

      ```
      git clone https://github.com/Eastern-Skill7173/SharedSnippets.git
      ```
      _TIP:_ you can add a `--depth 1` to the end of the command to only copy the latest version of each file if you are planing on just using the project, like so:
      ```
      git clone https://github.com/Eastern-Skill7173/SharedSnippets.git --depth 1
      ```


6. Install the mentioned requirements in the `requirements.txt` file included inside the copied project folder, like so:
    ```
    pip3 install -r SharedSnippets/requirements.txt
    ```

7. The project is now installed! All that is remaining is to run the `main.py` file located in the project folder, like so:
    ```
    python SharedSnippets/main.py
    ```

Installing project from source has many benefits, the most important one being that in the future if any updates are released you can easily just update the files and re-run the script, like so:

```
git pull
```

Another great feature is that you can change the code however you like! If there is a specific feature that is not covered by the project you can add it yourself!

## Running the tests

Explain how to run the automated tests for this system

### Break down into end-to-end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Built With

* [Python](https://www.python.org/) - The core programming language
* [Kivy](https://kivy.org/#home) - The core GUI framework
* [KivyMD](https://github.com/kivymd/KivyMD) - Kivy widget extensions following material design

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) & [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* [**Eastern-Skill7173**](https://github.com/Eastern-Skill7173) - *creator and maintainer*

See also the list of [contributors](https://github.com/Eastern-Skill7173/SharedSnippets/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Special thanks to the kivy & kivymd team
* Anyone who has shared or committed to the project
* Also, [_Billie Thompson_](https://github.com/PurpleBooth) for this README template

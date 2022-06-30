# PBuild
Just a little tool created in python to automate the proccess of downloading & building [Pa](https://github.com/valkarias/Pa).

## Downloading
PBuild is avaliable for Windows, Linux and Mac os under the [releases](https://github.com/valkarias/PBuild/releases/tag/latest) section.  
Get the zip version suitable for your platform.  

There is only one prerequisite, PBuild needs a [C](https://en.wikipedia.org/wiki/C_(programming_language)) compiler to build with, more details in the [Commands](https://github.com/valkarias/PBuild/new/master?readme=1#commands) *build* section.

## Usage
The zip contains exactly 1 one file. 
PBuild is a command line tool, it means you can only use it via your console or terminal.

### Commands

- *version:* This command is used of course, to display either the latest version from Pa repository or the one installed in your computer.
```bash
pbuild version

pbuild version --latest
```
<br>

- *download:* This command will download Pa repository as a zipfile into your computer, and extracts it into your PC's home directory.
```bash
pbuild download
```
<br>

- *build:* This command builds the downloaded repository, it takes a required option specifiying the **compiler** to use. There is only 2 compilers supported as of now:  <br>
<br><a href="https://gcc.gnu.org/">Gnu Compiler Collection (gcc)</a><br><a href="https://bellard.org/tcc/">Tiny C Compiler (tcc)</a>
<br>

Example:
```bash
pbuild build --cc-type=gcc
```
<br>

**{+}:** After building is finished, The Pa executable will be located in `(you-home-directory)/Pa/bin` folder.
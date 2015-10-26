# pimpl cpp generator

generate pimpl idiom code &nbsp;&nbsp; [![Build Status](https://travis-ci.org/notetau/pimpl-cpp-generator.svg?branch=master)](https://travis-ci.org/notetau/pimpl-cpp-generator)

## Install
This command uses libclang. You need to install libclang.

On Ubuntu 15.10:
``` sudo apt-get install libclang1-3.6 ```

## Option

| option | long option | description |
| -- | ------ | -- |
| -t | --target-class | [class name] implementation class |
| -o | --output-class |  [class name] set output class |
| -v | --dammy-var-prefix | [var name] if a function declaration has no argument variable name, put dummy variable there (default 'pimplvar') |
| |  --pimpl-name |  [var name] name of pimpl pointer (default 'pimpl') |
| |  --decl-with-def | define output class's delegate functions in class declaration (in common case, no need this option) |
| -h | --help |show this help message and exit |

## Usage

### Replace class name

for example : sample.cpp

``` c++
class Sample {
    public:
      Sample();
      int do_public(int x);
    private:
      void do_private();
  };
```

replace Sample to Sample_Impl

``` c++
class Sample::Sample_Impl {
    public:
      Sample_Impl();
      int do_public(int x);
    private:
      void do_private();
  };
```

### generate pimpl code

run :
```
$ ./pimplgen.py sample.cpp -t Sample_Impl -o Sample > gencode.cpp
```

gencode.cpp
``` c++
class Sample {
public:
    Sample();

    int do_public(int x);

private:
    class Sample_Impl;
    Sample_Impl* pimpl;
};

Sample::Sample() : pimpl(new Sample_Impl()) {}

Sample::~Sample() { delete pimpl; }

int Sample::do_public(int x) {
    return pimpl->do_public(x);
}
```

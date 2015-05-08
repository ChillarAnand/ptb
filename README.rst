ptb - Python TraceBack for humans!
----------------------------------

ptb aims to enhance the default python traceback. ptb speeds up
debugging process by

-  Taking away unwanted frames.

-  Bringing more context & relevant information.

Demo
~~~~

The default Python traceback looks like this

ptb traceback looks like this

Install
~~~~~~~

Recomended way is to install it using pip.

::

    pip install ptb

You can also install using easy\_install

::

    easy_install ptb

You can also install from git repo

::

    git clone https://github.com/ChillarAnand/ptb.git
    cd ptb/
    python setup.py install

Usage
~~~~~

Just add this line at the top of your script

::

    import ptb; ptb.enable()

and run your script

::

    python my_script.py

Features
~~~~~~~~

Filtering frames from your project.

::

    import ptb; ptb.enable(path='/path/to/project')

Modify context according to your needs.

::

    import ptb; ptb.enable(context=5)

Get locals & builtins for all frames.

::

    import ptb; ptb.enable(locals=True, builtins=True)


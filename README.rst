ptb - Python TraceBack for humans!
----------------------------------

ptb aims to enhance the default python traceback. ptb speeds up
debugging process by

-  Taking away unwanted frames.

-  Bringing more context & relevant information.



Demo
~~~~

**The default Python traceback looks like this**

|PTB0|

**ptb traceback looks like this**

|PTB1|



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

Test your existing script without editing it:

::

    python -m ptb my_script


Or just add this line at the top of your script

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


.. |PTB0| image:: https://cloud.githubusercontent.com/assets/4463796/7541758/3ee3b404-f5d5-11e4-8e6a-714f7623ad98.png
.. |PTB1| image:: https://cloud.githubusercontent.com/assets/4463796/7541757/3ee13e54-f5d5-11e4-9e18-f9a175545fca.png



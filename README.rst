Checklist
=========

`Scott Torborg <http://www.scotttorborg.com>`_

Checklist is a command-line tool for managing--you guessed it--checklists.

**Note: this is a preliminary spec, and this software doesn't actually work
yet.**

Overview
--------

So let's say you design lots of PCBs. You've made a checklist for your PCB
designs, so that you don't forget to do things when you get boards made.::

    $ cat pcb-design.md

    Debuggability:

    * Include test points, especially on critical traces from small-pitch
      components.
    * When extra IO and space is available, include one or more LEDs that is
      directly controlled by a dedicated MCU pin.

    General:

    * Check connectors to ensure that the mating half will not interfere with
      nearby components.
    * Check component footprints. Verify pinout, ensure that any non-standard
      packages were drawn from a top view and not a bottom view. Where possible,
      particularly with unconventional footprints, compare actual components to a
      1:1 printout of the board.

Your four-item checklist has saved your bacon a few times, but you
occassionally forget to go through it, or change something after you go through
it.

Enter Checklist.

First you'll register your checklist.::

    $ checklist register pcb-design.md

Then you can apply it in a project.::

    $ cd ~/my-awesome-pcb

    $ checklist check
    No checklist is registered for this project tree. Please select one:
    [1] pcb-design
    [2] static-website
    [3] android-app
    >>> 1

    Using pcb-design checklist. Let's go!
    -------------------------------------------
    Include test points, especially on critical traces from small-pitch
    components. [Y/n]
    -- Never checked.
    >>> Y
    -------------------------------------------
    When extra IO and space is available, include one or more LEDs that is
    directly controlled by a dedicated MCU pin. [Y/n]
    -- Never checked.
    >>> ^C

You can quit anytime you want. You can see that a file called
``checklist.json`` has been created in the local directory. It records when you
run checklist, and when you check things off. Next time you run it::

    $ checklist check
    Using pcb-design checklist. Let's go!
    -------------------------------------------
    When extra IO and space is available, include one or more LEDs that is
    directly controlled by a dedicated MCU pin. [Y/n]
    -- Never checked.
    >>> ^C

If you've changed files since a check-off, you'll be prompted to recheck it.::

    $ checklist check
    Using pcb-design checklist. Let's go!
    -------------------------------------------
    Include test points, especially on critical traces from small-pitch
    components. [Y/n]
    -- Last checked on 2015-09-13 by scott.
    >>> Y

You'll probably want a way to make sure that you actually follow the checklist.
You can use the included ``checklist verify`` command inside a Makefile, a
deployment step, or a git pre-commit hook for that. If the checklist is
incomplete, a non-zero exit status will be returned.::

    $ make cam-files.zip
    checklist verify
    Checklist pcb-design not verified: 12 items unchecked.
    make: *** [all] Error 1

More Usage
----------

Want to update a checklist? Just re-register it with the same filename.::

    $ checklist register pcb-design.md

Checklist reviews are 'invalidated' by file modiifcation times. So if you want
to force a review of your checklist, just touch a file.::

    $ touch file.brd

To see what checklists are registered, you can call::

    $ checklist view
    Checklists available:
    - pcb-design
    - static-website
    - android-app

Or look at a specific checklist.::

    $ checklist view static-website
    ...


Installation
============

Install with pip::

    $ pip install checklist

License
=======

Checklist is licensed under an MIT license. Please see the LICENSE file for
more information.

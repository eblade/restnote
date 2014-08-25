restnote
========

Restnote is a scripting layer on the top of Python. The main features are:

* Building Rest-based client scenarios with a minimum of boiler-plate code
* Generate a HTML-formatted diary of the HTTP methods done along with any xpaths
  resolved.

Dependencies
------------

* python3
* requests
* lxml
* pygments (optional)

Syntax
------

Most operations in restnote follow a simple pattern:

    COMMAND ARG1, ..., ARGn -> TARGET

where:

* `COMMAND` is one of the available keywords described later.
* `ARG1, ..., ARGn` is a comma-separated list of arguments.
* `TARGET` is a variable to use for storing the result. Variable names may
  include any characters, except for parenteses `()`, but including spaces.

Arguments are either a string or an abject. Objects are referred using
parenteses:

    get (some uri) -> response

Objects can be used as parts of strings:

    value World -> who
    log Hello (who)!

This example also shows the use of the `value` command to store a string into an
object. Multi-line strings can be stored using the `until` construct:

    until end
    More
    than
    one
    line
    end -> multiline

where `end` is what the parser waits for at the beginning of the line to stop
reading data.


Branches, loops and functions
-----------------------------

Branches are created using the `if` statement.

    if EXPRESSION
        STATEMENTS
    endif

where:

* `EXPRESSION` is a Python expression evaluated with the current variable-space.
* `STATEMENTS` are any number of statements to execute if the expressions returns
  `True`.

Note that the construct returns the value of the construct, which can be assigned
to a target varaible:

    if 1 + 1 = 2
        log It adds up!
    endif -> result

The variable space is the same within as outside the `if` block.

There are two kinds of loops, `while` and `each`. While evaulates a Python
expression before each execution loop and only executes it if it returns `True`.

    while EXPRESSION
        STATEMENTS
    endwhile -> number of loops done

Example:

    eval 0 -> x
    while x < 4
        log x is (x)
        eval x + 1 -> x
    endwhile -> count
    log There were (count) loops

will tell you there were 4 loopsa. The variable space of the while loop is shared
with the one above.

Functions, or Sub-routines, are defined with the `sub` block.

    sub
        STATEMENTS
        return VALUE
    endsub ARG1, ..., ARGn -> TARGET

where:

* `STATEMENTS` are any number of statements to execute.
* `VALUE` is a value or object to return.
* `ARG1, ..., ARGn` are any number of argument names in the order to pass them in
  when using the function.
* `TARGET` is the variable to store the function in.

The function will only have access to the variable you pass in. Functions are
called using the `call` command:

    call FUNCTION, ARG1, ..., ARGn -> result

where:

* `FUNCTION` is the reference to a function, e.g. `(my function)`.
* `ARG1, ..., ARGn` are arguments to pass in.

Example of a function that does not return anything:

    sub
        log Hello (name)!
    endsub name -> say hello
    call (say hello), World

Another example of a function that returns something is:

    sub
        eval (a) + (b) -> sum
        return (sum)
    endsub a, b -> plus
    call (plus), 4, 2 -> result
    log 4 + 2 is (result)

If you have a list of objects, you might want to use the `each` keyword:

    each LIST, FUNCTION, ARG2, ..., ARGn -> TARGET

where:

* `LIST` is a list object to loop through.
* `FUNCTION` is the function to use to handle each entry. It should take the
  entry as first argument and may take more after that. It should return what
  you want to have in the resulting list.


Example:

    list string 1, string 2, string 3 -> my list
    sub
        return touched (item)
    endsub item -> touch
    each (my list), (touch) -> my resulting list
    log (my resulting list)


Command reference
-----------------

### HTTP Commands

    connect HOST, USERNAME, PASSWORD

will connect you session to `HOST` using `USERNAME` and `PASSWORD` as
credentials. Available commands are then:

    get URL, [ACCEPT], [HEADERS] -> RESPONSE
    put URL, DATA, CONTENT-TYPE, [HEADERS] -> RESPONSE
    post URL, DATA, CONTENT-TYPE, [HEADERS] -> RESPONSE
    delete URL, [HEADERS] -> RESPONSE

where:

* `URL` is the full URL
* Optional `ACCEPT` is the value of the `Accept` header.
* Optional `HEADERS` is a `dict` object with additional headers.
* `DATA` is any string or file-like object.
* `CONTENT-TYPE` is the value of the `Content-Type` header.
* `RESPONSE` is a `reqeusts.Reponse` object that can be unpacked using the
  commands `xml` or `raw`.


When handling the responses, these commands would come in handy:

    namespace SHORT, URI
    xml RESPONSE -> DOM
    raw RESPONSE -> STRING
    headers RESPONSE -> HEADERS

The defining of namespaces is session-global and should be setup in the
beginning of the script.

### SYSTEM COMMANDS

    include MODULE, [OPTIONS]

will include a file named `MODULE`.rest, run it and merge its variable space
into yours. If `OPTIONS` has the term `log`, logging from the included `MODULE`
will also be printed, else it will be discarded.

    env VARIABLE, [DEFAULT] -> TARGET

will read the environment variable `VARIABEL` and return the value of it or
what's in `DEFAULT` (empty string if not given).

    fopen FILE -> TARGET
    fclose TARGET

will open a file-like object with the file `FILE` and store the object into
`TARGET`, which can be used as `DATA` by the HTTP commands.

    dict KEY1=VALUE1, ..., KEYn=VALUEn -> TARGET

will create a dictionary with string keys and values and store it into `TARGET`.

    list ITEM1, ..., ITEMn -> TARGET
    append LIST, ITEM

will create a list with the given items (which can be object references) and
store it into `TARGET`. The `append` command appends `ITEM` to `LIST`.

    value VALUE -> TARGET

will store the value `VALUE` into `TARGET`

    eval EXPRESSION -> TARGET

will eval `EXPRESSION` in python using your variable space and store the result
in `TARGET`.

    log DESRCIPTION, [DATA], [FORMAT]
    %% TITLE
    % NARRATIVE

will send a log post containing `DESCRIPTION` and `DATA`. `FORMAT` can be either
`xml`, `pp` (pretty print), `title` or `comment`. The other two lines are syntax
sugar for creating titles and comments.

    sleep SECONDS

will let the process sleep for `SECONDS` seconds, where `SECONDS` is a floating
point number.

### Various commands

    xpath DOM/ELEMENT, XPATH, [SINGLE=(true)] -> TARGET

will evaluate `XPATH` on `DOM/ELEMENT`. If `SINGLE` is `(true)`, it will return
the first result, otherwise a list. Attributes `@attribute` and values `/text()`
will return strings or list of strings.

    template TEMPLATE, DICTIONARY -> URL

will take an OpenSearch Template and substitute or remove all query parameters
using `DICTIONARY`. The result is a `URL` for doing `get` on.

    fill DATA, DICTIONARY -> MODIFIED DATA

will perform variable insertion of `(variable)` in the `DATA` using your variable
space.

    urilist LIST -> DATA

will create a URI List (new line separated) using the URIs in `LIST`.

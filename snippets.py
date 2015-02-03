import logging
import argparse
import sys

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet
  
def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet...

    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""
  
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparser = parser.add_subparsers(dest="command", help="Available commands")
    
    #subparser for put
    logging.debug("constructing put subparser")
    put_parser = subparser.add_parser("put", help="store a snippet")
    put_parser.add_argument("name",help="The name of the snippet")
    put_parser.add_argument("snippet",help="the snippet")
    
    #subparser for get
    logging.debug("constructing get subparser")
    get_parser = subparser.add_parser("get",help="retrieve a snippet")
    get_parser.add_argument("name",help="The name of the snippet")
    
    arguments = parser.parse_args(sys.argv[1:])
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "put":
      name, snippet = put(**arguments)
      print("Stored {!r} as {!r}".format(snippet,name))
    elif command == "get":
      snippet.get(**arguments)
      print("Retrieved snippet {!r}".format(snippet))

if __name__ == "__main__":
    main()
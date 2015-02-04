import logging
import argparse
import sys
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    logging.info("Storing snippet - put({!r}, {!r})".format(name, snippet))
    cursor = connection.cursor()
    try:
      command = "insert into snippets values (%s, %s)"
      cursor.execute(command, (name, snippet))
    except psycopg2.IntegrityError as e:
      connection.rollback()
      command = "update snippets set message=%s where keyword=%s"
      cursor.execute(command, (snippet,name))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet
  
def get(name):
  """Retrieve the snippet with a given name.

  If there is no such snippet...

  Returns the snippet.
  """
    
    
  logging.info("Getting snippet - get({!r})".format(name))
    
  cursor = connection.cursor()
  with connection, connection.cursor() as cursor:
    cursor.execute("select message from snippets where keyword=%s", (name,))
    row = cursor.fetchone()
  
  if not row:
    #no message found
    print('No snippet with that key found')
    return ""
  else:
    return row[0]
  
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
      snippet = get(**arguments)
      print("Retrieved snippet {!r}".format(snippet))

if __name__ == "__main__":
    main()
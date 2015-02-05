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
    with connection, connection.cursor() as cursor:
      try:
        command = "insert into snippets values (%s, %s)"
        cursor.execute(command, (name, snippet))
      except psycopg2.IntegrityError as e:
        connection.rollback()
        command = "update snippets set message=%s where keyword=%s"
        cursor.execute(command, (snippet,name))
   
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
  
def catalog(): 
  """ retrieve all entries """
  with connection, connection.cursor() as cursor:
    cursor.execute("select keyword from snippets order by keyword")
    keywords = cursor.fetchall()
  return keywords

def search(searchstring):
  """ search for keywords """
  with connection, connection.cursor() as cursor:
    command = command = "select * from snippets where keyword like (%s)"
    cursor.execute(command, (searchstring,))
    rows = cursor.fetchall()
  return rows
  
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
    
    #subparser for search
    logging.debug("constructing search subparser")
    get_parser = subparser.add_parser("search",help="look for a string")
    get_parser.add_argument("searchstring",help="The string to search on")
    
    #subparser for catalog
    logging.debug("constructing catalog subparser")
    catalog_parser = subparser.add_parser("catalog",help="list all snippets")
   
    if(len(sys.argv) < 2):
      command = "catalog"
    else:
      arguments = parser.parse_args(sys.argv[1:])
      arguments = vars(arguments)
      command = arguments.pop("command")
    
    if command == "put":
      name, snippet = put(**arguments)
      print("Stored {!r} as {!r}".format(snippet,name))
    elif command == "get":
      snippet = get(**arguments)
      print("Retrieved snippet {!r}".format(snippet))
    elif command == "catalog":
      keywords = catalog()
      for keyword in keywords:
        print(keyword[0])
    elif command == "search":
      rows = search(**arguments)
      for row in rows:
        print(row[0] + " = " + row[1])

if __name__ == "__main__":
    main()
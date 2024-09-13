# Import the main query function
from .main import query_kg

# The __all__ declaration helps define what is publicly accessible
__all__ = ['query_kg']

# This allows you to import the query_kg function from the query module like this:
# from query import query_kg
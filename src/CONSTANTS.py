import os

SCRIPT_DIR =        os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR =        os.path.join(SCRIPT_DIR, '../static')
DESTINATION_DIR =   os.path.join(SCRIPT_DIR, '../docs')
TEMPLATE_PATH =     os.path.join(SCRIPT_DIR, '../template.html')
FROM_PATH =         os.path.join(SCRIPT_DIR, '../content/index.md')
DESTINATION_FILE =  os.path.join(DESTINATION_DIR, 'index.html')
CONTENT_DIR =       os.path.join(SCRIPT_DIR, '../content')
BASE_PATH =         "/" 
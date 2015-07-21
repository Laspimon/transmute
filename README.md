# transmute
Automatically transform data between diffent schemas.

Form A:
  A = {
    'Animals': {
       'Four legged': ['Tiger', 'Bear', 'Turtle'],
       'Two legged': ['Man', 'Monkey', 'Penguin'] },
    'Plants': {
       'Flowers': ['Dandelion', 'Rose'] }
    }
Form B:
  B = {
    '4-legged animals': ['Tiger', 'Bear', 'Turtle'],
    '2-legged animals': ['Man', 'Monkey', 'Penguin'],
    'Flowers': ['Dandelion', 'Rose'] }

The aim of this project is to allow for automatic transformation between data structures. If we have large amounts of data with Form A, but want to represent it with Form B, we can train the system to recognize which operations need to be performed, in order to make the transformation without errors.
